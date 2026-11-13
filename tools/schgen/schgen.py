"""Generate KiCad schematics from a netlist-style description.

Every pin gets a short wire stub that ends in a global label, a power symbol
or a no-connect flag. The design is flat: a net name means the same net on every sheet.
"""
import copy
import math
import os
import uuid

from sx import Q, parse, dump, find, find_all

SYMBOL_DIR = os.environ.get("KICAD_SYMBOL_DIR", "/usr/share/kicad/symbols")
NS = uuid.UUID("6f1c1e0a-5b7e-4f6e-9a40-000000000000")
STUB = 2.54
FONT = ["effects", ["font", ["size", 1.27, 1.27]]]


def uid(*key):
    return Q(str(uuid.uuid5(NS, "/".join(str(k) for k in key))))


def effects(justify=None, hide=False):
    e = ["effects", ["font", ["size", 1.27, 1.27]]]
    if justify:
        e.append(["justify"] + justify.split())
    if hide:
        e.append(["hide", "yes"])
    return e


# ---------------------------------------------------------------- library

class Library:
    def __init__(self):
        self.cache = {}

    def _load_raw(self, lib, name):
        path = os.path.join(SYMBOL_DIR, lib + ".kicad_symdir", name + ".kicad_sym")
        tree = parse(open(path, encoding="utf-8").read())
        for s in find_all(tree, "symbol"):
            if s[1] == name:
                return s
        raise KeyError(lib + ":" + name)

    def add_custom(self, lib_id, sym):
        self.cache[lib_id] = sym

    def get(self, lib_id):
        """Return the flattened symbol tree, top-level name not yet prefixed."""
        if lib_id in self.cache:
            return self.cache[lib_id]
        lib, name = lib_id.split(":")
        s = self._load_raw(lib, name)
        ext = find(s, "extends")
        if ext:
            parent = copy.deepcopy(self.get(lib + ":" + ext[1]))
            pname = parent[1]
            parent[1] = Q(name)
            for sub in find_all(parent, "symbol"):
                sub[1] = Q(name + sub[1][len(pname):])
            for prop in find_all(s, "property"):
                old = [p for p in find_all(parent, "property") if p[1] == prop[1]]
                if old:
                    parent[parent.index(old[0])] = prop
                else:
                    idx = max(parent.index(p) for p in find_all(parent, "property"))
                    parent.insert(idx + 1, prop)
            s = parent
        self.cache[lib_id] = s
        return s

    def pins(self, lib_id, unit=1):
        s = self.get(lib_id)
        out = []
        for sub in find_all(s, "symbol"):
            u = int(sub[1].rsplit("_", 2)[1])
            if u not in (0, unit):
                continue
            for p in find_all(sub, "pin"):
                at = find(p, "at")
                out.append({
                    "num": str(find(p, "number")[1]),
                    "name": str(find(p, "name")[1]),
                    "x": float(at[1]), "y": float(at[2]), "a": float(at[3]),
                    "type": p[1],
                })
        return out

    def units(self, lib_id):
        s = self.get(lib_id)
        return sorted({int(sub[1].rsplit("_", 2)[1]) for sub in find_all(s, "symbol")} - {0}) or [1]

    def prop(self, lib_id, name):
        for p in find_all(self.get(lib_id), "property"):
            if p[1] == name:
                return p
        return None


def _prop(name, value, x, y, hide=False, justify=None):
    return ["property", Q(name), Q(value), ["at", x, y, 0], effects(justify, hide)]


def _pin(ptype, x, y, angle, name, num, length=2.54):
    return ["pin", ptype, "line", ["at", x, y, angle], ["length", length],
            ["name", Q(name), copy.deepcopy(FONT)],
            ["number", Q(num), copy.deepcopy(FONT)]]


def box_symbol(name, prefix, left, right, footprint="", datasheet="", description=""):
    """Rectangular IC symbol. left/right: lists of (number, name, type) or None for a gap."""
    rows = max(len(left), len(right))
    longest = lambda side: max([len(p[1]) for p in side if p] or [0])
    width = max(10.16, math.ceil(((longest(left) + longest(right)) * 1.1 + 5) / 5.08) * 5.08)
    half_w = width / 2
    top = math.ceil(rows / 2) * 2.54
    bottom = top - (rows + 1) * 2.54
    body = ["symbol", Q(name + "_0_1"),
            ["rectangle", ["start", -half_w, top], ["end", half_w, bottom],
             ["stroke", ["width", 0.254], ["type", "default"]],
             ["fill", ["type", "background"]]]]
    pins = ["symbol", Q(name + "_1_1")]
    for side, x, angle in ((left, -half_w - 2.54, 0), (right, half_w + 2.54, 180)):
        for i, p in enumerate(side):
            if p:
                pins.append(_pin(p[2], x, top - 2.54 * (i + 1), angle, p[1], p[0]))
    return ["symbol", Q(name),
            ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"],
            _prop("Reference", prefix, -half_w, top + 1.27, justify="left"),
            _prop("Value", name, -half_w, bottom - 1.27, justify="left"),
            _prop("Footprint", footprint, 0, 0, hide=True),
            _prop("Datasheet", datasheet, 0, 0, hide=True),
            _prop("Description", description, 0, 0, hide=True),
            body, pins]


def power_symbol(lib, net):
    """Power symbol for a net, cloned from KiCad's GND or +5V symbol."""
    base = "GND" if net.startswith("GND") else "+5V"
    s = copy.deepcopy(lib.get("power:" + base))
    s[1] = Q(net)
    for sub in find_all(s, "symbol"):
        sub[1] = Q(net + sub[1][len(base):])
        for p in find_all(sub, "pin"):
            find(p, "name")[1] = Q(net)
    for p in find_all(s, "property"):
        if p[1] == "Value":
            p[2] = Q(net)
        if p[1] == "Description":
            p[2] = Q("Power symbol, net " + net)
    return s


# ---------------------------------------------------------------- sheets

def rot(vx, vy, r):
    """Library vector (y up) to schematic vector (y down) for symbol rotation r."""
    c, s = round(math.cos(math.radians(r))), round(math.sin(math.radians(r)))
    return vx * c - vy * s, -(vx * s + vy * c)


class Project:
    def __init__(self, name, lib, power_nets):
        self.name = name
        self.lib = lib
        self.power_nets = set(power_nets)
        self.sheets = []
        self.refs = {}
        self.intent = {}
        self.power_syms = []
        self.root_uuid = uid(name, "root")

    def sheet(self, file, title):
        s = Sheet(self, file, title)
        self.sheets.append(s)
        return s

    def next_ref(self, prefix):
        self.refs[prefix] = self.refs.get(prefix, 0) + 1
        return prefix + str(self.refs[prefix])

    def write(self, out_dir, title, rev):
        used = {}
        for s in self.sheets:
            for net in {a[0] for a in s.attach}:
                used.setdefault(net, set()).add(s.file)
        global_nets = {n for n, f in used.items() if len(f) > 1}
        for i, s in enumerate(self.sheets):
            path = os.path.join(out_dir, s.file)
            open(path, "w", encoding="utf-8").write(
                dump(s.build(global_nets, title, rev, i + 2)) + "\n")
        root = ["kicad_sch", ["version", 20250114], ["generator", Q("eeschema")],
                ["generator_version", Q("9.0")], ["uuid", self.root_uuid], ["paper", Q("A4")],
                ["title_block", ["title", Q(title)], ["rev", Q(rev)]],
                ["lib_symbols"]]
        for i, s in enumerate(self.sheets):
            x, y = 25.4 + 50.8 * (i % 4), 38.1 + 38.1 * (i // 4)
            root.append(["sheet", ["at", x, y], ["size", 40.64, 20.32],
                         ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"], ["dnp", "no"],
                         ["stroke", ["width", 0.1524], ["type", "solid"]],
                         ["fill", ["color", 0, 0, 0, 0.0]],
                         ["uuid", s.sheet_uuid],
                         ["property", Q("Sheetname"), Q(s.title), ["at", x, y - 0.7, 0], effects("left bottom")],
                         ["property", Q("Sheetfile"), Q(s.file), ["at", x, y + 20.9, 0], effects("left top")],
                         ["instances", ["project", Q(self.name),
                                        ["path", Q("/" + self.root_uuid), ["page", Q(str(i + 2))]]]]])
        root.append(["sheet_instances", ["path", Q("/"), ["page", Q("1")]]])
        root.append(["embedded_fonts", "no"])
        open(os.path.join(out_dir, self.name + ".kicad_sch"), "w", encoding="utf-8").write(dump(root) + "\n")


def write_library(path, lib, lib_ids):
    tree = ["kicad_symbol_lib", ["version", 20251024], ["generator", Q("schgen")],
            ["generator_version", Q("10.0")]]
    for lib_id in lib_ids:
        s = copy.deepcopy(lib.get(lib_id))
        tree.append(s)
    open(path, "w", encoding="utf-8").write(dump(tree) + "\n")


class Sheet:
    def __init__(self, project, file, title):
        self.p = project
        self.file = file
        self.title = title
        self.sheet_uuid = uid(project.name, "sheet", file)
        self.items = []
        self.attach = []      # (net, x, y, outward dx, outward dy)
        self.used_syms = {}
        self.texts = []
        self.n = 0

    def _id(self, kind):
        self.n += 1
        return uid(self.p.name, self.file, kind, self.n)

    def _instance(self, lib_id, x, y, r, unit, ref, value, footprint, fields=None, hide_ref=False, value_at=None):
        lib = self.p.lib
        self.used_syms[lib_id] = True
        sym = ["symbol", ["lib_id", Q(lib_id)], ["at", x, y, r], ["unit", unit],
               ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"], ["dnp", "no"],
               ["uuid", self._id("sym")]]
        defaults = {"Reference": ref, "Value": value, "Footprint": footprint}
        for pname in ("Reference", "Value", "Footprint", "Datasheet", "Description"):
            lp = lib.prop(lib_id, pname)
            at = find(lp, "at") if lp else ["at", 0, 0, 0]
            dx, dy = rot(float(at[1]), float(at[2]), r)
            val = defaults.get(pname)
            if val is None:
                val = str(lp[2]) if lp else ""
            hidden = pname in ("Footprint", "Datasheet", "Description") or (pname == "Reference" and hide_ref)
            just = None
            if lp:
                j = find(find(lp, "effects"), "justify")
                if j and r == 0:
                    just = " ".join(j[1:])
            ang = float(at[3]) if r == 0 else 0
            if r in (90, 270) and pname in ("Reference", "Value"):
                # stored angle 90 on a symbol rotated 90 displays horizontally
                shift = 3.3 + 0.55 * len(val)
                dx, dy, ang = shift, (-1.27 if pname == "Reference" else 1.27), 90
            if value_at and pname == "Value":
                dx, dy = value_at[0] - x, value_at[1] - y
                ang = 90 if r in (90, 270) else 0
                just = None
            sym.append(["property", Q(pname), Q(val), ["at", x + dx, y + dy, ang], effects(just, hidden)])
        for k, v in (fields or {}).items():
            sym.append(["property", Q(k), Q(v), ["at", x, y, 0], effects(None, True)])
        for pin in lib.pins(lib_id, unit):
            sym.append(["pin", Q(pin["num"]), ["uuid", self._id("pin")]])
        sym.append(["instances", ["project", Q(self.p.name),
                                  ["path", Q("/" + self.p.root_uuid + "/" + self.sheet_uuid),
                                   ["reference", Q(ref)], ["unit", unit]]]])
        self.items.append(sym)

    def part(self, lib_id, prefix, at, nets, value=None, footprint=None, r=0, unit=1, ref=None, fields=None):
        """Place a symbol. nets maps pin number or pin name to a net name ("NC" = no connect)."""
        lib = self.p.lib
        ref = ref or self.p.next_ref(prefix)
        x, y = at
        self._instance(lib_id, x, y, r, unit, ref, value, footprint, fields)
        pins = lib.pins(lib_id, unit)
        seen = set()
        for pin in pins:
            net = nets.get(pin["num"], nets.get(pin["name"]))
            if net is None:
                raise ValueError("%s %s: pin %s (%s) has no net" % (ref, lib_id, pin["num"], pin["name"]))
            seen.update(k for k in (pin["num"], pin["name"]) if k in nets)
            self.p.intent[(ref, pin["num"])] = net
            dx, dy = rot(pin["x"], pin["y"], r)
            ox, oy = rot(-math.cos(math.radians(pin["a"])), -math.sin(math.radians(pin["a"])), r)
            self.attach.append((net, x + dx, y + dy, round(ox), round(oy)))
        extra = set(nets) - seen
        if extra:
            raise ValueError("%s %s: unknown pins %s" % (ref, lib_id, sorted(extra)))
        return ref

    def flag(self, net, at):
        """PWR_FLAG on a net, to tell ERC the net is driven."""
        x, y = at
        self._instance("power:PWR_FLAG", x, y, 0, 1, self.p.next_ref("#FLG"), "PWR_FLAG", "", hide_ref=True)
        self.attach.append((net, x, y, 1, 0))

    def text(self, s, at):
        self.texts.append(["text", Q(s), ["exclude_from_sim", "no"], ["at", at[0], at[1], 0],
                           effects("left bottom"), ["uuid", self._id("text")]])

    def build(self, global_nets, title, rev, page):
        lib = self.p.lib
        body = []
        pwr_n = 0
        for net, x, y, ox, oy in self.attach:
            if net == "NC":
                body.append(["no_connect", ["at", x, y], ["uuid", self._id("nc")]])
                continue
            ex, ey = x + ox * STUB, y + oy * STUB
            body.append(["wire", ["pts", ["xy", x, y], ["xy", ex, ey]],
                         ["stroke", ["width", 0], ["type", "default"]], ["uuid", self._id("wire")]])
            if net in self.p.power_nets and oy:
                lib_id = "home_plc:" + net
                if lib_id not in lib.cache:
                    lib.add_custom(lib_id, power_symbol(lib, net))
                    self.p.power_syms.append(lib_id)
                pwr_n += 1
                gnd = net.startswith("GND")
                pr = ({(0, 1): 0, (1, 0): 90, (0, -1): 180, (-1, 0): 270} if gnd else
                      {(0, -1): 0, (-1, 0): 90, (0, 1): 180, (1, 0): 270})[(ox, oy)]
                reach = 4.4
                self._instance(lib_id, ex, ey, pr, 1, self.p.next_ref("#PWR"), net, "",
                               hide_ref=True, value_at=(ex + ox * reach, ey + oy * reach))
                continue
            angle = {(1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270}[(ox, oy)]
            right = angle in (180, 270)
            if True:  # flat design: every label is global, so label boxes line up on 2.54 mm pin rows
                body.append(["global_label", Q(net), ["shape", "bidirectional"], ["at", ex, ey, angle],
                             effects("right" if right else "left"), ["uuid", self._id("glabel")],
                             ["property", Q("Intersheetrefs"), Q("${INTERSHEET_REFS}"), ["at", 0, 0, 0],
                              effects(None, True)]])
            else:
                body.append(["label", Q(net), ["at", ex, ey, angle],
                             effects("right bottom" if right else "left bottom"), ["uuid", self._id("label")]])
        libsyms = ["lib_symbols"]
        for lib_id in self.used_syms:
            s = copy.deepcopy(lib.get(lib_id))
            s[1] = Q(lib_id)
            libsyms.append(s)
        return (["kicad_sch", ["version", 20250114], ["generator", Q("eeschema")],
                 ["generator_version", Q("9.0")], ["uuid", uid(self.p.name, "file", self.file)],
                 ["paper", Q("A3")],
                 ["title_block", ["title", Q(title + ": " + self.title)], ["rev", Q(rev)]],
                 libsyms] + body + self.items + self.texts +
                [["sheet_instances", ["path", Q("/"), ["page", Q(str(page))]]], ["embedded_fonts", "no"]])

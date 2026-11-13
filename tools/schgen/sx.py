"""Minimal S-expression reader/writer for KiCad files."""


class Q(str):
    """A quoted string atom."""


def parse(text):
    pos = 0
    n = len(text)
    stack = [[]]
    while pos < n:
        c = text[pos]
        if c in " \t\r\n":
            pos += 1
        elif c == "(":
            new = []
            stack[-1].append(new)
            stack.append(new)
            pos += 1
        elif c == ")":
            stack.pop()
            pos += 1
        elif c == '"':
            pos += 1
            out = []
            while text[pos] != '"':
                if text[pos] == "\\":
                    out.append(text[pos:pos + 2])
                    pos += 2
                else:
                    out.append(text[pos])
                    pos += 1
            pos += 1
            stack[-1].append(Q("".join(out)))
        else:
            start = pos
            while pos < n and text[pos] not in " \t\r\n()":
                pos += 1
            stack[-1].append(text[start:pos])
    return stack[0][0]


def _atom(a):
    if isinstance(a, Q):
        return '"' + a + '"'
    if isinstance(a, float):
        s = ("%.4f" % a).rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s
    return str(a)


def dump(node, depth=0):
    if not isinstance(node, list):
        return _atom(node)
    if all(not isinstance(c, list) for c in node):
        return "(" + " ".join(_atom(c) for c in node) + ")"
    tab = "\t" * (depth + 1)
    parts = ["(" + _atom(node[0])]
    inline = True
    for c in node[1:]:
        if isinstance(c, list):
            inline = False
            parts.append("\n" + tab + dump(c, depth + 1))
        elif inline:
            parts.append(" " + _atom(c))
        else:
            parts.append("\n" + tab + _atom(c))
    parts.append("\n" + "\t" * depth + ")")
    return "".join(parts)


def find(node, head):
    for c in node:
        if isinstance(c, list) and c and c[0] == head:
            return c
    return None


def find_all(node, head):
    return [c for c in node if isinstance(c, list) and c and c[0] == head]

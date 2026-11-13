"""Compare a KiCad netlist export with the intent file written by the generator."""
import json
import sys

from sx import parse, find, find_all

net_file, intent_file = sys.argv[1:3]
tree = parse(open(net_file, encoding="utf-8").read())
actual = {}
for net in find_all(find(tree, "nets"), "net"):
    name = str(find(net, "name")[1]).rsplit("/", 1)[-1]
    for node in find_all(net, "node"):
        actual["%s.%s" % (find(node, "ref")[1], find(node, "pin")[1])] = name
intent = json.load(open(intent_file))
bad = 0
for pin, net in sorted(intent.items()):
    got = actual.get(pin)
    if net == "NC":
        ok = got is None or got.startswith("unconnected-")
    else:
        ok = got == net
    if not ok:
        bad += 1
        print("MISMATCH %s: want %s, got %s" % (pin, net, got))
extra = set(actual) - set(intent)
print("pins checked: %d, mismatches: %d, pins not in intent: %d" % (len(intent), bad, len(extra)))
sys.exit(1 if bad or extra else 0)

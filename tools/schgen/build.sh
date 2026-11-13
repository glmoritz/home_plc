#!/bin/sh
# Regenerate the io-board schematic, convert it to the KiCad 10 format and check it.
# Needs: KICAD_CLI     command that runs KiCad 10's kicad-cli
#        KICAD_SYMBOL_DIR  KiCad 10 symbol folder (the one holding *.kicad_symdir)
set -e
: "${KICAD_CLI:=$HOME/bin/kicad-10.0.5-x86_64.AppImage kicad-cli}"
: "${KICAD_SYMBOL_DIR:?set KICAD_SYMBOL_DIR to the KiCad 10 symbols folder}"
export KICAD_SYMBOL_DIR
here=$(cd "$(dirname "$0")" && pwd)
board="$here/../../io-board"
tmp=$(mktemp -d)
python3 "$here/io_board.py"
for f in "$board"/*.kicad_sch; do $KICAD_CLI sch upgrade --force "$f" >/dev/null; done
$KICAD_CLI sch export netlist "$board/io-board.kicad_sch" -o "$tmp/io.net" >/dev/null
python3 "$here/check_netlist.py" "$tmp/io.net" "$here/io_board.intent.json"
$KICAD_CLI sch erc "$board/io-board.kicad_sch" --severity-all -o "$tmp/erc.rpt" >/dev/null || true
grep -E '^\[' "$tmp/erc.rpt" | sed 's/:.*//' | sort | uniq -c
rm -rf "$tmp"

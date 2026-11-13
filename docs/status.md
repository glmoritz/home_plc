# Where we stopped

Last updated 2026-11-13. This is the hand-over note for the next session.

## Done

- Architecture: I/O board at the bottom, one of two CPU boards on top, expansion modules beside it. See the [README](../README.md).
- Interface specs: [stacking connector](stacking-connector.md), [expansion bus](expansion-bus.md), [CPU pin budget](pin-budget.md).
- I/O board schematic, six of seven sheets, in `io-board/`:

| Sheet | Contents |
|---|---|
| `power` | 24 V input protection, field 5 V buck and 3.3 V LDO, isolated 5 V module, CPU-side 3.3 V LDO |
| `barrier` | Stacking connector, 3 × ISO7741, chip-select decoder, expansion bus drive and connector |
| `digital_in` | MAX22190, 8 inputs with MELF resistor, TVS and LED each |
| `digital_out` | 74HC595 latch, TLC555 heartbeat watchdog, 8 commanded-state LEDs |
| `output_drivers` | 2 × IPS4140HQ for 8 outputs, load supply (2L+) with reverse-polarity protection |
| `analog` | 2 × 4–20 mA in (ADS1118), 1 × 4–20 mA out (MCP4921 + XTR111), 2.5 V reference |

The schematic has 186 parts. A KiCad 10 netlist export matches the generator's description on all 621 pins.

## Not done

1. **RS-485 sheet** (CA-IS2092W, SM712, termination, 3 terminals). It is the last I/O board sheet. The three RS485 nets on the stacking connector end nowhere until it exists.
2. **Footprints that do not exist yet**: IPS4140HQ (QFN48L 8×6), URB2405YMD-6WR3 (1 × 1 inch DIP), the field terminals, the Y-capacitor.
3. **CPU-C6 and CPU-P4 schematics**: empty projects.
4. **PCB layout** of all three boards, and the case.
5. **BOM update** against the LCSC brief (see "Changes from the brief").

## How the schematic is built

`tools/schgen/io_board.py` describes the circuit; `tools/schgen/build.sh` regenerates the sheets, converts them to KiCad 10 format, exports a netlist and compares every pin with the description.

```sh
# KiCad 10 symbol folder: mount the AppImage (--appimage-mount) and use <mount>/share/kicad/symbols
KICAD_SYMBOL_DIR=<path> tools/schgen/build.sh
```

Edit the script, not the `.kicad_sch` files: a rebuild overwrites hand edits.

ERC state: no unconnected pins. Expected findings are three unconnected RS-485 labels, one tri-state/output warning on MISO (the ADS1118 output is high-impedance when not selected; KiCad's symbol types it as a plain output), and "library not configured" warnings from the command-line tool.

## Changes from the brief

- **8 digital outputs**, not 4: a second IPS4140HQ. Outputs have their own load-supply terminals (2L+, 2M).
- **2 analog inputs**, not 1, on the same ADS1118.
- **100 Ω shunts**, not 250 Ω: at 3.3 V the ADC cannot take the 5 V a 250 Ω shunt gives at 20 mA.
- **TLC555**, not NE555: the NE555 does not run from 3.3 V. The watchdog is edge-triggered.
- **Three ISO7741**, not two, for the third address line and spares.
- **No MISO buffer, no 74HC165**: the base devices release MISO themselves.
- **Added**: LM4040 2.5 V reference for the DAC, a 74LVC2G34 bus buffer, two 74LVC1G04 inverters, an expansion connector.
- **More TVS diodes**: 21 SMBJ33CA instead of 15.

## Terminals

31 positions at 5.08 mm, which sets the board width near the 100 mm limit.

| Edge | Terminals | Positions | Length |
|---|---|---:|---:|
| Top | Power (L+, M, FE), DI1–8 + 1M, analog (AI1, M, AI2, M, AO, M) | 18 | 91 mm |
| Bottom | DO1–8 + 2L+ + 2M, RS-485 (A, B, common) | 13 | 66 mm |

The bottom edge keeps about 30 mm free for the Ethernet cable from the P4 module. This split is a proposal; it is not in the schematic, which has one connector per function.

## Open items

- **To confirm with you**: the terminal split above, and that 0.6 A per output is enough (the IPS4140HQ-1 gives 1.0 A in the same footprint).
- **Values still TBD**: both fuse ratings, the three P-MOSFET parts, the buck inductor (18 µH from TI's table).
- **To verify before layout**:
  - URB2405YMD-6WR3 pinout for the LCSC brand (taken from the Mornsun datasheet).
  - MAX22190 exposed-pad size (3.1 mm assumed).
  - ESP-Hosted default pins on the P4 (GPIO14–19, 54 assumed).
  - The DevKitC-1 5V pin and USB power path.
- **Firmware rules created by the hardware**:
  - Write the output latch before starting the heartbeat.
  - Heartbeat 1 kHz nominal, at least 100 Hz.
  - The analog output is disabled while the watchdog is not running.
- **Not checked**: power budget of the 6 W isolated supply against P4 + Ethernet + C6 + GPS, and the P4's ability to timestamp GPS PPS against its Ethernet clock.

## Next steps, in order

1. RS-485 sheet, then draw the four missing footprints.
2. CPU-C6 schematic (simplest, and enough to bring up the I/O board), then CPU-P4.
3. Fix the board outline and stacking-header position shared by all three boards, then lay out the I/O board.

# Where we stopped

Last updated 2026-11-16. This is the hand-over note for the next session.

## Done

- Architecture: I/O board at the bottom, one of two CPU boards on top, expansion modules beside it. See the [README](../README.md).
- Interface specs: [stacking connector](stacking-connector.md), [expansion bus](expansion-bus.md), [CPU pin budget](pin-budget.md).
- I/O board schematic, six of seven sheets, in `io-board/`:

| Sheet | Contents |
|---|---|
| `power` | 24 V input protection, field 5 V buck and 3.3 V LDO, isolated 5 V module, CPU-side 3.3 V LDO |
| `barrier` | Stacking connector, 3 × ISO7741, chip-select decoder, expansion bus drive and connector |
| `digital_in` | MAX22190, 8 inputs with MELF resistor, TVS and LED each; ISO1212 fast path for DI1/DI2 |
| `digital_out` | 74HC595 latch, TLC555 heartbeat watchdog, 8 commanded-state LEDs |
| `output_drivers` | 2 × IPS4140HQ for 8 outputs, load supply (2L+) with reverse-polarity protection |
| `analog` | 2 universal inputs (ADS124S08: 4–20 mA, thermocouple, 2/3-wire Pt100/Pt1000), cold-junction NTC, L+ monitor, 1 × 4–20 mA out (MCP4921 + XTR111), 2.5 V reference |

The schematic has 224 parts. A KiCad 10 netlist export matches the generator's description on all 737 pins.

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

ERC state: no unconnected pins. Expected findings are three unconnected RS-485 labels and "library not configured" warnings from the command-line tool.

## Changes from the brief

- **8 digital outputs**, not 4: a second IPS4140HQ. Outputs have their own load-supply terminals (2L+, 2M).
- **2 universal analog inputs**, not 1 × 4–20 mA, on an **ADS124S08** instead of the ADS1118. See "Analog inputs" below.
- **100 Ω shunts**, not 250 Ω: 24 mA gives 2.4 V, inside the ADC's 2.5 V reference.
- **Fast inputs**: an ISO1212 on DI1/DI2 feeds IO_FAST1/2 on stacking pins 19/20 (the former spare isolator pins).
- **TLC555**, not NE555: the NE555 does not run from 3.3 V. The watchdog is edge-triggered.
- **Three ISO7741**, not two, for the third address line and spares.
- **No MISO buffer, no 74HC165**: the base devices release MISO themselves.
- **Added**: LM4040 2.5 V reference for the DAC, a 74LVC2G34 bus buffer, two 74LVC1G04 inverters, an expansion connector.
- **More TVS diodes**: 21 SMBJ33CA instead of 15.

## Terminals

31 positions at 5.08 mm, which sets the board width near the 100 mm limit.

| Edge | Terminals | Positions | Length |
|---|---|---:|---:|
| Top | Power (L+, M, FE), DI1–8 + 1M, analog in (AI1 A B C, AI2 A B C) | 18 | 91 mm |
| Bottom | DO1–8 + 2L+ + 2M, RS-485 (A, B, common), AO + M | 15 | 76 mm |

The bottom edge keeps about 24 mm free for the Ethernet cable from the P4 module (30 mm before AO moved there). The two C terminals are the same net. This split is a proposal; it is not in the schematic, which has one connector per function.

## Analog inputs

Each channel has three terminals, A, B and C. A 4-way DIP switch puts each channel in 4–20 mA mode (switches 1+2 for AI1, 3+4 for AI2).

| Mode | Wiring | DIP | ADC setup |
|---|---|---|---|
| 4–20 mA | + to A, − to B | ON | Shunt sense (AIN4/AIN5) vs AINCOM, PGA bypassed, internal 2.5 V reference |
| Thermocouple | + to A, − to B | OFF | A sense − B sense, VBIAS on B sense (AIN1/AIN3), gain 32, internal reference; CJC from the NTC on AIN6 |
| RTD 3-wire | single lead to A, the pair to B and C | OFF | IDAC1 on A excitation, IDAC2 on B excitation, 250 µA each; A sense − B sense; reference REFP0/REFN0 across RREF (1.62 kΩ), REFP buffer on; gain 8 (Pt100) or 1 (Pt1000) |
| RTD 2-wire | A and B, bridge B–C at the terminals | OFF | As 3-wire; lead resistance is not cancelled |

- Excitation and sense run on separate pins (4.99 kΩ and 10 kΩ to the terminal), so the protection resistors carry no current in the measured path.
- AVDD is +5V_F through 10 Ω for IDAC headroom; worst case on an excitation pin is about 3.5 V (Pt1000, 850 °C) against a 4.6 V limit.
- 24 V on a sense or excitation terminal is limited to 2.4 mA and 4.8 mA by the series resistors and goes into the ADC's clamp diodes. 24 V on C is limited by the 1 kΩ in series with RREF.
- Firmware cannot read the DIP switch. The channel mode in the configuration must match it.
- AIN7 measures L+ (2.5 V = 33 V): a supply diagnostic.

## Open items

- **To confirm with you**: the terminal split above, and that 0.6 A per output is enough (the IPS4140HQ-1 gives 1.0 A in the same footprint).
- **Values still TBD**: both fuse ratings, the three P-MOSFET parts, the buck inductor (18 µH from TI's table).
- **Retentive data**: no FRAM for now. When the CPU boards are drawn, pick an RTC with battery-backed SRAM (for example MCP7940N, 64 bytes). SRAM has no write limit, so firmware can copy retentive counters to it every scan without a power-fail warning.
- **To verify before layout**:
  - URB2405YMD-6WR3 pinout for the LCSC brand (taken from the Mornsun datasheet).
  - MAX22190 exposed-pad size (3.1 mm assumed).
  - ESP-Hosted default pins on the P4 (GPIO14–19, 54 assumed), and a second GPIO for IO_FAST2 (see the pin budget).
  - Fault current into ADC_AVDD: with several analog terminals at 24 V, up to about 30 mA flows into ADC_AVDD through the ADC's clamp diodes. The +5V_F loads must absorb it, or ADC_AVDD needs a clamp.
  - **Layout**: put the NTC TH1 on the copper of the analog terminal block (it is the cold junction), and keep the ADS124S08 and the input RC filters away from the buck converter and output drivers. ISO1212 SUB1/SUB2 each go to their own small floating copper island.
  - The DevKitC-1 5V pin and USB power path.
- **Firmware rules created by the hardware**:
  - Write the output latch before starting the heartbeat.
  - Heartbeat 1 kHz nominal, at least 100 Hz.
  - The analog output is disabled while the watchdog is not running.
  - Analog channel mode must match the DIP switch. Allow settling after switching IDACs or VBIAS between channels.
- **Not checked**: power budget of the 6 W isolated supply against P4 + Ethernet + C6 + GPS, and the P4's ability to timestamp GPS PPS against its Ethernet clock.

## Next steps, in order

1. RS-485 sheet, then draw the four missing footprints.
2. CPU-C6 schematic (simplest, and enough to bring up the I/O board), then CPU-P4.
3. Fix the board outline and stacking-header position shared by all three boards, then lay out the I/O board.

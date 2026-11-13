# home_plc

A small 24 V PLC in the Siemens S7-1200 style: an I/O board at the bottom and a CPU board stacked on top, for DIN-rail mounting in a cabinet. KiCad 10.

## Boards

| Folder | Board | Contents |
|---|---|---|
| `io-board/` | IO-24 | 24 V field side: 8 DI, 4 DO, 2 × 4–20 mA in, 1 × 4–20 mA out, isolated RS-485, output watchdog, expansion connector, and the whole isolation barrier |
| `cpu-c6/` | CPU-C6 | ESP32-C6-DevKitC-1 socket, RTC, RUN/ERR LEDs and RUN/STOP switch on an I2C expander |
| `cpu-p4/` | CPU-P4 | Waveshare ESP32-P4-ETH-M socket, ESP32-C6-DevKitC-1 socket (Wi-Fi coprocessor), RTC, optional GPS breakout header (UART + PPS), RUN/ERR LEDs and RUN/STOP switch on an I2C expander |

Either CPU board plugs onto the I/O board through one connector: see [docs/stacking-connector.md](docs/stacking-connector.md).
Expansion modules chain from the side of the I/O board: see [docs/expansion-bus.md](docs/expansion-bus.md).
GPIO use on both CPU boards: [docs/pin-budget.md](docs/pin-budget.md).

## Other folders

- `lib/`: symbols and footprints shared by the three projects
- `tools/schgen/`: the I/O board schematic is generated from `io_board.py`; `build.sh` regenerates it, converts it to KiCad 10 format and checks every pin against the description. Edit the script, not the schematic, until this note is removed
- `case/`: enclosure
- `docs/`: specs, the LCSC sourcing brief, datasheets

## Target envelope

Case about 90 mm wide, 110 mm tall, 60 mm deep. No PCB may exceed 100 mm in either direction.

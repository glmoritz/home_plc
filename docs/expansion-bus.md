# Expansion bus (J_EXP)

Status: **draft**.

Expansion modules sit beside the PLC on the DIN rail and chain from the side of the I/O board with a short ribbon cable.
The bus is the field-side SPI bus, after the isolation barrier, so a module needs no isolators and no microcontroller: a shift register or an SPI chip is enough.
Modules are in the same isolation group as the base I/O.

For remote I/O at a distance, use the RS-485 port (Modbus RTU) instead.

## How addressing works

- A third address line (IO_A2) makes the field-side 74HC138 produce 8 chip selects. Addresses 0–3 stay on the I/O board; 4–7 go to J_EXP as CS_A to CS_D.
- A module uses CS_A (and CS_B if it needs two) and passes the remaining selects to its output connector shifted down: with one select used, CS_B → CS_A, CS_C → CS_B, CS_D → CS_C.
- So modules address themselves by position, with no DIP switches. Limit: 4 chip selects in total across the chain.
- Each module drives MISO through a tri-state buffer enabled by its own chip select, as the base I/O does.

## Connector

2×7, 2.54 mm shrouded box header on the I/O board edge; IDC ribbon to the module. Each module has one input and one output header.

| Pin | Signal | Pin | Signal |
|----:|--------|----:|--------|
| 1 | +24V_EXP | 2 | +24V_EXP |
| 3 | GND_F | 4 | GND_F |
| 5 | EXP_SCK | 6 | GND_F |
| 7 | EXP_MOSI | 8 | EXP_MISO |
| 9 | CS_A | 10 | CS_B |
| 11 | CS_C | 12 | CS_D |
| 13 | OUT_EN | 14 | FAULT# |

## Signal notes

- **+24V_EXP**: field 24 V through its own resettable fuse, for module logic only. Budget to be set; ribbon conductors carry about 1 A each. A module that switches loads takes its load supply from its own terminals.
- **Logic level**: 3.3 V. Each module makes its own 3.3 V from +24V_EXP.
- **EXP_SCK, EXP_MOSI**: buffered copies of the field-side bus, with 33 Ω in series, so a fault on the ribbon cannot stall the base I/O.
- **EXP_MISO**: joins the base MISO through 330 Ω, so a stuck expansion line cannot override a base device.
- **CS_A–CS_D**: active low, driven by the decoder, idle high. In the schematic they are EXP_CS_A_N to EXP_CS_D_N, and FAULT# is FAULT_N.
- **OUT_EN**: output of the heartbeat watchdog. High means the CPU is alive. Every module with outputs must turn them off when OUT_EN is low.
- **FAULT#**: open-drain, wired-OR across modules, feeds the base IO_FAULT.

## Effect on the I/O board

- Three ISO7741 instead of two: 9 channels CPU → field (7 used), 3 channels field → CPU (2 used).
- IO_A2 on stacking connector pin 18.
- One bus buffer for EXP_SCK / EXP_MOSI, series resistors, one fuse, the 2×7 header.
- FAULT# is inverted on the field side before the isolator, so IO_FAULT is active high.

## Open

- +24V_EXP fuse rating.
- Maximum SPI clock with a full chain; expect about 1 MHz.
- Which edge of the I/O board carries J_EXP, and the matching case opening.

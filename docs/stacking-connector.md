# Stacking connector (J_STACK)

Status: **draft**. Freeze before any board layout starts; all three boards depend on it.

The one electrical interface between the I/O board and a CPU board.
Everything on it is at CPU potential. The isolation barrier is entirely on the I/O board.

- Connector: 2×10, 2.54 mm. Pin header on top of `io-board`, socket on the underside of the CPU board.
- Logic level: 3.3 V. The I/O board has its own CPU-side 3.3 V LDO for the isolators; no 3.3 V crosses the connector.
- The socket sits on the underside of the CPU board, so its footprint is mirrored there. Check pin 1 on both boards before layout.

## Pinout

Direction is seen from the CPU board.

| Pin | Signal | Dir | Pin | Signal | Dir |
|----:|--------|-----|----:|--------|-----|
| 1 | +5V_ISO | in | 2 | +5V_ISO | in |
| 3 | GND | – | 4 | GND | – |
| 5 | IO_SCK | out | 6 | GND | – |
| 7 | IO_MOSI | out | 8 | IO_MISO | in |
| 9 | IO_A0 | out | 10 | IO_A1 | out |
| 11 | IO_EN | out | 12 | IO_HEARTBEAT | out |
| 13 | IO_FAULT | in | 14 | GND | – |
| 15 | RS485_TX | out | 16 | RS485_RX | in |
| 17 | RS485_DE | out | 18 | IO_A2 | out |
| 19 | SPARE1 | – | 20 | SPARE2 | – |

## Signal notes

- **+5V_ISO**: output of the isolated 24 V → 5 V module on the I/O board (6 W). Powers the CPU modules. Each CPU board must stop USB 5 V and +5V_ISO from back-feeding each other.
- **IO_A0, IO_A1, IO_A2**: chip-select address for the field-side 74HC138. Addresses 0–3 are on the I/O board (DI, DO latch, ADC, DAC); addresses 4–7 go to the expansion connector, see [expansion-bus.md](expansion-bus.md).
- **IO_EN**: enables the chip-select decoder and the outputs. Pulled down on the I/O board, so with no CPU board fitted all outputs are off.
- **IO_HEARTBEAT**: square wave from the CPU. If it stops, the 555 missing-pulse timer on the field side turns all digital outputs off and releases the heater contactor.
- **IO_FAULT**: combined field-side fault. Polarity and drive type to be set in the schematic.
- **RS485_TX / RX / DE**: logic side of the isolated RS-485 transceiver.
- **SPARE1, SPARE2**: not connected. The third ISO7741 leaves two spare channels CPU → field and one field → CPU on the I/O board if these are needed later.

## Open

- IO_FAULT polarity.
- Heartbeat frequency and timeout.
- Whether +5V_ISO needs a third pin once the P4 + C6 consumption is measured.

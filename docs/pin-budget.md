# CPU board pin budget

Status: **draft**, checked against the module documents on 2026-11-13.
Exact GPIO-to-signal assignment inside each pool is left to layout.

Sources:
- Waveshare ESP32-P4-ETH schematic and pinout: <https://files.waveshare.com/wiki/ESP32-P4-ETH/ESP32-P4-ETH-datasheet.pdf>, <https://www.waveshare.com/wiki/ESP32-P4-ETH>
- ESP32-C6-DevKitC-1 v1.2 user guide and dimension drawing: <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/user_guide.html>, <https://dl.espressif.com/dl/schematics/esp32-c6-devkitc-1-dimensions_v1.2.pdf>

## Signals each CPU board must provide

| Group | Signals | Count |
|---|---|---:|
| Stacking connector | IO_SCK, IO_MOSI, IO_MISO, IO_A0, IO_A1, IO_A2, IO_EN, IO_HEARTBEAT, IO_FAULT, RS485_TX, RS485_RX, RS485_DE | 12 |
| I2C | SDA, SCL: RTC and front-panel expander | 2 |
| GPS (CPU-P4 only) | GPS_TX, GPS_RX, GPS_PPS | 3 |
| Wi-Fi coprocessor link (CPU-P4 only) | SDIO CLK, CMD, D0–D3, C6 reset | 7 |

The RUN LED, ERR LED and RUN/STOP switch sit on an I2C expander on both boards, so they use no GPIO.

## CPU-P4: Waveshare ESP32-P4-ETH-M

The 2×20 header exposes 27 GPIOs. The USB-C port goes to a CH343 UART bridge on GPIO37/38, which are not on the header.

| Use | GPIOs | Count |
|---|---|---:|
| SDIO to the C6 | 14 (D0), 15 (D1), 16 (D2), 17 (D3), 18 (CLK), 19 (CMD), 54 (C6 reset) | 7 |
| I2C | 7 (SDA), 8 (SCL); shared with the module's ES8311 codec at 0x18 | 2 |
| Stacking connector + GPS | 15 from the pool: 2, 3, 4, 5, 6, 20, 21, 22, 23, 26, 27, 32, 33, 46, 47, 48 | 15 |
| Spare | 1 left in the pool, plus 24 and 25 | 3 |

- Keep GPIO24/25 free: they are the P4's USB serial/JTAG pins, useful for debugging.
- The SDIO pin set (14–19, 54) is the one I recall Espressif using for ESP-Hosted on its own P4 board. Confirm against the ESP-Hosted P4 defaults before layout.
- C6 side of the SDIO link: GPIO18 (CMD), 19 (CLK), 20–23 (D0–D3), RST. Add pull-ups on CMD and D0–D3.

### Power

Header pin 39 (VSYS) is the module's 5 V rail after its own Schottky (D2); pin 40 (VBUS) is the USB side of that diode.
Feed +5V_ISO into **VSYS**. USB and +5V_ISO then cannot back-feed each other through the module, and no extra diode is needed for the P4.

## CPU-C6: ESP32-C6-DevKitC-1 as the only CPU

The two 1×16 headers expose 23 GPIOs.

| Use | GPIOs | Count |
|---|---|---:|
| Stacking connector + I2C | all 14 of the pool: 0, 1, 2, 3, 6, 7, 10, 11, 18, 19, 20, 21, 22, 23 | 14 |
| Spare | none without using a strapping pin | 0 |
| Avoid: strapping | 4, 5, 8, 9, 15 (8 also drives the on-board RGB LED) | 5 |
| Avoid: USB | 12, 13 | 2 |
| Avoid: console UART | 16, 17 | 2 |

### Power

The user guide calls the USB ports and the 5V pin mutually exclusive supplies. Open: read the DevKitC schematic for the diode between USB VBUS and the 5V pin. Until then, plan a Schottky from +5V_ISO to each C6 5V pin.

## Module dimensions

| Module | Board | Header rows | Connectors |
|---|---|---|---|
| ESP32-P4-ETH | 78 × 21 mm | 2×20, 17.78 mm apart | RJ45 at one end (22.3 mm long), USB-C at the opposite end |
| ESP32-C6-DevKitC-1 | 51.8 × 25.4 mm, plus 6.35 mm antenna overhang | 2×16, 22.86 mm apart | Two USB-C at the end opposite the antenna |

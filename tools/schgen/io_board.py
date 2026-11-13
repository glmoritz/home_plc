"""IO-24 board schematic. Run: KICAD_SYMBOL_DIR=<KiCad 10 symbols> python3 io_board.py"""
import json
import os

from schgen import Library, Project, box_symbol, write_library

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")

R0805 = "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder"
C0805 = "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder"
C1206 = "Capacitor_SMD:C_1206_3216Metric_Pad1.33x1.80mm_HandSolder"
F1812 = "Fuse:Fuse_1812_4532Metric_Pad1.30x3.40mm_HandSolder"
LED0805 = "LED_SMD:LED_0805_2012Metric_Pad1.15x1.40mm_HandSolder"

POWER_NETS = ["+24V_F", "+5V_F", "+3V3_F", "GND_F", "+5V_ISO", "+3V3_C", "GND_C"]

lib = Library()

lib.add_custom("home_plc:ISO7741DW", box_symbol(
    "ISO7741DW", "U",
    [("1", "VCC1", "power_in"), ("3", "INA", "input"), ("4", "INB", "input"), ("5", "INC", "input"),
     ("6", "OUTD", "output"), ("7", "EN1", "input"), ("2", "GND1", "power_in"), ("8", "GND1", "power_in")],
    [("16", "VCC2", "power_in"), ("14", "OUTA", "output"), ("13", "OUTB", "output"), ("12", "OUTC", "output"),
     ("11", "IND", "input"), ("10", "EN2", "input"), ("15", "GND2", "power_in"), ("9", "GND2", "power_in")],
    footprint="Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm",
    datasheet="https://www.ti.com/lit/ds/symlink/iso7741.pdf",
    description="Quad digital isolator, 3 forward / 1 reverse, default output high, SOIC-16W"))

lib.add_custom("home_plc:TPS560430XDBV", box_symbol(
    "TPS560430XDBV", "U",
    [("5", "VIN", "power_in"), ("4", "EN", "input"), None, ("2", "GND", "power_in")],
    [("1", "CB", "passive"), ("6", "SW", "output"), None, ("3", "FB", "input")],
    footprint="Package_TO_SOT_SMD:SOT-23-6",
    datasheet="https://www.ti.com/lit/ds/symlink/tps560430.pdf",
    description="Buck converter, 4-36 V in, 600 mA, 1.1 MHz, adjustable, SOT-23-6"))

lib.add_custom("home_plc:URB2405YMD-6WR3", box_symbol(
    "URB2405YMD-6WR3", "PS",
    [("2", "Vin", "power_in"), None, ("1", "GND", "power_in")],
    [("3", "+Vo", "power_out"), None, ("5", "0V", "power_out")],
    footprint="",
    datasheet="https://kyohritsu.com/eclib/OTHER/CATALOG/MORNSUN/urbymd6wr3.pdf",
    description="Isolated DC-DC, 9-36 V in, 5 V 1.2 A out, 6 W, 1500 VDC isolation, 1 x 1 inch DIP"))

lib.add_custom("home_plc:MAX22190ATJ", box_symbol(
    "MAX22190ATJ", "U",
    [("1", "IN1", "input"), ("3", "IN2", "input"), ("5", "IN3", "input"), ("7", "IN4", "input"),
     ("18", "IN5", "input"), ("20", "IN6", "input"), ("22", "IN7", "input"), ("24", "IN8", "input"), None,
     ("2", "LED1", "output"), ("4", "LED2", "output"), ("6", "LED3", "output"), ("8", "LED4", "output"),
     ("17", "LED5", "output"), ("19", "LED6", "output"), ("21", "LED7", "output"), ("23", "LED8", "output")],
    [("30", "VDD24", "power_in"), ("31", "VDD", "power_out"), ("16", "VL", "power_in"), None,
     ("10", "SCLK", "input"), ("11", "SDI", "input"), ("13", "SDO", "tri_state"), ("9", "~{CS}", "input"),
     ("12", "LATCH", "input"), ("14", "~{FAULT}", "open_collector"), ("15", "~{READY}", "open_collector"),
     ("28", "M0", "input"), ("29", "M1", "input"), ("27", "REFDI", "passive"), ("26", "REFWB", "passive"),
     ("25", "GND", "power_in"), ("32", "GND", "power_in"), ("33", "GND", "power_in")],
    footprint="Package_DFN_QFN:TQFN-32-1EP_5x5mm_P0.5mm_EP3.1x3.1mm",
    datasheet="https://www.analog.com/media/en/technical-documentation/data-sheets/MAX22190.pdf",
    description="Octal 24 V digital input, IEC 61131-2 Type 1/3, SPI, TQFN-32. Pin 33 is the exposed pad"))

lib.add_custom("home_plc:IPS4140HQ", box_symbol(
    "IPS4140HQ", "U",
    [("49", "VCC", "power_in"), None, ("13", "IN1", "input"), ("15", "IN2", "input"), ("19", "IN3", "input"),
     ("21", "IN4", "input"), None, ("14", "~{STAT1}", "open_collector"), ("16", "~{STAT2}", "open_collector"),
     ("18", "~{STAT3}", "open_collector"), ("20", "~{STAT4}", "open_collector"), None, ("17", "GND", "power_in")],
    [("45", "OUT1", "output"), ("46", "OUT1", "passive"), ("47", "OUT1", "passive"),
     ("42", "OUT2", "output"), ("43", "OUT2", "passive"), ("44", "OUT2", "passive"),
     ("39", "OUT3", "output"), ("40", "OUT3", "passive"), ("41", "OUT3", "passive"),
     ("36", "OUT4", "output"), ("37", "OUT4", "passive"), ("38", "OUT4", "passive")],
    footprint="",
    datasheet="https://www.st.com/resource/en/datasheet/ips4140hq.pdf",
    description="Quad 24 V high-side switch, 0.6 A per channel, QFN48L 8x6. Pin 49 is the tab (VCC). "
                "Pins 1-12, 22-35 and 48 are not connected and not drawn"))

CUSTOM = ["home_plc:ISO7741DW", "home_plc:TPS560430XDBV", "home_plc:URB2405YMD-6WR3",
          "home_plc:MAX22190ATJ", "home_plc:IPS4140HQ"]

prj = Project("io-board", lib, POWER_NETS)


def two_pin(sheet, lib_id, prefix, at, a, b, value, fp, r=0):
    return sheet.part(lib_id, prefix, at, {"1": a, "2": b}, value=value, footprint=fp, r=r)


def R(sheet, at, value, a, b):
    return two_pin(sheet, "Device:R", "R", at, a, b, value, R0805)


def C(sheet, at, value, a, b, fp=C0805):
    return two_pin(sheet, "Device:C", "C", at, a, b, value, fp)


# ------------------------------------------------------------------ power
s = prj.sheet("power.kicad_sch", "Power")
Y1, Y2, Y3 = 60.96, 132.08, 203.2

s.text("24 V input: fuse, TVS, reverse-polarity P-MOSFET", (25.4, Y1 - 27.94))
s.part("Connector_Generic:Conn_01x03", "J", (40.64, Y1), {"1": "+24V_IN", "2": "GND_F", "3": "FE"},
       value="24V IN (L+, M, FE)", footprint="")
two_pin(s, "Device:Polyfuse", "F", (66.04, Y1), "+24V_IN", "24V_FUSED", "PTC TBD", F1812)
two_pin(s, "Device:D_TVS", "D", (81.28, Y1), "GND_F", "24V_FUSED", "SMBJ33CA", "Diode_SMD:D_SMB_Handsoldering", r=90)
s.part("Transistor_FET:Q_PMOS_GDS", "Q", (104.14, Y1), {"G": "RP_GATE", "D": "24V_FUSED", "S": "+24V_F"},
       value="PMOS 60V TBD", footprint="Package_TO_SOT_SMD:TO-252-2")
two_pin(s, "Device:D_Zener", "D", (132.08, Y1), "+24V_F", "RP_GATE", "15V", "Diode_SMD:D_SOD-123", r=90)
R(s, (149.86, Y1), "100k", "RP_GATE", "GND_F")
two_pin(s, "Device:C_Polarized", "C", (165.1, Y1), "+24V_F", "GND_F", "100u 50V",
        "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm")
C(s, (180.34, Y1), "100n 50V", "+24V_F", "GND_F")
C(s, (200.66, Y1), "4n7 1kV", "FE", "GND_F", C1206)
R(s, (215.9, Y1), "1M", "FE", "GND_F")
s.flag("+24V_IN", (236.22, Y1 - 5.08))
s.flag("GND_F", (236.22, Y1 + 5.08))
s.flag("+24V_F", (261.62, Y1 - 5.08))
s.flag("FE", (261.62, Y1 + 5.08))

s.text("Field-side logic supply: 24 V -> 5 V buck -> 3.3 V LDO", (25.4, Y2 - 27.94))
s.part("home_plc:TPS560430XDBV", "U", (55.88, Y2),
       {"VIN": "+24V_F", "EN": "+24V_F", "GND": "GND_F", "CB": "BUCK_CB", "SW": "BUCK_SW", "FB": "BUCK_FB"})
C(s, (91.44, Y2), "2u2 50V", "+24V_F", "GND_F", C1206)
C(s, (106.68, Y2), "100n", "BUCK_CB", "BUCK_SW")
two_pin(s, "Device:L", "L", (121.92, Y2), "BUCK_SW", "+5V_F", "18u TBD", "Inductor_SMD:L_Bourns_SRN6045TA")
R(s, (137.16, Y2), "88k7 1%", "+5V_F", "BUCK_FB")
R(s, (152.4, Y2), "22k1 1%", "BUCK_FB", "GND_F")
C(s, (167.64, Y2), "22u 10V", "+5V_F", "GND_F", C1206)
s.flag("+5V_F", (182.88, Y2 - 5.08))
s.part("Regulator_Linear:AP2112K-3.3", "U", (220.98, Y2),
       {"VIN": "+5V_F", "EN": "+5V_F", "GND": "GND_F", "NC": "NC", "VOUT": "+3V3_F"})
C(s, (251.46, Y2), "1u", "+5V_F", "GND_F")
C(s, (266.7, Y2), "1u", "+3V3_F", "GND_F")
R(s, (281.94, Y2), "1k", "+3V3_F", "LED_F_A")
two_pin(s, "Device:LED", "D", (297.18, Y2), "GND_F", "LED_F_A", "green", LED0805, r=90)

s.text("CPU-side supply: isolated 24 V -> 5 V, then 3.3 V for the CPU side of the isolators", (25.4, Y3 - 27.94))
s.text("PS1: 1500 VDC isolation. Pinout from the Mornsun datasheet; confirm it for the part bought on LCSC.", (25.4, Y3 + 27.94))
s.part("home_plc:URB2405YMD-6WR3", "PS", (58.42, Y3),
       {"Vin": "+24V_F", "GND": "GND_F", "+Vo": "+5V_ISO", "0V": "GND_C"})
C(s, (99.06, Y3), "1u 50V", "+24V_F", "GND_F", C1206)
C(s, (114.3, Y3), "10u 10V", "+5V_ISO", "GND_C", C1206)
C(s, (129.54, Y3), "100n", "+5V_ISO", "GND_C")
C(s, (152.4, Y3), "1n 2kV Y", "GND_F", "GND_C", "")
s.part("Regulator_Linear:AP2112K-3.3", "U", (220.98, Y3),
       {"VIN": "+5V_ISO", "EN": "+5V_ISO", "GND": "GND_C", "NC": "NC", "VOUT": "+3V3_C"})
C(s, (251.46, Y3), "1u", "+5V_ISO", "GND_C")
C(s, (266.7, Y3), "1u", "+3V3_C", "GND_C")

# ---------------------------------------------------------------- barrier
s = prj.sheet("barrier.kicad_sch", "Isolation barrier, chip selects, expansion")
s.text("Stacking connector (CPU side)", (25.4, Y1 - 27.94))
s.part("Connector_Generic:Conn_02x10_Odd_Even", "J", (45.72, Y1), {
    "1": "+5V_ISO", "2": "+5V_ISO", "3": "GND_C", "4": "GND_C", "5": "IO_SCK", "6": "GND_C",
    "7": "IO_MOSI", "8": "IO_MISO", "9": "IO_A0", "10": "IO_A1", "11": "IO_CS_N", "12": "IO_HEARTBEAT",
    "13": "IO_FAULT", "14": "GND_C", "15": "RS485_TX", "16": "RS485_RX", "17": "RS485_DE", "18": "IO_A2",
    "19": "IO_SPARE1", "20": "IO_SPARE2"},
    value="STACK 2x10", footprint="Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical")
R(s, (30.48, Y2), "10k", "+3V3_C", "IO_CS_N")
R(s, (45.72, Y2), "10k", "IO_HEARTBEAT", "GND_C")
R(s, (60.96, Y2), "10k", "IO_SPARE1", "GND_C")

s.text("Isolators: CPU side left, field side right", (93.98, Y1 - 27.94))
ISO = "home_plc:ISO7741DW"
common = {"VCC1": "+3V3_C", "EN1": "+3V3_C", "GND1": "GND_C", "VCC2": "+3V3_F", "EN2": "+3V3_F", "GND2": "GND_F"}
s.part(ISO, "U", (116.84, Y1), dict(common, INA="IO_SCK", OUTA="F_SCK", INB="IO_MOSI", OUTB="F_MOSI",
                                    INC="IO_CS_N", OUTC="F_CS_N", IND="F_MISO", OUTD="IO_MISO"))
s.part(ISO, "U", (116.84, Y2), dict(common, INA="IO_A0", OUTA="F_A0", INB="IO_A1", OUTB="F_A1",
                                    INC="IO_A2", OUTC="F_A2", IND="F_FAULT", OUTD="IO_FAULT"))
s.part(ISO, "U", (116.84, Y3), dict(common, INA="IO_HEARTBEAT", OUTA="F_HEARTBEAT", INB="IO_SPARE1", OUTB="NC",
                                    INC="GND_C", OUTC="NC", IND="F_SPARE_IN", OUTD="IO_SPARE2"))
for y in (Y1, Y2, Y3):
    C(s, (152.4, y), "100n", "+3V3_C", "GND_C")
    C(s, (165.1, y), "100n", "+3V3_F", "GND_F")
R(s, (177.8, Y1), "100k", "F_MISO", "GND_F")
R(s, (177.8, Y3), "10k", "F_SPARE_IN", "GND_F")

s.text("Chip-select decoder: 0-3 on this board, 4-7 to expansion", (198.12, Y1 - 27.94))
s.part("74xx:74HC138", "U", (223.52, Y1), {
    "A0": "F_A0", "A1": "F_A1", "A2": "F_A2", "~{E0}": "F_CS_N", "~{E1}": "GND_F", "E2": "+3V3_F",
    "~{Y0}": "CS_DI_N", "~{Y1}": "CS_DO_N", "~{Y2}": "CS_ADC_N", "~{Y3}": "CS_DAC_N",
    "~{Y4}": "EXP_CS_A_N", "~{Y5}": "EXP_CS_B_N", "~{Y6}": "EXP_CS_C_N", "~{Y7}": "EXP_CS_D_N",
    "VCC": "+3V3_F", "GND": "GND_F"},
    value="74HC138", footprint="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm")
C(s, (259.08, Y1), "100n", "+3V3_F", "GND_F")

s.text("Expansion bus drive and fault return", (198.12, Y2 - 27.94))
BUF = "74xGxx:74LVC2G34"
u = s.part(BUF, "U", (223.52, Y2 - 10.16), {"1": "F_SCK", "6": "EXP_SCK_B"}, value="74LVC2G34",
           footprint="Package_TO_SOT_SMD:SOT-23-6")
s.part(BUF, "U", (223.52, Y2 + 10.16), {"3": "F_MOSI", "4": "EXP_MOSI_B"}, value="74LVC2G34",
       footprint="Package_TO_SOT_SMD:SOT-23-6", unit=2, ref=u)
s.part(BUF, "U", (254, Y2), {"VCC": "+3V3_F", "GND": "GND_F"}, value="74LVC2G34",
       footprint="Package_TO_SOT_SMD:SOT-23-6", unit=3, ref=u)
C(s, (269.24, Y2), "100n", "+3V3_F", "GND_F")
R(s, (284.48, Y2), "33R", "EXP_SCK_B", "EXP_SCK")
R(s, (299.72, Y2), "33R", "EXP_MOSI_B", "EXP_MOSI")
R(s, (314.96, Y2), "330R", "EXP_MISO", "F_MISO")

s.part("74xGxx:74LVC1G04", "U", (223.52, Y3), {"1": "NC", "2": "FAULT_N", "4": "F_FAULT", "GND": "GND_F", "VCC": "+3V3_F"},
       value="74LVC1G04", footprint="Package_TO_SOT_SMD:SOT-23-5")
C(s, (254, Y3), "100n", "+3V3_F", "GND_F")
R(s, (269.24, Y3), "10k", "+3V3_F", "FAULT_N")
two_pin(s, "Device:Polyfuse", "F", (289.56, Y3), "+24V_F", "+24V_EXP", "PTC TBD", F1812)

s.text("Expansion connector (field side)", (332.74, Y1 - 27.94))
s.part("Connector_Generic:Conn_02x07_Odd_Even", "J", (360.68, Y1), {
    "1": "+24V_EXP", "2": "+24V_EXP", "3": "GND_F", "4": "GND_F", "5": "EXP_SCK", "6": "GND_F",
    "7": "EXP_MOSI", "8": "EXP_MISO", "9": "EXP_CS_A_N", "10": "EXP_CS_B_N", "11": "EXP_CS_C_N",
    "12": "EXP_CS_D_N", "13": "OUT_EN", "14": "FAULT_N"},
    value="EXPANSION 2x7", footprint="Connector_IDC:IDC-Header_2x07_P2.54mm_Vertical")

SMB = "Diode_SMD:D_SMB_Handsoldering"


def tvs(sheet, at, net, gnd="GND_F"):
    return two_pin(sheet, "Device:D_TVS", "D", at, gnd, net, "SMBJ33CA", SMB, r=90)


def led(sheet, at, anode, cathode="GND_F", value="green"):
    return two_pin(sheet, "Device:LED", "D", at, cathode, anode, value, LED0805, r=90)


# ---------------------------------------------------------- digital inputs
s = prj.sheet("digital_in.kicad_sch", "Digital inputs")
YA, YB, YC, YD = 48.26, 99.06, 172.72, 248.92
s.text("8 x 24 V inputs, sinking, IEC 61131-2 Type 1/3. 1M is the input common (GND_F).", (25.4, YA - 25.4))
s.part("Connector_Generic:Conn_01x09", "J", (40.64, YA + 25.4),
       dict({str(i): "DI%d" % i for i in range(1, 9)}, **{"9": "GND_F"}),
       value="DI1-8, 1M", footprint="")
for i in range(1, 9):
    x = 73.66 + (i - 1) * 22.86
    two_pin(s, "Device:R", "R", (x, YA), "DI%d" % i, "DI_IN%d" % i, "1k5 MELF", "Resistor_SMD:R_MiniMELF_MMA-0204")
    tvs(s, (x, YB), "DI%d" % i)
    led(s, (200.66 + (i - 1) * 15.24, YC), "DI_LED%d" % i)
s.text("Input state LEDs, driven by the MAX22190 from the input current", (198.12, YC - 25.4))
nets = {"VDD24": "+24V_F", "VDD": "DI_VDD", "VL": "+3V3_F", "SCLK": "F_SCK", "SDI": "F_MOSI", "SDO": "F_MISO",
        "~{CS}": "CS_DI_N", "LATCH": "+3V3_F", "~{FAULT}": "FAULT_N", "~{READY}": "NC",
        "M0": "GND_F", "M1": "GND_F", "REFDI": "DI_REFDI", "REFWB": "DI_REFWB", "GND": "GND_F"}
for i in range(1, 9):
    nets["IN%d" % i] = "DI_IN%d" % i
    nets["LED%d" % i] = "DI_LED%d" % i
s.part("home_plc:MAX22190ATJ", "U", (93.98, YC), nets)
s.text("M1:M0 = 00: 24-bit SPI frames with CRC. LATCH tied high: inputs latch on CS.", (25.4, YC + 35.56))
R(s, (33.02, YD), "7k5 1%", "DI_REFDI", "GND_F")
R(s, (48.26, YD), "24k 1%", "DI_REFWB", "GND_F")
C(s, (63.5, YD), "1u 50V", "+24V_F", "GND_F", C1206)
C(s, (78.74, YD), "100n 50V", "+24V_F", "GND_F")
C(s, (93.98, YD), "1u", "DI_VDD", "GND_F")
C(s, (109.22, YD), "100n", "DI_VDD", "GND_F")
C(s, (124.46, YD), "100n", "+3V3_F", "GND_F")

# --------------------------------------------------------- digital outputs
N_DO = 8
s = prj.sheet("digital_out.kicad_sch", "Output latch and watchdog")
s.text("Output latch. Outputs are high-Z until the watchdog sees the heartbeat (OUT_EN high).", (25.4, Y1 - 30.48))
s.part("74xx:74HC595", "U", (55.88, Y1), {
    "SER": "F_MOSI", "SRCLK": "F_SCK", "RCLK": "CS_DO_N", "~{SRCLR}": "+3V3_F", "~{OE}": "DO_OE_N",
    "QA": "DO_Q1", "QB": "DO_Q2", "QC": "DO_Q3", "QD": "DO_Q4", "QE": "DO_Q5", "QF": "DO_Q6", "QG": "DO_Q7",
    "QH": "DO_Q8", "QH'": "NC", "VCC": "+3V3_F", "GND": "GND_F"},
    value="74HC595", footprint="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm")
C(s, (91.44, Y1), "100n", "+3V3_F", "GND_F")
s.part("74xGxx:74LVC1G04", "U", (129.54, Y1), {"1": "NC", "2": "OUT_EN", "4": "DO_OE_N", "GND": "GND_F", "VCC": "+3V3_F"},
       value="74LVC1G04", footprint="Package_TO_SOT_SMD:SOT-23-5")
C(s, (160.02, Y1), "100n", "+3V3_F", "GND_F")

s.text("Heartbeat watchdog. Only edges on F_HEARTBEAT retrigger it, so a line stuck high or low times out "
       "(about 0.1 s) and OUT_EN goes low.", (25.4, Y2 - 30.48))
C(s, (33.02, Y2), "10n", "F_HEARTBEAT", "WD_TRIG")
R(s, (48.26, Y2), "10k", "+3V3_F", "WD_TRIG")
two_pin(s, "Device:D_Schottky", "D", (63.5, Y2), "+3V3_F", "WD_TRIG", "BAT54", "Diode_SMD:D_SOD-123", r=90)
R(s, (81.28, Y2), "4k7", "WD_TRIG", "WD_BASE")
s.part("Transistor_BJT:MMBT3906", "Q", (101.6, Y2), {"B": "WD_BASE", "E": "WD_CAP", "C": "GND_F"})
R(s, (121.92, Y2), "1M", "+3V3_F", "WD_CAP")
C(s, (137.16, Y2), "100n", "WD_CAP", "GND_F")
s.part("Timer:TLC555xD", "U", (172.72, Y2), {
    "TRIG": "WD_TRIG", "THRES": "WD_CAP", "DISCH": "WD_CAP", "~{RST}": "+3V3_F", "CONT": "WD_CV",
    "OUT": "OUT_EN", "VCC": "+3V3_F", "GND": "GND_F"})
C(s, (208.28, Y2), "10n", "WD_CV", "GND_F")
C(s, (223.52, Y2), "100n", "+3V3_F", "GND_F")
R(s, (243.84, Y2), "1k", "OUT_EN", "WD_LED")
led(s, (259.08, Y2), "WD_LED", value="green OUT EN")

s.text("Commanded-state LEDs", (25.4, Y3 - 30.48))
for i in range(1, N_DO + 1):
    x = 33.02 + (i - 1) * 30.48
    R(s, (x, Y3), "1k", "DO_Q%d" % i, "DO_LED%d" % i)
    led(s, (x + 12.7, Y3), "DO_LED%d" % i, value="yellow")

# ---------------------------------------------------------- output drivers
s = prj.sheet("output_drivers.kicad_sch", "Output drivers")
s.text("8 x 24 V high-side outputs, 0.6 A each. 2L+ is the load supply, 2M its return (GND_F).", (25.4, Y1 - 35.56))
s.part("Connector_Generic:Conn_01x10", "J", (38.1, Y1),
       dict({str(i): "DO%d" % i for i in range(1, 9)}, **{"9": "24V_DO_IN", "10": "GND_F"}),
       value="DO1-8, 2L+, 2M", footprint="")
s.part("Transistor_FET:Q_PMOS_GDS", "Q", (71.12, Y1), {"G": "DO_RP_GATE", "D": "24V_DO_IN", "S": "+24V_DO"},
       value="PMOS 60V 10A TBD", footprint="Package_TO_SOT_SMD:TO-252-2")
two_pin(s, "Device:D_Zener", "D", (96.52, Y1), "+24V_DO", "DO_RP_GATE", "15V", "Diode_SMD:D_SOD-123", r=90)
R(s, (114.3, Y1), "100k", "DO_RP_GATE", "GND_F")
tvs(s, (129.54, Y1), "+24V_DO")
two_pin(s, "Device:C_Polarized", "C", (149.86, Y1), "+24V_DO", "GND_F", "100u 50V",
        "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm")
C(s, (165.1, Y1), "100n 50V", "+24V_DO", "GND_F")
C(s, (180.34, Y1), "100n 50V", "+24V_DO", "GND_F")
s.flag("+24V_DO", (203.2, Y1 - 5.08))
s.flag("24V_DO_IN", (203.2, Y1 + 5.08))
for chip, y in ((0, Y2), (1, Y3)):
    nets = {"VCC": "+24V_DO", "GND": "GND_F"}
    for k in range(1, 5):
        i = chip * 4 + k
        nets["IN%d" % k] = "DO_Q%d" % i
        nets["~{STAT%d}" % k] = "FAULT_N"
        nets["OUT%d" % k] = "DO%d" % i
        R(s, (104.14 + (k - 1) * 15.24, y), "47k", "DO_Q%d" % i, "GND_F")
        x = 175.26 + (k - 1) * 27.94
        tvs(s, (x, y), "DO%d" % i)
        C(s, (x + 15.24, y), "10n 50V", "DO%d" % i, "GND_F")
    s.part("home_plc:IPS4140HQ", "U", (60.96, y + 5.08), nets)

# ------------------------------------------------------------------ analog
R1206 = "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder"
s = prj.sheet("analog.kicad_sch", "Analog inputs and output")
s.text("2 x 4-20 mA inputs: 100R shunt to GND_F, so 20 mA = 2.0 V at the ADC. "
       "Terminals: AI1, M, AI2, M, AO, M.", (25.4, Y1 - 30.48))
s.part("Connector_Generic:Conn_01x06", "J", (38.1, Y1),
       {"1": "AI1", "2": "GND_F", "3": "AI2", "4": "GND_F", "5": "AO", "6": "GND_F"},
       value="AI1, M, AI2, M, AO, M", footprint="")
for n in (1, 2):
    x = 66.04 + (n - 1) * 121.92
    ai, sh, adc = "AI%d" % n, "AI%d_SH" % n, "ADC_CH%d" % n
    two_pin(s, "Device:Polyfuse", "F", (x, Y1), ai, sh, "PTC 50mA", F1812)
    two_pin(s, "Device:R", "R", (x + 15.24, Y1), sh, "GND_F", "100R 0.1%", R1206)
    tvs(s, (x + 30.48, Y1), ai)
    R(s, (x + 50.8, Y1), "4k7", sh, adc)
    C(s, (x + 66.04, Y1), "100n", adc, "GND_F")
    s.part("Diode:BAT54S", "D", (x + 88.9, Y1), {"A": "GND_F", "K": "+3V3_F", "COM": adc})

s.text("ADC, 2.5 V reference and DAC", (25.4, Y2 - 30.48))
s.part("Analog_ADC:ADS1118IDGS", "U", (60.96, Y2), {
    "SCLK": "F_SCK", "~{CS}": "CS_ADC_N", "DIN": "F_MOSI", "DOUT/~{DRDY}": "F_MISO",
    "AIN0": "ADC_CH1", "AIN1": "ADC_CH2", "AIN2": "GND_F", "AIN3": "GND_F", "VDD": "+3V3_F", "GND": "GND_F"},
    footprint="Package_SO:MSOP-10_3x3mm_P0.5mm")
C(s, (99.06, Y2), "100n", "+3V3_F", "GND_F")
R(s, (119.38, Y2), "680R", "+3V3_F", "VREF_2V5")
s.part("Reference_Voltage:LM4040DBZ-2.5", "U", (142.24, Y2), {"K": "VREF_2V5", "A": "GND_F", "NC": "NC"})
C(s, (165.1, Y2), "100n", "VREF_2V5", "GND_F")
s.part("Analog_DAC:MCP4921-ESN", "U", (213.36, Y2), {
    "VDD": "+3V3_F", "~{CS}": "CS_DAC_N", "SCK": "F_SCK", "SDI": "F_MOSI", "~{LDAC}": "GND_F",
    "VrefA": "VREF_2V5", "AVSS": "GND_F", "VoutA": "DAC_OUT"},
    footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm")
C(s, (251.46, Y2), "100n", "+3V3_F", "GND_F")
R(s, (266.7, Y2), "1k", "DAC_OUT", "AO_VIN")

s.text("4-20 mA output: Iout = 10 x Vin / 1k, so 2.0 V = 20 mA. OD is high (output off) while the watchdog "
       "has no heartbeat.", (25.4, Y3 - 30.48))
R(s, (33.02, Y3), "10R", "+24V_F", "AO_VSP")
C(s, (48.26, Y3), "100n 50V", "AO_VSP", "GND_F")
s.flag("AO_VSP", (33.02, Y3 + 25.4))
s.part("Interface_CurrentLoop:XTR111AxDGQ", "U", (93.98, Y3), {
    "VSP": "AO_VSP", "IS": "AO_IS", "VG": "AO_VG", "REGS": "AO_REG", "REGF": "AO_REG", "VIN": "AO_VIN",
    "SET": "AO_SET", "~{EF}": "NC", "OD": "DO_OE_N", "GND": "GND_F"},
    value="XTR111AIDGQ")
C(s, (132.08, Y3), "470n", "AO_REG", "GND_F")
two_pin(s, "Device:R", "R", (147.32, Y3), "AO_SET", "GND_F", "1k 0.1%", R0805)
s.part("Transistor_FET:Q_PMOS_GDS", "Q", (175.26, Y3), {"G": "AO_VG", "S": "AO_IS", "D": "AO_DRAIN"},
       value="PMOS 60V TBD", footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2")
two_pin(s, "Device:D_Schottky", "D", (203.2, Y3), "AO", "AO_DRAIN", "SS16", "Diode_SMD:D_SMA_Handsoldering", r=90)
tvs(s, (223.52, Y3), "AO")
C(s, (243.84, Y3), "10n 50V", "AO", "GND_F")

out = os.path.join(ROOT, "io-board")
prj.write(out, "home_plc IO-24", "0.1")
write_library(os.path.join(ROOT, "lib", "home_plc.kicad_sym"), lib, CUSTOM + prj.power_syms)
json.dump({"%s.%s" % k: v for k, v in prj.intent.items()},
          open(os.path.join(HERE, "io_board.intent.json"), "w"), indent=0, sort_keys=True)
print("sheets:", [x.file for x in prj.sheets],
      "parts:", sum(v for k, v in prj.refs.items() if not k.startswith("#")))

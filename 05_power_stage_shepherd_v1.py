import SchemDraw
# short introduction: https://schemdraw.readthedocs.io/en/latest/usage/placement.html

import SchemDraw.elements as elm  # electrical (Resistor, Capacitor, Diode, Opamp, Dot)
from SchemDraw import dsp  # https://schemdraw.readthedocs.io/en/latest/elements/dsp.html
import matplotlib.pyplot as plt
#plt.xkcd()

# MPPT
sch_mppt = SchemDraw.Drawing(unit=1, fontsize=10)
prt_sw_mppt = sch_mppt.add(elm.SwitchDpdt(reversed=True))
mppt_pins = [elm.IcPin(name="V_BQ", pin=1, side="left"),
            elm.IcPin(name="VOC", pin=2, side="left"),
            elm.IcPin(name="VREF", pin=3, side="left"),
            elm.IcPin(name="VBAT", pin=4, side="right"),
            elm.IcPin(name="VSTOR", pin=5, side="right")]
mppt = elm.Ic(pins=mppt_pins, botlabel="Conv_MPPT", anchor="VREF")
sig_vref_samp = sch_mppt.add(dsp.Arrow(label="VREF_SAMP", xy=prt_sw_mppt.p1))
prt_mppt = sch_mppt.add(mppt)
sig_voc_samp = sch_mppt.add(dsp.Arrow(label="VOC_SAMP", xy=prt_sw_mppt.p2, tox=prt_mppt.VOC))

# V_EMU_I
sch_i_emu = SchemDraw.Drawing(unit=1, fontsize=10)
sig_spi_i = sch_i_emu.add(dsp.Arrow("right", lftlabel="SPI", l=sch_i_emu.unit / 2))
prt_dac_emu_i = sch_i_emu.add(dsp.DAC(label="DAC"))
sig_v_emu_i = sch_i_emu.add(dsp.Arrow("right", toplabel="V_EMU_I"))
prt_sub_emu_i = sch_i_emu.add(dsp.Circle(label="SUB-"))
sig_v_bias_i = sch_i_emu.add(dsp.Arrow("right", label="V_EMU_I_Biased"))
prt_v2i_v = sch_i_emu.add(dsp.Circle(label="V2I"))
sig_v_in_sht_p1 = sch_i_emu.add(dsp.Arrow("right"))
jct_v_in_sht_p = sch_i_emu.add(dsp.Dot(label="V_IN_SHT+"))

# V_EMU_V
sch_v_emu = SchemDraw.Drawing(unit=1, fontsize=10)
sig_spi_v = sch_v_emu.add(dsp.Arrow("right", lftlabel="SPI", l=sch_i_emu.unit / 2))
prt_dac_v_emu = sch_v_emu.add(dsp.DAC(label="DAC"))
sig_vi_emu = sch_v_emu.add(dsp.Arrow("right", toplabel="V_EMU_V", tox=prt_sw_mppt.t1))

# VCREF buffered
sch_vcref = SchemDraw.Drawing(unit=1, fontsize=10)
prt_cap_vc = sch_vcref.add(elm.Capacitor())
sig_vcref = sch_vcref.add(dsp.Arrow("right", label="VCREF", tox=prt_sw_mppt.t2))

# P_HARVEST - Connector
sch_harv = SchemDraw.Drawing(unit=1, fontsize=10)
prt_p_harv = sch_harv.add(elm.connectors.Header(label="P_Harv", rows=2, cols=1, ))
sig_voc_vc = sch_harv.add(dsp.Arrow(label="VOC_VD", xy=prt_p_harv.p1, tox=prt_sw_mppt.t4))
sig_v_h = sch_harv.add(dsp.Arrow(label="V_H", xy=prt_p_harv.p2))
prt_sw_vh = sch_harv.add(elm.Switch(label="SW"))
sig_v_in_sht_p2 = sch_harv.add(dsp.Arrow("down", tox=jct_v_in_sht_p.center))


# V_CONST for Target
sch_v_const = SchemDraw.Drawing(unit=1, fontsize=10)
sch_v_const.add(dsp.Arrow("right", lftlabel="I2C", l=sch_i_emu.unit / 2))
sch_v_const.add(dsp.DAC(label="DAC"))
sch_v_const.add(dsp.Arrow("right", toplabel="V_C1"))
sch_v_const.add(dsp.Circle(label="LDO"))
sch_v_const.add(dsp.Arrow("right", label="V_C2"))
prt_ldo_v = sch_v_const.add(elm.Switch(label="SW"))
sch_v_const.add(dsp.Arrow("right"))
sch_v_const.add(dsp.Dot(label="V_LD_SHT+"))


'''


sig_v_in_sht_p2 = sch_i_emu.add(dsp.Arrow("right"))



prt_sw_v = sch_i_emu.add(dsp.Square(label="Switch"))
sig_v_harv_0 = sch_i_emu.add(dsp.Line("right"))
jct_v_harv = sch_i_emu.add(dsp.Dot(), label="V_H")

sig_v_harv_1 = sch_i_emu.add(dsp.Arrow("right"))


sig_voc_vd = sch_i_emu.add(dsp.Arrow("right", label="VOC_VD"))

# ...

sig_v_harv_2 = sch_i_emu.add(dsp.Line("down"), xy=jct_v_harv.end)
sig_v_harv_3 = sch_i_emu.add(dsp.Arrow("right"))

prt_shunt_in = sch_i_emu.add(dsp.Square(label="Shunt"))
sig_v_in_sht_m0 = sch_i_emu.add(dsp.Line(label="V_in_sht"))
jct_v_in_sht_m = sch_i_emu.add(dsp.Dot())
sig_v_in_sht_m1 = sch_i_emu.add(dsp.Arrow())

# ...

sig_v_in_sht_m2 = sch_i_emu.add(dsp.Arrow("down", xy=jct_v_in_sht_m.center))
prt_buf_vin = sch_i_emu.add(dsp.Square(label="BUF"))
sig_v_vin = sch_i_emu.add(dsp.Arrow("down"))
prt_adc_vin = sch_i_emu.add(dsp.Adc(label="ADC", lftlabel="SPI"))

# modifiers parts: to=part.start, d="down", anchor="in1" (for Opamps), at=part.out (connect to a specific port of part)
# modifiers lines: tox=C.start
# push(), pop(), will get back to saved position

#SW_VOC =

# Adc,
'''

sch_mppt.save("05_power_stage_shepherd_v1.png")

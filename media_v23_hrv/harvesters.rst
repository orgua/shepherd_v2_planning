Harvester Frontend
===================

Test of various harvesting algorithms with a solar cell

- solar cell: IXYS SM101K09L
- lighting by philips LED 9W 806 lm, 50 Hz
- harvesting Profiles in detail_
- Plots show
    - a general overview while the lighting was moved
    - an area with low light
    - an area with bright light and eventually a detailed shot of the measurement
- interesting findings
    - voc: setpoint of 76 % in low-light seems off -> is the VOC wrong?
    - voc & iv: opening the circuit lets the voltage rise significantly above VOC (especially in low light scenario) and it takes time to stabilize
    - voc: jumping to setpoint lets the power increase for a short time in bright light (hidden capacitor?)
    - iv: sawtooth-ramp is highly non-linear in the cross-section coming from VOC (1000 Hz, bright light detail)
    - iv: current measurement is delayed for a timeslot (obvious in scenario "1000 Hz bright light detail" @ 0V
    - all: detail-shots show a 5 kHz and 50 kHz resonance
    - iv open input: voltage seems to follow despite no driving source

.. _detail: https://github.com/orgua/shepherd//blob/master/software/python-package/shepherd/virtual_harvester_defs.yml

MPPT VOC
--------

- setpoint 76 %
- 100 ms intervall with 1.2 ms VOC-measurement


.. image:: ./media_v23_hrv/hrv_mppt_voc_overview.png
.. image:: ./media_v23_hrv/hrv_mppt_voc_lowlight.png
.. image:: ./media_v23_hrv/hrv_mppt_voc_led_light.png
.. image:: ./media_v23_hrv/hrv_mppt_voc_led_light_detail.png

MPPT PO
-------

- 6 ms intervals with visible 10 mV (minimal) step-size
- "follow the highest power-output"

.. image:: ./media_v23_hrv/hrv_mppt_po_overview.png
.. image:: ./media_v23_hrv/hrv_mppt_po_lowlight.png
.. image:: ./media_v23_hrv/hrv_mppt_po_led_light.png



IV-Curve 110 Hz
---------------

- 0 to 5 V, 909 Steps (between 50 & 60 Hz)

.. image:: ./media_v23_hrv/hrv_ivcurve110Hz_overview.png
.. image:: ./media_v23_hrv/hrv_ivcurve110Hz_lowlight.png
.. image:: ./media_v23_hrv/hrv_ivcurve110Hz_led_light.png
.. image:: ./media_v23_hrv/hrv_ivcurve110Hz_led_light_detail.png


IV-Curve 1000 Hz
---------------

- 0 to 5 V, 100 Steps

.. image:: ./media_v23_hrv/hrv_ivcurve1000Hz_overview.png
.. image:: ./media_v23_hrv/hrv_ivcurve1000Hz_lowlight.png
.. image:: ./media_v23_hrv/hrv_ivcurve1000Hz_led_light.png
.. image:: ./media_v23_hrv/hrv_ivcurve1000Hz_led_light_detail.png

IV-Curve with Open Input
------------------------

- no solar!
- 110 Hz and 1000 Hz Plots

.. image:: ./media_v23_hrv/hrv_iv110Hz_open_input.png
.. image:: ./media_v23_hrv/hrv_iv1000Hz_open_input.png

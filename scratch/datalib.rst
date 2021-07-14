
"iv_reconstruct" zeigt ein bisschen, wie ich mir das mit den transformationskoeffizienten gedacht habe.

"gen_data.py" erzeugt je ein hdf File für jeden typ von database den wir unterstützen wollen.
Dazu verwendet es unter anderem echt aufgenommene Daten ("jogging_10m.iv").

Es benutzt die zwei exemplarischen maximum powerpoint Algorithmen, die in "mppt.py" implementiert sind.

Ausführung von "gen_data" dauert ziemlich lang.
Für das MPPT (dauert am längsten) gibt es eine rudimentäre statusanzeige.

"python plot.py db_traces.h5" plottet den Inhalt des entsprechenden Files.



calibrate.py measure sheep0 -u hans -p 10241024 --smu-ip 10.0.0.41 --emulation -o sheep0_meas.yml
calibrate.py convert sheep0_meas.yml -o sheep0_cal.yml

calibrate.py write sheep0 -c sheep0_cal.yml -v 22A0 -s 2021w28i0001 -u hans -p 10241024
calibrate.py read sheep0 -u hans -p 10241024

sudo shepherd-sheep eeprom read

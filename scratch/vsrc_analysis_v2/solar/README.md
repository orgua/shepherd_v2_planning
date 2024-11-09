# IVCurves

Measured with shepherds harvester-circuit

run without hrv: 1.6623726666952912e-05


```Shell
scp jane@sheep0:/var/shepherd/recordings/LE* ./

shepherd-data extract-meta LED_003pc.h5

shepherd-data plot -s 1.7998 -e 1.8102 -m .

shepherd-data extract -s 1.80 -e 2.00 --ds-factor 1 .
# for 20 IVCurves a 1000 samples

```
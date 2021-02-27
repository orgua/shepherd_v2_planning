Level Translators
=================

Problem
-------
- voltages on B-side seemed to work fine from 2.5 V to 5V, but showed errors below,
- Nexperia LSF0108 seems to have hidden properties that are not mentioned in the datasheet
- expected behaviour: 
	- open drain on both sides when pins float / only PUs active
	- PUs bring pins to ref-voltage
	- a low on side results in a low on the opposite side

Setup
-----
- Side A has constant supply voltage of 3.3 V
- side B supply is dynamic, 0 to 5 V, but voltages below 1 V are not expected to be covered by the translator


.. image:: media/leveltranslator_schematic.png

Nexperia LSF0108
----------------
- marketed as bidirectional, multivoltage, open-drain, push-pull
- translation between "0.95 V and 1.8, 2.5, 3.3 and 5V" (room for speculation)
- unlike the TI-Versions, this IC does not have voltage constraints (like V_A has to be >= 0.8 V + V_B)
- "An and Bn pins may be exchanged" (mentioned more than once)

Measurements
------------
- V_RefA = 3v3, V_RefB = 4v5
	- both sides highZ, only PUs working -> V_A and V_B settle at 1.2 V -> UNEXPECTED, should be VRef
	- Side A tied to GND -> V_B = 0 V
	- Side A tied to 3v3 -> V_B = 3v3 -> UNEXPECTED, V_B is capped at 3v3
	- Side B tied to GND -> V_A = 0 
	- Side B tied to 4V5 -> V_A = 3 V
- V_RefA = 3v3, V_RefB = 2v0
	- both sides highZ, only PUs working -> V_A and V_B settle at 0.9 V -> UNEXPECTED, should be VRef
	- Side A tied to GND -> V_B = 0 V
	- Side A tied to 2v0 -> V_B = 1v9 -> UNEXPECTED, but ok
	- Side A tied to 3v3 -> V_B = 2v0
	- Side B tied to GND -> V_A = 0 V
	- Side B tied to 2V0 -> V_A = 1.4 V -> UNEXPECTED, still below detection threshold 
	
	

Concept - Testbed
=================

General Philosophy
    - only as complex as needed
    - most bang for the buck, not to expensive and to specialized design, hardware, etc
    - possibility to build on your own
    - unique selling point is the replay of energy (harvesting) sources and emulation of power converters with high temporal resolution

infrastructure
    - ~ 30 RF-Nodes (Beaglebone with custom RF-IC) with Ethernet-Backchannel
    - distributed on cfaed-floors, several rooms / offices, also on corridors
        - i.e. BAR II55 - II75, III50 - III80, II52 - II54, II40A-II43A (end in another dispatch-room)
        - we could use right side of ethernet-socket (largely unpatched for now)
        - Nodes should be secured by powerstrips (on the wall, under desk, ..)
    - RF stays within ETSI Norms, mainly bluetooth (Nordic nRF-Modules) or other IEEE 802.15.4 based standard
    - Nodes connected and powered via Ethernet-Backchannel, optional with PTP, QoS, POE-Support
        - preferred if Nodes are connected to one switch (in BAR II65) for low jitter for ~100 ns PTP timing-constraint
        - preferred if PoE could be controlled to shut down and reset nodes (mainly to safe energy)
    - **ZIH-Response and -Requirements**:
        - Nodes need installed fusion-inventory (to scan for vulnerabilities)
        - no QoS on Campus ("has more disadvantages")
        - POE -> Configuration-Access to Switch only when used exclusively for this vLAN
            - alternative: wake on LAN (WOL) -> no native beaglebone support (BBAI unclear, but unlikely)
        - current Switches should have very low jitter under low load, time in ASIC-Stack ~ 300 ns
            - lower latency ZIH alternative: infiniband, not applicable for us
        - we can't use the cable canal (== structural change)
        - wifi is used on channel 1, 6, 11, self managed with varying tx-power, often < 20 mW
        - nodes are allowed to use the 2.4 GHz Band without restrictions, ZIH also offers to disable Wifi on these channels either for one floor or based on a schedule (routers seem to have that option, but it is untested)
        - cisco switches offer "clean air"-Monitor-Service -> for II57 it reports 100% Quality with < 10 % non Wifi
        - ports on corridors can be used but ZIH-Infrastructure has higher priority
        - nodes may not get direct internet connection (relayed)

RF-Network-Design
    - limit to one floor
    - ring-structure (due to impenetrable II800) would be a nice novelty
    - the 3 consecutive NES-Rooms should be center of a cluster / group (something like 7 Offices with 3 Nodes each)
    - remaining network can be more sparse (1 in each office, or 1 every two)
    - there could be nodes with higher tx power and special antennas to directly link II59 and II71 (cut through II800)
    -> results in

Control-Server
    - one control-server that contains: user data, web interface, shepherd controller
    - needs linux from debian-family, python 3.7+, ansible
    - 20 - 100 GB scratch area
    - Port 80 accessible from the internet
    - manageable from the intranet
    - needs access to vLAN of RF-Nodes (mostly ssh-based)
    - **ZIH-Requirements**:
        - managed by ZIH with Centreon
        - for access from internet the server needs a security-concept -> needs to pass Greenbone Security Manager Test (GSM-Test)
        - access via subdomain, cfaed, tu-website
        - no SSH from Internet

Misc
    - Casing in laser-acrylic or off-the-shelf case with custom front
        - input Marco: open and transparent is fine
        - Case should blend in, be passive and option to use powerstrips to attach it to wall or below desk
    - dynamic roles of nodes -> config can be "static" (network access, gps attached, mobile) -> ansible-roles
    - switching to BB-AI seems to be an important step, but price increase is 3.5 fold
        - focus is still on the PRUs, now 4 Cores
        - GBE is more than welcome
        - we get a more reliable power connection (type c instead of micro-usb)
        - CPU is hopefully drastically faster
            - BBB brings 995 BogoMIPS, 277 MIPS FP, 1600 MIPS Int (numbers from internet, see 25_improve_sw_linux.rst)
            - BBAI TBD
        - documentation and community is small, underdeveloped
    - with vCap in mind, PRU would be best replaced by a teensy 4.1 (keep it simple) or same uController
        - teensy has lots of iO, SPI with DMA & FIFO, FPU, 600 MHz, 1 MB RAM
    - web-interface should make clear that users are responsible to stay within ETSI-norm, no misuse, no out-of-boundary, monitoring and logging is active
    - ssh-interface should also make clear about project, active monitoring and offer a contact-email

Administrative Info
-------------------

- ZIH offers hosting of (self provided) physical server and virtual ones
    - ZIH Server-FAQ_
    - phyServer: gets power, ethernet, USV, cooling, ...
    - vServer: prefered by ZIH, free of charge, 3-5 Days prepare -> vServer-SelfService_
    - ZIH offers Sub-Domains on Website -> SubDomain-FAQ_
- ZIH-Rules for using their infrastructure
    - central dhcp: only by IT-Admin of facility -> DHCP-FAQ_
    - network access: IT-Admin .. `FAQ <https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/bereitstellung_datennetz>`_
    - cfaed IT-Admin_
    - WIFI interference und network capability undocumented online
- Answer to inquiry, from IT / ZIH
    - we could use right side of nw-sockets (currently mostly unpatched) -> TODO: talk with the leaders of groups that occupy offices
    - vLAN and DHCP from ZIH
    - we could use the server-room in BAR
    - ZIH offers more powerful vServers than listed on website
    - distribution plan shows that patch-cables of the floor all end in the same patch-room (BAR II65 S2/S3)
        - if switches do not meet our standards we can provide our own, needs to be a supported cisco model
        - if even that does not suffice it will get a lot harder -> bringing new cable / devices into the wall is a structural change with a whole book of needed permissions
    - if LAN-Sockets do not suffice, we can use a (cisco-)switch locally in offices
    - unix-nodes should host fusion-inventory (to scan for vulnerabilities)
    - hardware > 150 € needs to be in inventory (sticker & database listing)
    - vServer gets monitored / managed with Centreon
        - for access from outside (internet) the server needs a security-concept
    - passwords and access-data should be managed with "TeamPass" -> password manager for groups
- cfaed floor-plan_

.. _Server-FAQ: https://tu-dresden.de/zih/dienste/service-katalog/zusammenarbeiten-und-forschen/server_hosting
.. _DHCP-FAQ: https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/zentrale_ip_adressverwaltung
.. _SubDomain-FAQ: https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/domains-dns/management
.. _IT-Admin: https://cfaed.tu-dresden.de/it-support
.. _vServer-SelfService: https://selfservice.zih.tu-dresden.de/l/index.php/cloud_dienste
.. _floor-plan: https://navigator.tu-dresden.de/etplan/bar/02

RF-Measurement
--------------

- sender was a nRF52840-DK Board with BLE Beacon example, 1 MBit,
    - tx power - 16 to 8 dBm, in this case 0 and 8 dBm
    - rx sensitivity is - 97 dBm
- receiver was a phone, oneplus 3T, with visualisation of rx-power,
    - rx sensitivity down to - 100 dBm
    - path loss in direct proximity was about 50 dB
- measurement-mode: determine max range while using link-budget and keeping stable connection
- results for 0 dBm
    - range was about 4 offices (horizontal) with dry-wall in between
    - was not able to get to upper floor
    - no signal through II800
- results for 8 dBm
    - range is about 7 offices (horizontal) with dry-wall in between
    - packets reached upper floor, even the adjacent office next to the direct overlying one
    - no signal through II800, not even with direct wall contact (these are massive walls, with massive metal / ventilation parts inside
- with active use of II64 / II64B / II64C it would be possible to get a U-Shaped network
- see "10_rf_measurements.ods" for protocol

.. image:: 10_concept_floor_plan_bar_2.png
    :alt: floor plan bar 2

.. image:: 10_concept_floor_plan_bar_3.png
    :alt: floor plan bar 3

Anforderungen für das ZIH
-------------------------

Projektbeschreibung Shepherd

- Prüfstand für Funknetzwerk-Algorithmen, speziell im Bereich Energy-Harvesting
- ~ 30 Funkknoten mit Netzwerk-Backchannel, Basis sind Beaglebone Einplatinenrechner mit Linux / Debian-Derivat
    - erste Testknoten sind bereits einsatzfähig
- Verteilung der Knoten auf der unteren cfaed-Etage im Barkhausen Bau
    - mehrere Räume, BAR II52 - II75
    - einige Knoten auf den Fluren, Etage 2 hat vier freie Ports
- RF Netzwerk befindet sich im 2.4 GHz ISM-Band, bleibt innerhalb der ETSI-Norm, hauptsächlich IEEE 802.15.4, beispiel Bluetooth
    - Bluetooth belegt 81x 1 MHz breite Kanäle von 2400 - 2480 MHz und benutzt Frequency-Hopping, d.h jedes Paket wird auf einem anderen Kanal gesendet, mehrere tausend Sprünge pro Sekunde
- Ethernet-Rückkanal braucht Unterstützung für GBE, PoE, wenn möglich PTP nativ im Switch
    - im Bestfall wäre PoE abschaltbar um das Netzwerk auszuschalten, da es nicht 24/7 laufen muss, oder einzelne Knoten neuzustarten
    - PTP-Anforderung: Synchronisationsabweichung < 1 us zwischen den Knoten, optimal wären 100 ns
    - Internet Zugang für Updates
    - ein eigenes vLAN für die Knoten
    - die Kommunikation zu den Knoten wird aktuell per SSH (TCP Port 22) realisiert (aber es wird noch eine temporäre Datenverbindung wie z.B. hinzukommen)
- wir sind offen für alle administrativen bzw. Sicherheits-Auflagen die notwendig sind zur Erfüllung der Anforderungen

Anforderungen

- NW-Switch in Raum II65
    - GBE (maximal benötigte Geschwindigkeit)
    - optimal ist ein dediziertes Gerät mit >= 30 Ports -> Ziel: sehr geringer Jitter bei PTP-Zeitsynchronisierung der Knoten
    - vLan-Zugriff für Knoten
    - wenn möglich Kontrolle über POE der Ports zum Energiesparen, da embedded Knoten zwar runtergefahren werden können, aber kein WOL beherrschen
- Cisco-Wifi-Router
    - das ZIH hat ein temporäres Abschalten von WLAN im 2.4 GHz Band angeboten
    - wir würden das Angebot gerne Annehmen, aktuell halten wir beispielsweise ein regelmäßiges Scheduling für Samstag / Sonntag ab sinnvollsten
    - betroffene Router
        - TODO
- vLan
    - Zugriff vom Kontroll-Server aus, SSH (TCP Port 22)
    - Internet-Zugriff der Knoten für Updates
- vServer als Kontroll- und Web-Interface
    - die engen Zeitsynchronisierungsvorgaben gelten hier nicht
    - Software die benötigt wird:  Debian Linux Derivat, python 3.7+, ansible
    - 20 - 100 GB scratch-area
    - Port 80 erreichbar aus dem Internet für Web-Interface, im Bestfall mit Sub-Domain oder eingebettet in CFAED-Seite
- zu beschaltene NW-Dosen
    - Laut Aussage vom ZIH dürften wir (mit niedrigster Priorität) ebenfalls NW-Dosen auf den Fluren benutzen
    - TODO




Comparison D-Cube
-----------------

- D-Cube-Overview_
- DBs: relational -> MariaDB, Time Series -> InfluxDB
- user interface -> Grafana
- gpio-tracing -> isolators for usb, power, bi-dir gpio (TI ISO7220M, ISO7221M, ADUM3160, NXE2)
- latency profiling -> Navspark-GL, later uBlox Neo
- power profiling -> TI LMP92064
- interference generator -> JamLab-NG
- supports binary patching
- PoE via PEM1305

.. _D-Cube-Overview: http://www.carloalbertoboano.com/documents/D-Cube_overview.pdf

Comparison Flocklab
-------------------

- 3 Targets
- Target-GPIO with resolution of 100 ns with accuracy +- 200 ns


Inventory
---------

- ~20 PoE Adapters
- 10 - 15 Beaglebone Black / green, same amount of Shepherd V1.x Capes
- ZyXEL Ethernet Switch GS1900-24HP, with PoE
- Linksys Router WRT54GL
- uBlox Neo M8T

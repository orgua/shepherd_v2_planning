Concept - Testbed
=================

- infrastructure
    - 20 - 30 RF-Nodes (Beaglebone with custom RF-IC) with Ethernet-Backchannel
    - distributed on one floor, several rooms / offices -> (BAR II55 - II75)
        - we could use right side of ethernet-socket (largely unpatched for now)
    - RF stays within ETSI Norms, mainly bluetooth
    - Nodes connected and powered via Ethernet-Backchannel, with PTP, QoS, POE-Support
        - preferred if Nodes are connected to one switch (in BAR II65) for ~100 ns timing-constraint
        - preferred if PoE could be controlled to shut down nodes, safe energy
    - ZIH-Requirements: installed fusion-inventory (to scan for vulnerabilities)
- one control-server that contains: user data, web interface, shepherd controller
    - needs linux from debian-family, python 3.7+, ansible
    - 20 - 100 GB scratch area
    - ZIH-Requirements: managed by ZIH with Centreon
    - Port 80 accessible from the internet
    - manageable from the intranet
    - needs access to vLAN of RF-Nodes (mostly ssh-based)
- Casing in laser-acrylic or off-the-shelf case with custom front


Administrative Info
-------------------

- ZIH offers hosting of (self provided) physical server and virtual ones
    - `ZIH Server FAQ <https://tu-dresden.de/zih/dienste/service-katalog/zusammenarbeiten-und-forschen/server_hosting>`_
    - phyServer: gets power, ethernet, USV, cooling, ...
    - vServer: prefered by ZIH, free of charge, 3-5 Days prepare -> `vServer via Self Service <https://selfservice.zih.tu-dresden.de/l/index.php/cloud_dienste>`_
    - ZIH offers Sub-Domains on Website -> `FAQ Sub <https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/domains-dns/management>`_
- ZIH-Rules for using their infrastructure
    - central dhcp: only by IT-Admin of facility `FAQ DHCP <https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/zentrale_ip_adressverwaltung>`_
    - network access: IT-Admin .. `FAQ <https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/bereitstellung_datennetz>`_
    - `cfaed IT-Admin <https://cfaed.tu-dresden.de/it-support>`_
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
    - passwords and access-data should be managed with "TeamPass" -> password manager for groups
- `cfaed floor-plan <https://navigator.tu-dresden.de/etplan/bar/02>`_

Anforderungen für das ZIH
-------------------------

Projektbeschreibung Shepherd
- Prüfstand für Funknetzwerk-Algorithmen, speziell im Bereich Energy-Harvesting
- 20 - 30 Funkknoten mit Netzwerk-Backchannel, Basis sind Beaglebone Einplatinenrechner mit Linux / Debian-Derivat
    - erste Testknoten sind bereits einsatzfähig
- Verteilung der Knoten auf einer Etage, mehrere Räume (CFAED, BAR II55 - II75)
    - initial wären die Räume II59, II69-II71 der Gruppe für Tests ausreichend
- RF befindet sich im ISM-Band, bleibt innerhalb der ETSI-Norm, hauptsächlich Bluetooth
- Ethernet-Rückkanal braucht Unterstützung für GBE, PoE, und wenn möglich PTP nativ im Switch, alternativ QoS
    - im Bestfall wäre PoE abschaltbar um das Netzwerk auszuschalten, da es nicht 24/7 laufen muss, oder einzelne Knoten neuzustarten
    - PTP-Anforderung: Synchronisationsabweichung < 1 us zwischen den Knoten, optimal wären 100 ns
    - Internet Zugang für Updates
    - im Bestfall eigenes vLAN für die Knoten
- Kontroll-Server in Form eines vServers
    - die engen Zeitsynchronisierungsvorgaben gelten hier nicht
    - Software die benötigt wird: python 3.7+, ansible
    - 20 - 100 GB scratch-area
    - Port 80 erreichbar aus dem Internet für Web-Interface, im Bestfall mit Sub-Domain oder eingebettet in CFAED-Seite

Anforderungen
- Info über Koexistenz-Regeln für Office-WLAN, Eduroam und anderen Uni-Systemen im ISM-Band
- möglichkeit PoE der Ports zu kontrollieren zum Stromsparen?
-
- TODO


Comparison D-Cube
-----------------

- `Overview <http://www.carloalbertoboano.com/documents/D-Cube_overview.pdf>`_
- DBs: relational -> MariaDB, Time Series -> InfluxDB
- user interface -> Grafana
- gpio-tracing -> isolators for usb, power, bi-dir gpio (ISO7220M, ISO7221M, ADUM3160, NXE2)
- latency profiling -> Navspark-GL, later uBlox Neo
- power profiling -> TI LMP92064
- interference generator -> JamLab-NG
- supports binary patching
- PoE via PEM1305

Inventory
---------

- ~20 PoE Adapters
- 10 - 15 Beaglebone Black, same amount of Shepherd V1.x Capes
- ZyXEL Ethernet Switch GS1900-24HP
- Linksys Router WRT54GL

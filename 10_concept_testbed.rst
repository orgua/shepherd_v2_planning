Concept - Testbed
=================

- infrastructure
    - 20 - 30 RF-Nodes (Beaglebone with custom RF-IC) with Ethernet-Backchannel
    - distributed on one floor, several rooms / offices -> (BAR II55 - II75)
    - RF stays within ETSI Norms, mainly bluetooth
    - Nodes connected via ETH-Backchannel, with PTP, QoS, POE-Support
- one control-server that contains: user data, web interface, shepherd controller
- TODO

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
    - we could use right side of nw-sockets (currently mostly unpatched) -> TODO: talk with the leaders of groups
    - vLAN and DHCP from ZIH
    - we could use the server-room in BAR
    - ZIH offers more powerful vServers than listed on website
    - distribution plan shows that patch-cables of the floor all end in the same patch-room (BAR II65 S2/S3)
        - if switches do not meet our standards we can provide our own, needs to be a supported cisco model
    - if LAN-Sockets do not suffice, we can use a switch (cisco) in offices
    - unix-nodes should host fusion-inventory (to scan for vulnaribilities)
    - hardware > 150 € needs to be in inventory (sticker & database listing)
    - vServer gets monitored / managed with Centreon
    - passwords and access-data should be managed with "TeamPass" -> password manager for groups
- `cfaed floor-plan <https://navigator.tu-dresden.de/etplan/bar/02>`_

Anforderungen für das ZIH
-------------------------

Projektbeschreibung
- Prüfstand für ein Funknetzwerk
- 20 - 30 Funkknoten mit Netzwerk-Backchannel, Basis sind Beaglebone Einplatinenrechner mit Linux
- Verteilung auf einer Etage, mehrere Räume, (CFAED, BAR II55 - II75)
- RF im ISM-Band, bleibt innerhalb der ETSI-Norm, hauptsächlich Bluetooth
- Ethernet-Rückkanal braucht Unterstützung für QoS, PoE, und wenn möglich PTP
- PTP-Anforderung: Synchronisationsabweichung < 1 us, optimal wären 100 ns

Anforderungen
- Info über Koexistenz-Regeln für Office-WLAN, Eduroam und anderen Uni-Systemen im ISM-Band


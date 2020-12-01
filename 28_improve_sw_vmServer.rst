VM Shepherd Server
==================

Basic Specs
-----------

    cfaed-shepherd
    Ubuntu 20.04 LTS 64 Bit, 2 Cores, 4 GB Ram
    50 GB Scrap
    IP: ....
    Connectable via VPN / LAN in TUD

TODO
----

    - mount 10 TB Storage for raw measurement data
    - prepare basic install scripts
        - auto-update, with mail to admin
        - remove clutter
        - basic software
        -

Auto-Update::

    sudo apt-get install unattended-upgrades
    sudo dpkg-reconfigure -plow unattended-upgrades
    # OR manipulate config-file
    # etc/apt/apt.conf.d/10periodic
    APT::Periodic::Update-Package-Lists "1";
    APT::Periodic::Download-Upgradeable-Packages "1";
    APT::Periodic::AutocleanInterval "7";
    APT::Periodic::Unattended-Upgrade "1";
    # etc/apt/apt.conf.d/50unattended-upgrades -> allow normal updates, uncomment:
    "${distro_id}:${distro_codename}-updates";
    Unattended-Upgrade::Mail "..";
    # ref1: https://libre-software.net/ubuntu-automatic-updates/
    # ref2: https://wiki.ubuntuusers.de/Aktualisierungen/Konfiguration/



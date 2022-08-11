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

Enable SSH-Server (manual bootstrap in vmrc, not needed in the end)::

    sudo apt install openssh-server net-tools
    sudo systemctl status sshd
    # service should be active (running)
    sudo netstat -tulpn | grep 22^
    sudo systemctl enable ssh
    # -> seems all ok on the Server itself

Adapt Firewall

- selfservice -> could service -> enterprise cloud -> vm management -> fw rules
- add vpn or your specific ip-group -> reboot VM or wait till full our for update

Gruppenlaufwerk::

    shepherdDS, 10TB
    vs-grp04.zih.tu-dresden.de
    - weekly backup to central (26 week retention)

    # info:
    https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/datenspeicher/details#section-2-3

    # sshfs-mount for Data-Gateway (seems to be the current solution)
    # https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/datenspeicher/copy_of_details
    sudo apt install sshfs
    sudo mkdir /mnt/shp_ds
    chown service /mnt/shp_ds
    # -> ./glw/shepherdDS links to /svm/vs-grp04/shepherdDS, same for ./glw_new/shepherdDS
    sshfs zihlogin@dgw.zih.tu-dresden.de:/svm/vs-grp04/shepherdDS /mnt/shp_ds/
    umount /mnt/shp_ds

    # Include account into automount:
    # V1 shitty:
    sudo apt install sshpass
    sshpass -p "your_password" scp -r backup_user@target_ip:/home/ /backup/$name

    # V2 - proposed by helpdesk - login-server and dgw share home-directory:
    ssh-keygen
    ssh-copy-id zihuser@host
    ssh-copy-id zihuser@login.zih.tu-dresden.de

    # check if key was added
    ssh zihuser@login.zih.tu-dresden.de
    nano /home/zihuser/.ssh/authorized_key

    # automount - add mount to ~/.bashrc

# V3 - even better / helpdesk-solution:
Das Laufwerk wurde ja nur mit der Standardkonfiguration SMB+NTFS beantragt, aber man könnte dafür auch nachträglich noch NFS konfigurieren und es dann direkt vom Filer an die VM-IP exportieren lassen, sodass Sie es dort nativ als NFS-Laufwerk mounten können. Authentisierung entfällt in dem Fall, da lediglich über die Export-Rule (IP-basiert) festgelegt wird, wer es mounten darf und wer nicht.
Das wäre sicherlich die direktere und sinnvollere Methode als den Umweg über den DGW zu gehen, der das Laufwerk ja auch nur über NFS bezieht.

Nachteil: Sie müssen dann etwas mit den genutzten UIDs/GIDs aufpassen, da bei NFS natürlich direkt die lokalen UIDs Ihrer VM genutzt werden und nicht mehr die des Users über den Sie es zuvor über den DGW eingebunden hatten. D.h. wenn die VM nicht gleichzeitig am LDAP hängt und Sie noch auf anderem Wege auf das Gruppenlaufwerk zugreifen wollen, sollten Sie möglichst eine IDM-UID auch auf der VM verwenden.
Das Laufwerk ist ja auch nicht mit UNIX-Permissions sondern mit NTFS konfiguriert, andernfalls funktionieren Schreibzugriffe eventuell dann auch gar nicht.

Functional Account::

    create: https://selfservice.zih.tu-dresden.de/l/index.php/login
    overview: https://selfservice.zih.tu-dresden.de/l/index.php/flogin_mgmt#

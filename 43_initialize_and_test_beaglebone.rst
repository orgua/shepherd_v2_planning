Install custom Shepherd-Code and check install, prior to release
----------------------------------------------------------------

Install on Server::

    sudo git clone https://github.com/orgua/shepherd
    cd /shepherd
    pip install --upgrade ansible
    ansible-playbook ./deploy/deploy.yml


Useful commands on a fresh system::

    sudo chown -R user /opt/shepherd
    sudo passwd user
    cp /opt/shepherd/software/meta-package/example_config_harvest.yml /etc/shepherd/config.yml
    sudo shepherd-sheep -vvv run --config /etc/shepherd/config.yml

    cd /opt/shepherd/software/python-package/
    sudo python3 setup.py test --addopts "-vv"
    # bump2version --tag patch # -> just hand in PR or hash

    # test code on live system
    sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml

    # test suite in /opt/shepherd/software/python-package
    sudo python3 setup.py test --addopts "-vv"

    # helpful when build-system was used with sudo
    sudo chown -R user ./

Check (on sheep)::

    # DT-Overlay: there should be an BB-SHPRD-... -> overlay is active
    ll /proc/device-tree/chosen/overlays/

    # Custom-Services: should show 3x shepherd entries, only shepherd-launcher.service enabled, also: shepherd-rpc, shepherd
    systemctl list-unit-files | grep shep

    # Timesync-Services: both should be active and running
    systemctl | grep ptp
    systemctl | grep phc

    # PRUs: two pru-rproc available and probed successfully
    dmesg | grep pru

    # PRUs: should show remoteproc1 and 2
    ll /sys/class/remoteproc/

    # KernelModule: it should probably be active - but isn't (sudo modprobe shepherd)
    lsmod | grep shep

    # KernelModule: should talk "shprd: found device", "found PRU0/1", "PRUs started"
    dmesg | grep shp

    # KernelModule: ``state`` should exist
    ll /sys/shepherd/

    # Shepherd program: >
    cp /opt/shepherd/software/meta-package/example_config_harvest.yml /etc/shepherd/config.yml
    shepherd-sheep -vv run --config /etc/shepherd/config.yml
        -> error, no /sys/shepherd/state
            there is /sys/module/shepherd, without "state"

Debug (on sheep)::

    # KModule autoload in
    sudo nano /etc/modules
    /lib/modules/$(KVERSION)/extra/shepherd.ko

    # manual load fw into pru
    /sys/class/remoteproc/remoteprocX/firmware      -> fw-name in lib/firmware/ usually am335x_pru0-shepherd-fw
    echo "start" > /sys/class/remoteproc/remoteprocX/state



Tests for preparing software-release
------------------------------------

    - use a fresh ubuntu lts host and newest fresh ubuntu image for BB
    - follow install instructions (install ansible, bootstrap, deploy)
    - let pytests run

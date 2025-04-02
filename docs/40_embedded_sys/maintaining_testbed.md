# Maintaining the Testbed

## Regular Updates

```Shell
shepherd-herd shell-cmd "sudo pip install click -U --break-system-packages"
shepherd-herd shell-cmd "sudo pip install pydantic -U --break-system-packages"

shepherd-herd shell-cmd "sudo apt update"
shepherd-herd shell-cmd "apt list --upgradable"
shepherd-herd shell-cmd "sudo apt dist-upgrade -y"
```

## Check Storage

```Shell
df -h

sudo du -s /var/shepherd/* | sort -n
```

One thing to figure out is why `df` shows 3 TB usage, but the folders inside only sum up to 100 GB.

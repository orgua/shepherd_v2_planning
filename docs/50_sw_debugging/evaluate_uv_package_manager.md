# Evaluate UV Package Manager

## Advantages for us

- can install the newest python versions
- all done in virtual envs
- even installed apps are kept in venvs
- very fast
- dependencies can be kept up-to-date easier

## Try using it on BBB

```Shell
curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.cargo/env

uv python list
# cpython-3.10.12-linux-armv7-gnu    /usr/bin/python3.10
uv install python
# error: No download found for request: cpython-3.11-linux-armv7-gnu
```

Still an [open bug](https://github.com/astral-sh/uv/issues/6873) in uv (v0.4.15, 2024-09-23)
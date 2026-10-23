# Step 02 - Installation

## Goal
Install the Zenoh Python library on all three machines with the same pinned version.
The `zenohd` router is installed later (Step 05) on Pi-2 only.

## Why a pinned version
Nodes in a Zenoh network should run the same version. The version is pinned in
`requirements.txt`, so every machine installs exactly the same package via the repo.

## Why a virtual environment
Debian 12/13 block `pip install` into the system Python (PEP 668), and a venv keeps
the lab isolated from the host's Python installation.

## Result

| Machine | Python | Wheel                                       | eclipse-zenoh |
|---------|--------|---------------------------------------------|---------------|
| Laptop  | 3.14   | cp39-abi3 macOS universal2                  | 1.10.1        |
| Pi-1    | 3.11   | cp39-abi3 manylinux_2_28_aarch64            | 1.10.1        |
| Pi-2    | 3.13   | cp39-abi3 manylinux_2_28_aarch64            | 1.10.1        |

The wheels are `abi3`, so a single build works across Python 3.9+.

## Commands
Laptop:
    python3 -m venv .venv && source .venv/bin/activate
    pip install -U pip && pip install -r requirements.txt

Pi-1 / Pi-2:
    sudo apt install -y python3-venv
    git clone https://github.com/deoxys08/zenoh-lab.git && cd zenoh-lab
    python3 -m venv .venv && source .venv/bin/activate
    pip install -U pip && pip install -r requirements.txt

Verify:
    python -c "import zenoh; print('zenoh import OK')"

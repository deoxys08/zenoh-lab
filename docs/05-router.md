# Step 05 - zenohd router

## Goal
Install and run the Zenoh router (`zenohd`) on Pi-2, pinned to the same version
as the Python library used by the applications.

## What a router is
A router is a dedicated Zenoh process that neither produces nor consumes data
itself; it relays traffic between the nodes connected to it. It also hosts
plugins (e.g. storage) and can be linked to other routers to span networks.

## Installation (Pi-2, Debian 13)
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key \
      | sudo gpg --dearmor -o /etc/apt/keyrings/zenoh.gpg
    echo "deb [signed-by=/etc/apt/keyrings/zenoh.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" \
      | sudo tee /etc/apt/sources.list.d/zenoh.list
    sudo apt update
    sudo apt install -y zenohd=1.10.1

The package ships a `zenohd.service` systemd unit, installed disabled.
For this lab the router is started manually to watch its logs.

## Running
    zenohd -l tcp/<PI2_LAN_IP>:7447

Listening only on the LAN address (lesson from Step 04) keeps the advertised
locator list clean.

## Startup log highlights
- `mode: router`: same Zenoh runtime, different role.
- `Using ZID: ...`: every Zenoh node has a unique Zenoh ID.
- `Zenoh can be reached at: tcp/<PI2_LAN_IP>:7447`: the only advertised locator.
- `Listening scout messages on 224.0.0.224:7446`: the router answers multicast
  scouting, so local nodes can discover it automatically.
- `access_control.enabled: false`: no authentication or authorization by default.
  Anyone who can reach the port can connect; production setups need TLS and ACLs.

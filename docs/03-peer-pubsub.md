# Step 03 - Peer-to-peer pub/sub

## Goal
Exchange messages directly between the laptop and Pi-1 in peer mode, with no
router or broker in between.

## Concepts in the code
- `zenoh.open(conf)` opens a **session**: the application's entry point to Zenoh.
- `--key` is a **key expression**: the name/address of the data.
  The publisher writes to `lab/<name>/counter`; the subscriber listens on `lab/**`
  (`**` matches any number of levels below `lab/`).
- `pub.put(...)` sends a sample to everyone currently subscribed to a matching key.

## Connection setup
- Pi-1 listens on `tcp/0.0.0.0:7447`.
- The laptop opens no listening socket (`--no-listen`) and connects to Pi-1 (`--connect`).
- Endpoints are given explicitly; automatic discovery is explored in Step 04.

## Experiment A - laptop publishes, Pi-1 subscribes
Pi-1:   python scripts/sub.py --listen tcp/0.0.0.0:7447
Laptop: python scripts/pub.py --no-listen --connect tcp/$PI1_IP:7447

Result: 16 messages sent, 16 received, in order.

## Experiment B - Pi-1 publishes, laptop subscribes (late join)
Pi-1:   python scripts/pub.py --listen tcp/0.0.0.0:7447 --name pi1 --key lab/pi1/counter
Laptop: python scripts/sub.py --no-listen --connect tcp/$PI1_IP:7447   (started ~13 s later)

Result: the first message received by the laptop was `pi1 #14`.

## Observations
- Once the TCP link is established, both sides are equal peers. Who connected to whom
  only decides how the link was created, not which way data can flow.
- Data flowed towards the laptop over a connection the laptop initiated, so an
  outbound-only device can both send and receive.
- Pub/sub has no memory by default: samples published while nobody was subscribed
  (#1-#13) were simply lost. Retaining data requires an explicit component such as
  a Zenoh storage.
- The subscriber declares its interest (`lab/**`) to the other side; the publisher
  only sends samples over the network when a matching subscriber exists.

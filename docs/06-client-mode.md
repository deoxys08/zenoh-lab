# Step 06 - Client mode via a router

## Goal
Connect Pi-1 and the laptop as clients to the router on Pi-2 and exchange
messages through it. Then observe what happens when the router goes down.

## Commands
Pi-2:   zenohd -l tcp/<PI2_LAN_IP>:7447
Pi-1:   python scripts/pub.py --mode client --connect tcp/<PI2_LAN_IP>:7447 --name pi1 --key lab/pi1/counter
Laptop: python scripts/sub.py --mode client --connect tcp/<PI2_LAN_IP>:7447

A client opens no listening socket, so `--no-listen` is no longer needed.

## Experiment A - topology
- `ss` on the router: two established links (Pi-1 and laptop).
- `ss` on Pi-1: a single link, to the router.
- No direct link between Pi-1 and the laptop; all traffic is relayed by the router.
- The laptop, started later, began receiving at `#16`: the router relays but does not store.

## Experiment B - router restart
The router was stopped for ~10 s while pub/sub was running, then restarted.

- Messages `#24-#38` were lost.
- The publisher kept printing `[sent]` with no error: `put` means "handed to Zenoh",
  not "delivered". Default pub/sub has no end-to-end acknowledgement.
- The restarted router had a new ZID (no previous state), yet both clients
  reconnected automatically and the subscriber's interest was re-declared;
  data flow resumed with no reconnection code in the application.

## Peer vs client vs router

|                          | Peer                   | Client               | Router                |
|--------------------------|------------------------|----------------------|-----------------------|
| Opens a listening port   | yes                    | no                   | yes                   |
| Connects to              | peers and routers      | a single router      | other routers         |
| Multicast scouting       | to find peers          | only to find a router| answers scouts        |
| Relays others' traffic   | no                     | no                   | yes                   |

- Peer: direct links, lowest latency, no single point of failure; full mesh, same LAN.
- Client: lightest role, outbound-only, ideal for constrained or unreachable devices.
- Router: relays traffic, spans networks, links to other routers, hosts plugins;
  adds a hop and is a single point of failure unless made redundant.

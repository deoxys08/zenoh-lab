# Step 08 - Comparison with MQTT

Each point is grounded in an experiment from this lab.

| Topic | MQTT | Zenoh (observed in this lab) |
|-------|------|------------------------------|
| Broker | Always required | Optional: peers talked directly (Steps 03-04); router added in Step 05 |
| Topology | Star around the broker | Peer mesh, client-to-router star; router-to-router possible |
| Discovery | Broker address configured | Multicast scouting found peers automatically (Step 04); `listen` needed on multi-homed hosts |
| Request/response | Emulated with two topics and a timeout | Native get/queryable: multiple replies, explicit completion, immediate empty result when nobody answers (Step 07) |
| Late joiners | Retained message gives the last value | No memory by default: late subscribers missed earlier samples (Steps 03, 06); needs storage or extensions |
| Delivery | QoS 1/2 acknowledged by the broker; persistent sessions queue for offline subscribers | No end-to-end ack by default: samples sent during the router outage were lost silently (Step 06) |
| Unneeded traffic | Publisher always sends to the broker | Interest is declared up front; data is only forwarded where a matching subscriber or queryable exists (Steps 03, 07) |
| Addressing | Topics with `+` / `#` | Key expressions with `*` / `**`, shared by pub/sub and queries |
| Security defaults | Broker-dependent | Router started with access control disabled (Step 05) |

## Where each fits
- MQTT: mature ecosystem, native cloud support, retain and persistent sessions out of the box.
- Zenoh: low-latency edge/in-vehicle communication, brokerless operation, native queries,
  scales down to constrained devices.
- They can coexist: a Zenoh router can expose an MQTT interface through a plugin.

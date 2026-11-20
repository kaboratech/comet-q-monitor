# Configuration Guide

## 1. Comet Q configuration

The Comet Q script uses a local configuration file:

`/userdata/trmnl-glkvm.conf`

Create this file using the example provided in:

`examples/trmnl-glkvm.conf.example`

Set the receiver URL:

```sh
RECEIVER_URL="http://RECEIVER_HOST:8766/cometq"
```

Replace `RECEIVER_HOST` with the address of your receiver.

## 2. Receiver configuration

The receiver uses an environment file:

`/etc/trmnl-cometq.env`

Start with the example:

`examples/trmnl-cometq.env.example`

Configure the following variables:

| Variable | Description |
|---|---|
| `BIND_IP` | Network address used by the receiver |
| `PORT` | Receiver listening port |
| `ALLOWED_SOURCE_IP` | Comet Q address allowed to send data |
| `TRMNL_WEBHOOK` | Private TRMNL webhook URL |
| `STATE_FILE` | Path used to store monitoring state |
| `OFFLINE_TIMEOUT` | Time in seconds before the device is marked offline |

## 3. Important settings

- The receiver defaults to `127.0.0.1`. Configure `BIND_IP` appropriately if the Comet Q must reach it over the network.
- The receiver and Comet Q must be able to communicate.
- `ALLOWED_SOURCE_IP` should match the Comet Q's source address as seen by the receiver.
- Keep the TRMNL webhook private. Never publish the real value.

## 4. Network security

The receiver uses HTTP and source IP filtering. This is not encryption or authentication.

Use it only on a trusted LAN or VPN. Do not expose port 8766 directly to the public internet.

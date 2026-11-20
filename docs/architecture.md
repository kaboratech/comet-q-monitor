# Project Architecture

## Overview

The Kaboratech Comet Q Monitor uses two main components:

1. A monitoring script running on the GL.iNet Comet Q.
2. A receiver running on a separate Linux device.

The receiver forwards the monitoring information to TRMNL.

## Data flow

```text
┌──────────────────────┐
│   GL.iNet Comet Q    │
│                      │
│   glkvm-info         │
│   trmnl-glkvm.sh     │
└──────────┬───────────┘
           │
           │ HTTP POST
           ▼
┌──────────────────────┐
│   Linux Receiver     │
│                      │
│   receiver.py        │
│   Watchdog           │
└──────────┬───────────┘
           │
           │ TRMNL Webhook
           ▼
┌──────────────────────┐
│       TRMNL          │
│                      │
│   Monitoring Display │
└──────────────────────┘
```

## Components

### Comet Q

The Comet Q runs scripts that collect system information, including:

- CPU temperature
- Memory usage
- Storage usage
- System uptime
- System load
- Network status
- Tailscale connection status

The monitoring script sends this information to the receiver.

### Linux Receiver

The receiver:

- Accepts monitoring data from the Comet Q.
- Checks the configured source IP.
- Stores the latest monitoring state.
- Forwards information to the TRMNL webhook.
- Detects when the Comet Q stops reporting.

### TRMNL

TRMNL displays the monitoring information using a private plugin.

## Network requirements

The Comet Q must be able to reach the receiver on its configured address and port.

The receiver needs internet access to communicate with TRMNL.

The default receiver port is `8766`.

## Design

The receiver is separated from the Comet Q so that monitoring can continue to be managed independently of the device being monitored.

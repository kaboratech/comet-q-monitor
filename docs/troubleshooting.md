# Troubleshooting

This guide covers common issues when setting up Kaboratech Comet Q Monitor.

## 1. Comet Q cannot reach the receiver

Check that:

- The receiver is running.
- The receiver is listening on the correct network address.
- The configured port is correct (default: `8766`).
- Both devices can communicate over the network.
- The firewall allows the connection.

Check that `RECEIVER_URL` in `/userdata/trmnl-glkvm.conf` points to the correct receiver address.

## 2. Receiver rejects incoming requests

Check the `ALLOWED_SOURCE_IP` setting in the receiver environment file.

It must match the source IP address seen by the receiver when the Comet Q connects.

Also check the receiver logs for error messages.

## 3. TRMNL does not receive monitoring data

Check that:

- The `TRMNL_WEBHOOK` value is correct.
- The webhook has not been exposed or accidentally changed.
- The receiver has internet access.
- The receiver logs do not report delivery errors.

Never share your real webhook URL when requesting help.

## 4. Device appears offline

The receiver uses a timeout to determine whether the Comet Q has stopped reporting.

Check:

- Whether the Comet Q is powered on.
- Whether its monitoring script is running.
- Whether network connectivity is available.
- Whether `OFFLINE_TIMEOUT` is appropriate for the reporting interval.

## 5. Receiver service does not start

Check the systemd service status:

```sh
sudo systemctl status trmnl-cometq
```

View recent service logs:

```sh
sudo journalctl -u trmnl-cometq -n 50 --no-pager
```

Check that the environment file and script paths match your installation.

## 6. Health endpoint

The receiver provides a health endpoint:

```text
http://RECEIVER_HOST:8766/health
```

Replace `RECEIVER_HOST` with the receiver's address.

A successful response indicates that the receiver's HTTP server is responding. It does not guarantee that TRMNL delivery is working.

## Getting help

When reporting an issue, include:

- The component affected (Comet Q, receiver or TRMNL).
- The error message.
- Relevant logs with private information removed.
- Your operating system and software versions.

Never publish passwords, webhook URLs, private IP details or authentication tokens.

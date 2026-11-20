# GL.iNet Comet Q Monitor

**A Kaboratech project for monitoring the GL.iNet Comet Q and sending system information to a TRMNL dashboard.**

This project provides a lightweight monitoring solution for the GL.iNet Comet Q (GLKVM), allowing you to monitor device health and connectivity through a TRMNL display.

## Demo & Video Review

**GL.iNet Comet Q Review – Control Any PC From Anywhere!**

[Watch the full video review](https://youtu.be/ZJA3Ocfnb-s)

- [Terminal demonstration — 05:25](https://youtu.be/ZJA3Ocfnb-s?t=325)
- [TRMNL dashboard demonstration — 15:09](https://youtu.be/ZJA3Ocfnb-s?t=909)

## Features

- CPU temperature monitoring
- RAM usage monitoring
- Storage usage monitoring
- System uptime
- CPU load average
- Wi-Fi connection status
- Local network IP information
- Tailscale connection status
- TRMNL dashboard integration
- Offline detection through a separate receiver

## How It Works

The project uses two main components:

1. **Comet Q client:** collects system information from the GL.iNet Comet Q and sends it to a receiver on the local network.
2. **TRMNL receiver:** accepts monitoring data, forwards it to TRMNL and detects when the Comet Q stops reporting.

The receiver runs on a separate Linux host. The Comet Q does not need to communicate directly with the TRMNL service.

## Repository Structure

```text
comet-q-monitor/
├── docs/
│   ├── installation.md
│   ├── configuration.md
│   ├── security.md
│   ├── architecture.md
│   └── troubleshooting.md
├── examples/
│   ├── trmnl-glkvm.conf.example
│   └── trmnl-cometq.env.example
├── receiver/
│   ├── receiver.py
│   └── trmnl-cometq.service
├── scripts/
│   ├── glkvm-info
│   └── trmnl-glkvm.sh
├── .gitignore
└── README.md
```

## Documentation

Detailed guides are available in the `docs/` directory:

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [Security Guide](docs/security.md)
- [Project Architecture](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)

## Requirements

- GL.iNet Comet Q / GLKVM
- SSH access to the Comet Q
- A separate Linux host to run the receiver
- Python 3 and curl on the receiver
- A TRMNL account and compatible private plugin
- Network connectivity between the Comet Q and the receiver

## Configuration

Example configuration files are provided in the `examples/` directory.

Replace all placeholder values with your own settings before running the scripts.

**Never publish your actual TRMNL webhook URL, passwords, tokens or private network information.**

## Security

- Never publish TRMNL webhook URLs, credentials or private configuration files.
- Use example configuration files with placeholder values.
- Keep the receiver accessible only through a trusted network or VPN.
- Do not expose the receiver directly to the public internet.
- The receiver uses HTTP and source IP filtering; this does not provide encryption or authentication.

Read the [Security Guide](docs/security.md) before installation.

## Project Status

The project is published as an initial public release.

Documentation is available for installation, configuration, security, architecture and troubleshooting.

The project has not yet been independently tested by other users. Feedback, suggestions and contributions are welcome.

## About Kaboratech

Developed by **Kaboratech**, covering hardware reviews, homelab projects, monitoring solutions and practical technology experiments.

- YouTube: https://www.youtube.com/c/kaboratech/videos
- GitHub: https://github.com/kaboratech


# GL.iNet Comet Q Monitor

**A Kaboratech project for monitoring the GL.iNet Comet Q and sending system information to a TRMNL dashboard.**

This project provides a lightweight monitoring solution for the GL.iNet Comet Q (GLKVM), allowing you to keep track of device health and connectivity through a TRMNL display.

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

The project uses two components:

1. **Comet Q client:** collects system information from the GL.iNet Comet Q and sends it to a receiver on the local network.
2. **TRMNL receiver:** accepts monitoring data, forwards it to TRMNL and detects when the Comet Q stops reporting.

The receiver runs on a separate Linux host. The Comet Q does not need to communicate directly with the TRMNL service.

## Project Status

The project is being prepared for public release. Installation instructions, configuration examples and security notes will be added after validation.

## Security

- Never publish TRMNL webhook URLs, credentials or private configuration files.
- Use example configuration files with placeholder values.
- Keep the receiver accessible only through a trusted network or VPN.
- Do not expose the receiver directly to the public internet.

## Requirements

- GL.iNet Comet Q / GLKVM
- A Linux host to run the receiver
- A TRMNL account and compatible private plugin
- Network connectivity between the Comet Q and the receiver

## About Kaboratech

Developed by **Kaboratech**, covering hardware reviews, homelab projects, monitoring solutions and practical technology experiments.

- YouTube: https://www.youtube.com/c/kaboratech/videos
- GitHub: https://github.com/kaboratech

More documentation and project files will be published as they are reviewed and prepared for release.

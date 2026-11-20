# Installation Guide

## Overview

This project provides a monitoring solution for the GL.iNet Comet Q (GLKVM), with optional integration with a TRMNL display.

The solution has two components:

- **Comet Q:** Collects system information and sends it to a receiver.
- **Receiver:** Runs on a separate Linux device and forwards monitoring data to TRMNL.

## Requirements

### Comet Q
- GL.iNet Comet Q / GLKVM device
- SSH access
- `sh`
- `curl`
- Network connectivity to the receiver

### Receiver
- A separate Linux device
- Python 3
- `curl`
- `systemd`
- Network connectivity to the Comet Q and the internet

## Installation status

Installation instructions are being prepared. The scripts and service files in this repository are provided as examples and should be reviewed and adapted to your environment before use.

**Important:** Do not copy example configuration values directly. Replace all placeholders with your own settings.

## Security

- Keep webhook URLs and credentials private.
- Do not expose the receiver directly to the internet.
- Prefer a trusted local network or VPN.
- Configure the receiver to accept requests only from the Comet Q.

# Security Guide

## Protect your credentials

Never publish:

- TRMNL webhook URLs
- Passwords or authentication tokens
- SSH private keys
- Private configuration files
- Personal or public-facing device identifiers that reveal your network setup

Use the example configuration files in the `examples/` directory. Replace placeholders locally with your own values.

## Network security

The receiver accepts HTTP requests from a configured source IP.

Important considerations:

- Use the receiver only on a trusted local network or VPN.
- Do not forward port 8766 from your router to the public internet.
- Configure `ALLOWED_SOURCE_IP` to restrict incoming requests.
- Keep the receiver and Comet Q software updated.

## HTTP limitations

The current receiver uses HTTP, not HTTPS.

Source IP filtering is not encryption or authentication. Monitoring data could be observed by other devices with access to the same network.

Use a trusted network and do not send sensitive information through this service.

## Public repository checklist

Before publishing changes, check that:

- No real IP addresses or private hostnames are included.
- No webhook URLs or credentials are included.
- No private keys or passwords are included.
- Example files contain placeholders only.
- Logs and runtime data are not committed.

## Reporting a security issue

If you discover a security problem, avoid publishing credentials or sensitive details in a public issue.

Contact the repository owner privately to report the problem.

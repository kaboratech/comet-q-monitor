
#!/bin/sh

# Kaboratech - GL.iNet Comet Q TRMNL Monitor
# Public version: receiver address is stored in a separate config file.

CONFIG_FILE="/userdata/trmnl-glkvm.conf"

if [ ! -r "$CONFIG_FILE" ]; then
    echo "ERROR: Configuration file not found or not readable:"
    echo "$CONFIG_FILE"
    exit 1
fi

. "$CONFIG_FILE"

if [ -z "$RECEIVER_URL" ]; then
    echo "ERROR: RECEIVER_URL is not configured."
    exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl is not installed."
    exit 1
fi

HOSTNAME="$(hostname)"

TEMP_RAW="$(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null)"
TEMP_C="$(awk -v t="$TEMP_RAW" 'BEGIN {if (t ~ /^[0-9]+$/) printf "%.1f", t/1000; else printf "0"}')"

MEM_TOTAL="$(awk '/^MemTotal:/ {printf "%d", $2/1024}' /proc/meminfo)"
MEM_AVAILABLE="$(awk '/^MemAvailable:/ {printf "%d", $2/1024}' /proc/meminfo)"
MEM_USED=$((MEM_TOTAL - MEM_AVAILABLE))

DISK_TOTAL="$(df -k /userdata | awk 'END {printf "%d", $2/1024}')"
DISK_USED="$(df -k /userdata | awk 'END {printf "%d", $3/1024}')"
DISK_FREE="$(df -k /userdata | awk 'END {printf "%d", $4/1024}')"
DISK_PERCENT="$(df -k /userdata | awk 'END {gsub(/%/,"",$5); print $5}')"

UPTIME_SECONDS="$(awk '{printf "%d", $1}' /proc/uptime)"
DAYS=$((UPTIME_SECONDS / 86400))
HOURS=$(((UPTIME_SECONDS % 86400) / 3600))
MINUTES=$(((UPTIME_SECONDS % 3600) / 60))
UPTIME_TEXT="${DAYS}d ${HOURS}h ${MINUTES}m"

LOAD1="$(awk '{print $1}' /proc/loadavg)"

WIFI_STATE="$(cat /sys/class/net/wlan0/operstate 2>/dev/null)"
[ -n "$WIFI_STATE" ] || WIFI_STATE="unknown"
WIFI_STATE="$(printf '%s' "$WIFI_STATE" | tr '[:lower:]' '[:upper:]')"

LOCAL_IP="$(ip -o -4 addr show dev wlan0 scope global 2>/dev/null | awk '{split($4,a,"/"); print a[1]; exit}')"
[ -n "$LOCAL_IP" ] || LOCAL_IP="N/A"

if tailscale status >/dev/null 2>&1; then
    TAILSCALE="CONNECTED"
else
    TAILSCALE="DISCONNECTED"
fi

PAYLOAD="$(printf '{
  "merge_variables": {
    "device": "GLKVM",
    "hostname": "%s",
    "temperature_c": %s,
    "uptime": "%s",
    "uptime_seconds": %s,
    "ram_total_mb": %s,
    "ram_used_mb": %s,
    "ram_available_mb": %s,
    "storage_total_mb": %s,
    "storage_used_mb": %s,
    "storage_free_mb": %s,
    "storage_used_percent": "%s",
    "load_average": "%s",
    "wifi": "%s",
    "local_ip": "%s",
    "tailscale": "%s"
  }
}' "$HOSTNAME" "$TEMP_C" "$UPTIME_TEXT" "$UPTIME_SECONDS" \
"$MEM_TOTAL" "$MEM_USED" "$MEM_AVAILABLE" \
"$DISK_TOTAL" "$DISK_USED" "$DISK_FREE" "$DISK_PERCENT" \
"$LOAD1" "$WIFI_STATE" "$LOCAL_IP" "$TAILSCALE")"

echo "Sending Comet Q data to the local receiver..."

HTTP_CODE="$(curl -sS -o /tmp/trmnl-glkvm-response \
    -w '%{http_code}' \
    --max-time 15 \
    -X POST "$RECEIVER_URL" \
    -H 'Content-Type: application/json' \
    --data-binary "$PAYLOAD")"

echo "HTTP response: $HTTP_CODE"

case "$HTTP_CODE" in
    2*)
        echo "Data accepted by the receiver."
        ;;
    *)
        echo "Data delivery was not confirmed. Response:"
        cat /tmp/trmnl-glkvm-response 2>/dev/null
        ;;
esac

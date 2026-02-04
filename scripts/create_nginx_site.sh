#!/bin/sh
set -e

DOMAIN="nfix.uz"
UPSTREAM_PORT="8007"
SITES_AVAILABLE="/etc/nginx/sites-available"
SITES_ENABLED="/etc/nginx/sites-enabled"

CONF_PATH="${SITES_AVAILABLE}/${DOMAIN}"
LINK_PATH="${SITES_ENABLED}/${DOMAIN}"

if [ -f "$CONF_PATH" ]; then
  echo "Config already exists: $CONF_PATH"
else
  cat <<'EOF' > "$CONF_PATH"
server {
    listen 80;
    server_name nfix.uz;

    location / {
        proxy_pass http://127.0.0.1:8007;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
  echo "Created config: $CONF_PATH"
fi

if [ -L "$LINK_PATH" ] || [ -e "$LINK_PATH" ]; then
  echo "Link already exists: $LINK_PATH"
else
  ln -s "$CONF_PATH" "$LINK_PATH"
  echo "Enabled site: $LINK_PATH"
fi

echo "Test with: nginx -t"
echo "Reload with: systemctl reload nginx"

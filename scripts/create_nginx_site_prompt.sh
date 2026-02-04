#!/bin/sh
set -e

printf "Domain (server_name): "
read -r DOMAIN
if [ -z "$DOMAIN" ]; then
  echo "Domain is required."
  exit 1
fi

printf "Root path (leave empty to use reverse proxy): "
read -r ROOT_PATH

printf "Upstream port (leave empty to use root path): "
read -r UPSTREAM_PORT

SITES_AVAILABLE="/etc/nginx/sites-available"
SITES_ENABLED="/etc/nginx/sites-enabled"

CONF_PATH="${SITES_AVAILABLE}/${DOMAIN}"
LINK_PATH="${SITES_ENABLED}/${DOMAIN}"

if [ -f "$CONF_PATH" ]; then
  echo "Config already exists: $CONF_PATH"
  exit 0
fi

if [ -n "$ROOT_PATH" ] && [ -n "$UPSTREAM_PORT" ]; then
  echo "Choose either root path or upstream port, not both."
  exit 1
fi

if [ -z "$ROOT_PATH" ] && [ -z "$UPSTREAM_PORT" ]; then
  echo "You must provide either a root path or an upstream port."
  exit 1
fi

if [ -n "$ROOT_PATH" ]; then
  cat <<EOF > "$CONF_PATH"
server {
    listen 80;
    server_name ${DOMAIN};

    root ${ROOT_PATH};
    index index.html index.htm;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
    }

    location ~ /\.ht {
        deny all;
    }
}
EOF
  echo "Created static site config: $CONF_PATH"
else
  cat <<EOF > "$CONF_PATH"
server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:${UPSTREAM_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
  echo "Created proxy site config: $CONF_PATH"
fi

if [ -L "$LINK_PATH" ] || [ -e "$LINK_PATH" ]; then
  echo "Link already exists: $LINK_PATH"
else
  ln -s "$CONF_PATH" "$LINK_PATH"
  echo "Enabled site: $LINK_PATH"
fi

echo "Test with: nginx -t"
echo "Reload with: systemctl reload nginx"

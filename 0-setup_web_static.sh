#!/usr/bin/env bash
# Sets up web server for static website

if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "
<html>
<head></head>
<body>
  Holberton School
</body>
</html>
" > /data/web_static/releases/test/index.html

rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"
config_content=$(cat << EOM
server {
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location /redirect_me {
	return 301 http://esmond-portfolio.vercel.app;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}
EOM
)
echo "$config_content" > "$config_file"
service nginx restart

#!/bin/bash
set -e

# Setup
echo "Setting up Snipper (FastAPI + SQLite + Uvicorn + Poetry + Nginx + Systemd + UDS)"
echo "This script will install the necessary dependencies and set up a systemd service for Snipper."
echo "Please run this script as root or with sudo."

PROJECT_DIR="$(
    cd "$(dirname "$0")"
    pwd
)"

# Install dependencies
echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv sqlite3 libsqlite3-dev nginx ufw

# Create virtual environment
sudo apt-get update
cd "$PROJECT_DIR"
python3 -m venv venv
source venv/bin/activate

# Install Poetry in venv if not present
if ! venv/bin/poetry --version &>/dev/null; then
    echo "Poetry not found, installing..."
    pip install poetry
fi

# Install project dependencies
echo "Installing project dependencies..."
venv/bin/poetry install

# Create systemd service file
echo "Creating systemd service file..."
sudo tee /etc/systemd/system/snipper.service >/dev/null <<EOF
[Unit]
Description=Snipper Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$(poetry env info --path) app:app --host 0.0.0.0 --port 8000 --uds /tmp/snipper.sock --workers $(($(nproc) * 2 + 1)) --env-file .env --access-log --use-colors --no-server-header --proxy-headers
Restart=always
User=$USER
Group=$USER
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=$(poetry env info --path)/lib/python3.*/site-packages
Environment=PATH=$(poetry env info --path)/bin:$PATH
Environment=VIRTUAL_ENV=$(poetry env info --path)

[Install]
WantedBy=multi-user.target
EOF

# Set up Nginx
echo "Setting up Nginx..."
sudo tee /etc/nginx/sites-available/snipper >/dev/null <<EOF
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://unix:/tmp/snipper.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx configuration
sudo ln -s /etc/nginx/sites-available/snipper /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 22/tcp
sudo ufw allow 'Nginx Full'
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw enable

# Enable and start the Snipper service
echo "Enabling and starting the Snipper service..."
sudo systemctl daemon-reload
sudo systemctl enable snipper.service
sudo systemctl start snipper.service
sudo systemctl status snipper.service

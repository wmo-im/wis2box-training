#!/bin/bash
set -e

USERNAME="${1}"

# ==========================
# Remove existing user if exists
# ==========================
if id "$USERNAME" &>/dev/null; then
  echo "User $USERNAME already exists. Removing..."
  sudo pkill -u "$USERNAME" || true
  sudo deluser --remove-home "$USERNAME"
fi

# ==========================
# Install Docker and dependencies
# ==========================
echo "Installing Docker and dependencies..."
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get -y update
sudo apt-get install -y docker-ce docker-compose-plugin unzip python3-pip wget
sudo pip3 install --upgrade pip pyopenssl
sudo pip3 install urllib3==1.26.0

sudo pip3 install minio
sudo pip3 install pywiscat==0.4.0

# ==========================
# Create user with random password
# ==========================
echo "Creating new user '$USERNAME'..."
PASSWORD=$(openssl rand -base64 14 | tr -dc 'A-Za-z0-9' | head -c10)

sudo useradd -m -s /bin/bash "$USERNAME"
echo "${USERNAME}:${PASSWORD}" | sudo chpasswd
sudo usermod -aG docker,sudo "$USERNAME"

USER_HOME="/home/$USERNAME"
sudo chown -R "$USERNAME:$USERNAME" "$USER_HOME"
sudo chmod 755 "$USER_HOME"

# ==========================
# Download and unzip content
# ==========================
echo "Downloading and unpacking setup files..."
sudo -u "$USERNAME" bash <<EOF
cd "$USER_HOME"
wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.2.0/wis2box-setup-1.2.0.zip
unzip wis2box-setup-1.2.0.zip && rm wis2box-setup-1.2.0.zip
wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
unzip exercise-materials.zip && rm exercise-materials.zip
EOF

sudo chown -R "$USERNAME:$USERNAME" "$USER_HOME"

# ==========================
# Display result
# ==========================
echo "====================================="
echo "Setup completed successfully!"
echo "Username: $USERNAME"
echo "Password: $PASSWORD"
echo "====================================="

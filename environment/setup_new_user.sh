# /bin/bash
# this is a  simple script to create a new user on the local training hardware
# and ensure the user has required materials in the home-directory

read -p "USERNAME: " USERNAME

echo "USERNAME=`echo $USERNAME`"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

sudo useradd -p $(openssl passwd -1 "wis2training") "$USERNAME" -m -G docker,sudo --shell /bin/bash
sudo cp -rf exercise-materials/ /home/`echo $USERNAME`/exercise-materials/
sudo cp -rf wis2box-1.0b3/ /home/`echo $USERNAME`/wis2box-1.0b3/

echo WIS2BOX_HOST_DATADIR=/home/`echo $USERNAME`/exercise-materials/wis2box-test-data/ > /tmp/dev.env
echo WIS2BOX_URL=http://`echo $USERNAME`.wis2.training >> /tmp/dev.env
echo WIS2BOX_API_URL=http://`echo $USERNAME`.wis2.training/oapi >> /tmp/dev.env
echo WIS2BOX_LOGGING_LOGLEVEL=INFO >> /tmp/dev.env
sudo cp /tmp/dev.env /home/`echo $USERNAME`/wis2box-1.0b3/

# create ftp.env
echo MYHOSTNAME=`echo $USERNAME`.wis2.training > /tmp/ftp.env
echo FTP_USER=wis2box > /tmp/ftp.env
echo FTP_PASS=wis2box > /tmp/ftp.env
echo FTP_HOST=${MYHOSTNAME} > /tmp/ftp.env
echo WIS2BOX_STORAGE_ENDPOINT=http://${MYHOSTNAME}:9000 > /tmp/ftp.env
echo WIS2BOX_STORAGE_USER=minio > /tmp/ftp.env
echo WIS2BOX_STORAGE_PASSWORD=minio123 > /tmp/ftp.env
echo LOGGING_LEVEL=WARNING > /tmp/ftp.env
sudo cp /tmp/ftp.env /home/`echo $USERNAME`/wis2box-1.0b3/ > /tmp/ftp.env

sudo chown -R `echo $USERNAME`:`echo $USERNAME` /home/`echo $USERNAME`
sudo cat /home/`echo $USERNAME`/wis2box-1.0b3/dev.env
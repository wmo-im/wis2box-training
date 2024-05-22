# /bin/bash
# this is a  simple script to create a new user on the local training hardware
# and ensure the user has required materials in the home-directory

# throw and error if no arguments are provided
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./setup_student_vm.sh <USERNAME> <HOST_IP>"
    exit 1
fi

# first argument of the script is the username
USERNAME=$1
# second argument is the IP of the student-vm
HOST_IP=$2

echo "USERNAME=`echo $USERNAME`"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
echo "HOST_IP=`echo $HOST_IP`"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

# execute commands over ssh

# create the user, if not already existing
ssh wmo_admin@`echo $HOST_IP` "sudo useradd "$USERNAME" -m -G docker --shell /bin/bash"
# set the initial password to "wis2training"
ssh wmo_admin@`echo $HOST_IP` "echo "$USERNAME":wis2training | sudo chpasswd"
# rename the hostname to student-vm-<USERNAME>
ssh wmo_admin@`echo $HOST_IP` "sudo hostnamectl set-hostname student-vm-`echo $USERNAME`"

# copy the latest wis2box-setup-1.0b5.zip to the student-vm
ssh wmo_admin@`echo $HOST_IP` "wget https://github.com/wmo-im/wis2box/releases/download/1.0b5/wis2box-setup-1.0b5.zip -O /tmp/wis2box-setup-1.0b5.zip"
# unzip the wis2box-setup-1.0b5.zip
ssh wmo_admin@`echo $HOST_IP` "sudo unzip -o /tmp/wis2box-setup-1.0b5.zip -d /home/`echo $USERNAME`/"
# remove the wis2box-setup-1.0b5.zip
ssh wmo_admin@`echo $HOST_IP` "rm -rf /tmp/wis2box-setup-1.0b5.zip"

# copy the latest exercise materials to the student-vm
ssh wmo_admin@`echo $HOST_IP` "wget https://training.wis2box.wis.wmo.int/exercise-materials.zip -O /tmp/exercise-materials.zip"
# unzip the exercise-materials.zip
ssh wmo_admin@`echo $HOST_IP` "sudo unzip -o /tmp/exercise-materials.zip -d /home/`echo $USERNAME`/"
# remove the exercise-materials.zip
ssh wmo_admin@`echo $HOST_IP` "rm -rf /tmp/exercise-materials.zip"

# create ftp.env
ssh wmo_admin@`echo $HOST_IP` "echo MYHOSTNAME=`echo $USERNAME`.wis2.training > /tmp/ftp.env"	
ssh wmo_admin@`echo $HOST_IP` "echo FTP_USER=wis2box >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "echo FTP_PASS=wis2box >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "echo FTP_HOST=`echo $USERNAME`.wis2.training >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "echo "WIS2BOX_STORAGE_ENDPOINT=http://`echo $USERNAME`.wis2.training:9000" >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "echo WIS2BOX_STORAGE_USERNAME=minio >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "echo WIS2BOX_STORAGE_PASSWORD=minio123 >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "echo LOGGING_LEVEL=WARNING >> /tmp/ftp.env"
ssh wmo_admin@`echo $HOST_IP` "sudo cp /tmp/ftp.env /home/`echo $USERNAME`/wis2box-1.0b7/"
# remove /tmp/ftp.env
ssh wmo_admin@`echo $HOST_IP` "rm -rf /tmp/ftp.env"

ssh wmo_admin@`echo $HOST_IP` "sudo chown -R `echo $USERNAME`:`echo $USERNAME` /home/`echo $USERNAME`"
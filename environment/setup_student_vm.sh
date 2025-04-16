# /bin/bash
# this is a  simple script to create a new user on the local training hardware
# and ensure the user has required materials in the home-directory

# throw and error if no arguments are provided
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./setup_student_vm.sh <USERNAME> <HOST_IP>"
    return 1
fi

# first argument of the script is the username
USERNAME=$1
# second argument is the IP of the student-vm
HOST_IP=$2

echo "USERNAME=`echo $USERNAME`"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || return 1
echo "HOST_IP=`echo $HOST_IP`"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || return 1

# execute commands over ssh

# create the user, if not already existing
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "sudo useradd "$USERNAME" -m -G docker --shell /bin/bash"
# set the initial password to "wis2training"
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "echo "$USERNAME":wis2training | sudo chpasswd"
# rename the hostname to student-vm-<USERNAME>
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "sudo hostnamectl set-hostname student-vm-`echo $USERNAME`"

# copy the latest wis2box-setup.zip to the student-vm
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip -O /tmp/wis2box-setup.zip"
# unzip the wis2box-setup.zip
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "sudo unzip -o /tmp/wis2box-setup.zip -d /home/`echo $USERNAME`/"
# remove the wis2box-setup.zip
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "rm -rf /tmp/wis2box-setup.zip"

# copy the latest exercise materials to the student-vm
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "wget https://training.wis2box.wis.wmo.int/exercise-materials.zip -O /tmp/exercise-materials.zip"
# unzip the exercise-materials.zip
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "sudo unzip -o /tmp/exercise-materials.zip -d /home/`echo $USERNAME`/"
# remove the exercise-materials.zip
ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "rm -rf /tmp/exercise-materials.zip"

ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "sudo chown -R `echo $USERNAME`:`echo $USERNAME` /home/`echo $USERNAME`"

ssh -o StrictHostKeyChecking=no wmo_admin@`echo $HOST_IP` "sudo pip3 install pywiscat==0.2.2"

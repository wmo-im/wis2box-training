#!/bin/bash

USERNAME="$1"
IP="$2"

echo "=== Copying setup script to VM ==="
scp -o StrictHostKeyChecking=accept-new setup_vm.sh "ubuntu@${IP}:/home/ubuntu/setup_vm.sh"

echo "=== Executing setup script on VM ==="
ssh "ubuntu@${IP}" "source setup_vm.sh ${USERNAME}"

echo "=== Adding DNS A record ==="
python3 dns-scripts/add_a_record.py "${USERNAME}.training" "${IP}"

echo "Server setup finished: ${USERNAME}.training.wis2dev.io"
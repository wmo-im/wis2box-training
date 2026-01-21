#!/bin/bash
# ---------------------------------------------------------------------------
# Script: prepare-new-training-instance.sh
# Purpose: Automate the creation and setup of a new training VM instance.
# Usage: ./prepare-new-training-instance.sh <username>
# Example: ./prepare-new-training-instance.sh mlimper
# ---------------------------------------------------------------------------

# Prevent accidental sourcing
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
  echo "Do NOT use: source prepare-new-training-instance.sh"
  return 1 2>/dev/null || exit 1
fi

USERNAME="$1"
SERVER_NAME="${USERNAME}.training.wis2dev.io"

echo "=== Creating OpenStack server for ${USERNAME} ==="
openstack server create \
  --flavor 2cpu-4gbmem-30gbdisk \
  --image Ubuntu-22.04 \
  --key-name EWC-mlimper-training \
  --network external-internet \
  --security-group wis2box-security-group \
  "${SERVER_NAME}"

for i in {1..10}; do
  echo "sleep $i"
  sleep 1
done

echo "=== Fetching server IP address ==="
ADDR_JSON=$(openstack server show "${SERVER_NAME}" -c addresses -f value)
# Example output: {'external-internet': ['136.156.135.48']}
IP=$(echo "$ADDR_JSON" | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")

if [ -z "$IP" ]; then
  echo "Error: Failed to extract IP address from output: $ADDR_JSON"
  exit 1
fi

echo "Server ${SERVER_NAME} is ready at IP ${IP}"

echo "=== Copying setup script to VM ==="
scp -o StrictHostKeyChecking=accept-new setup_vm.sh "ubuntu@${IP}:/home/ubuntu/setup_vm.sh"

echo "=== Executing setup script on VM ==="
ssh "ubuntu@${IP}" "source setup_vm.sh ${USERNAME}"

echo "=== Adding DNS A record ==="
python3 dns-scripts/add_a_record.py "${USERNAME}.training" "${IP}"

echo "Server setup finished: ${USERNAME}.training.wis2dev.io"

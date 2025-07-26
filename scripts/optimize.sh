#!/bin/bash
# EC2 t3.micro Optimization Script
# This script optimizes AWS EC2 t3.micro instances (1 vCPU, 1GB RAM, ~8GB storage)
# for better performance and resource management
#
# 🔄 SAFE TO RE-RUN: This script is idempotent and can be safely executed multiple times
# It will skip operations that have already been completed and only apply missing optimizations
#
# Usage: chmod +x optimize.sh && sudo ./optimize.sh

set -e

echo "=== EC2 t3.micro Optimization Script ==="
echo "Instance specs: 1 vCPU, 1GB RAM, ~8GB storage"
echo "Starting optimization process..."
echo ""

echo "=== [1/6] Creating swap file (1 GB) ==="
# t3.micro has only 1GB RAM, swap is critical for preventing OOM kills
if ! swapon --show | grep -q '/swapfile'; then
    echo "Creating 1GB swap file (recommended for 1GB RAM instances)..."
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile  # Security: only root can read/write
    sudo mkswap /swapfile
    sudo swapon /swapfile
    
    # Make swap permanent across reboots
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    
    # Optimize swappiness for low-memory instances (default is 60)
    if ! grep -q "vm.swappiness=10" /etc/sysctl.conf 2>/dev/null; then
        echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
    fi
    sudo sysctl vm.swappiness=10
    
    echo "✅ Swap created and configured successfully"
else
    echo "ℹ️  Swap already exists, skipping creation"
fi
echo ""

echo "=== [2/6] Cleaning Docker and system files ==="
# Critical for t3.micro with limited 8GB storage
echo "Removing unused Docker images, containers, networks, and volumes..."
docker system prune -af --volumes || echo "⚠️  Docker not running or not installed"

echo "Cleaning package cache and removing unused packages..."
sudo apt autoremove -y
sudo apt autoclean
sudo apt clean

# Additional cleanup for EC2 instances
echo "Cleaning system logs and temporary files..."
sudo journalctl --vacuum-time=3d  # Keep only 3 days of logs
sudo rm -rf /tmp/* /var/tmp/* 2>/dev/null || true
sudo find /var/log -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true

echo "✅ System cleanup completed"
echo ""

echo "=== [3/6] Configuring Docker logging ==="
# Prevent Docker logs from consuming all available storage
DOCKER_CONFIG="/etc/docker/daemon.json"
sudo mkdir -p /etc/docker

echo "Setting up log rotation for Docker containers..."
# Check if configuration already exists and is correct
if [ -f "$DOCKER_CONFIG" ]; then
    if grep -q '"max-size": "10m"' "$DOCKER_CONFIG" && grep -q '"max-file": "3"' "$DOCKER_CONFIG"; then
        echo "ℹ️  Docker logging already configured correctly"
    else
        echo "Updating existing Docker configuration..."
        sudo cp "$DOCKER_CONFIG" "${DOCKER_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        cat <<EOF | sudo tee $DOCKER_CONFIG
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true
}
EOF
    fi
else
    echo "Creating new Docker configuration..."
    cat <<EOF | sudo tee $DOCKER_CONFIG
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true
}
EOF
fi

echo "✅ Docker logging configuration updated"
echo ""

echo "=== [4/6] Optimizing system for low-memory environment ==="
# Additional optimizations for t3.micro's 1GB RAM constraint

# Reduce memory usage by limiting unnecessary services
echo "Configuring memory optimizations..."

# Create memory optimization config
SYSCTL_CONFIG="/etc/sysctl.d/99-ec2-micro-optimize.conf"
if [ -f "$SYSCTL_CONFIG" ]; then
    echo "ℹ️  Memory optimizations already configured, updating if needed..."
else
    echo "Creating new memory optimization configuration..."
fi

cat <<EOF | sudo tee $SYSCTL_CONFIG
# Memory optimizations for t3.micro (1GB RAM)
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_background_ratio=5
vm.dirty_ratio=10

# Network optimizations
net.core.rmem_default=262144
net.core.rmem_max=16777216
net.core.wmem_default=262144
net.core.wmem_max=16777216
EOF

sudo sysctl -p $SYSCTL_CONFIG

echo "✅ System memory optimizations applied"
echo ""

echo "=== [5/6] Restarting Docker with new configuration ==="
if systemctl is-active --quiet docker; then
    echo "Restarting Docker service..."
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    
    # Wait for Docker to be ready
    echo "Waiting for Docker to be ready..."
    timeout 30 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done' || echo "⚠️  Docker restart timeout"
    
    echo "✅ Docker restarted successfully"
else
    echo "ℹ️  Docker is not running, skipping restart"
fi
echo ""

echo "=== [6/6] System status after optimization ==="
echo "📊 Disk usage:"
df -h | grep -E "(Filesystem|/dev/)"
echo ""

echo "💾 Memory usage:"
free -h
echo ""

echo "🔄 Swap status:"
swapon --show
echo ""

echo "🐳 Docker system usage:"
docker system df 2>/dev/null || echo "Docker not available"
echo ""

echo "🎯 EC2 t3.micro optimization completed!"
echo ""
echo "📝 Summary of optimizations:"
echo "   ✅ 1GB swap file created with optimized swappiness"
echo "   ✅ Docker logs limited to 30MB per container"
echo "   ✅ System cache and temporary files cleaned"
echo "   ✅ Memory management optimized for 1GB RAM"
echo "   ✅ Log rotation configured to save disk space"
echo ""
echo "💡 Recommendations:"
echo "   • Run this script weekly to maintain optimal performance"
echo "   • Monitor disk usage: df -h"
echo "   • Monitor memory: free -h"
echo "   • Check Docker usage: docker system df"
echo "   • For persistent low memory, consider upgrading to t3.small"

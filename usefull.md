# Linux System Administration

## How to Check Memory Swap and Create One and Verify

### Check current swap status
```bash
# Display all active swap devices and their details
swapon --show

# Show memory and swap usage in human-readable format
free -h
```

### Create a new swap file (1GB example)
```bash
# Allocate 1GB of space for swap file
sudo fallocate -l 1G /swapfile

# Set proper permissions (readable/writable by root only)
sudo chmod 600 /swapfile

# Format the file as swap space
sudo mkswap /swapfile

# Enable the swap file
sudo swapon /swapfile

# Make swap permanent by adding to fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Verify swap is working
```bash
# Check memory and swap usage after setup
free -h

# Verify swap file is listed
swapon --show
```

### Additional useful swap commands
```bash
# Disable specific swap file
sudo swapoff /swapfile

# Disable all swap
sudo swapoff -a

# Check swap usage by process
sudo grep -i swap /proc/*/status 2>/dev/null | grep -v "0 kB"
```

# Monitoring 

top 
htop
docker stats
docker system df

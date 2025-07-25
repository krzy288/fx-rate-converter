#!/bin/bash
set -e

echo "🧹 [1/6] Zatrzymywanie wszystkich kontenerów..."
docker stop $(docker ps -aq) 2>/dev/null || true

echo "🗑️ [2/6] Usuwanie wszystkich kontenerów, obrazów i wolumenów..."
docker system prune -a --volumes -f

echo "🧽 [3/6] Czyszczenie APT cache..."
sudo apt clean

echo "🧼 [4/6] Czyszczenie logów systemowych..."
sudo journalctl --vacuum-time=1d
sudo truncate -s 0 /var/log/syslog || true
sudo truncate -s 0 /var/log/docker.log || true

echo "🧯 [5/6] Czyszczenie /tmp..."
sudo rm -rf /tmp/*

echo "📊 [6/6] Status dysku po cleanupie:"
df -h | tee /tmp/disk-usage.txt
echo "✅ Cleanup zakończony pomyślnie!"
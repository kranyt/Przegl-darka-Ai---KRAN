#!/bin/bash
# DziobMc - start serwera (Linux / macOS)
# Wrzuć tu plik server.jar (Paper / Purpur / Vanilla 1.21 – 1.21.4)
cd "$(dirname "$0")"
while true; do
  java -Xms2G -Xmx4G -XX:+UseG1GC -jar server.jar nogui
  echo "Serwer wyłączony. Restart za 5 sekund (Ctrl+C aby anulować)..."
  sleep 5
done

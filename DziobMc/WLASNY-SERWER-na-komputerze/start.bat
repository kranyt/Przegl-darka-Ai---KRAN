@echo off
title DziobMc - Dziob.fun
REM Wrzuc tu plik server.jar = Paper 1.21.4 (wymaga Java 21)
:start
java -Xms2G -Xmx4G -XX:+UseG1GC -jar server.jar nogui
echo Serwer wylaczony. Restart za 5 sekund...
timeout /t 5
goto start

#!/bin/bash
# Buduje DziobEarth.jar. Kompiluje się na zaślepkach API (stubs/), które NIE trafiają do jara –
# prawdziwe klasy Bukkit/Paper dostarcza serwer.
set -e
cd "$(dirname "$0")"
rm -rf build && mkdir -p build/stubs build/classes
javac -nowarn --release 21 -d build/stubs $(find stubs -name "*.java")
javac --release 21 -Xlint:all -cp build/stubs -d build/classes $(find src/main/java -name "*.java")
cp -r src/main/resources/* build/classes/
(cd build/classes && jar cf ../DziobEarth.jar .)
ls -la build/DziobEarth.jar

#!/bin/bash
#!/usr/bin/bash
filename="PPIDejecutarBTserver.txt"
while read  line; do
    name="$line"
    echo "Name read from file - $name"
    kill -9 $name
done < "$filename"


rm /home/pi/HB/PPIDejecutarBTserver.txt
    
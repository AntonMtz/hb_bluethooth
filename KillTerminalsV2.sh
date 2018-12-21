#!/bin/bash
#!/usr/bin/bash
filename="allPids.txt"
while read  line; do
    name="$line"
    echo "Name read from file - $name"
    kill -9 $name
done < "$filename"


rm /home/pi/HB/allPids.txt
    
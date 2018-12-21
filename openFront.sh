#!/bin/bash
a="$(xdotool getactivewindow)"
COUNTER=1
echo $a  
 
 
   

xdotool search --class "terminal" | while read id
do

      if [ $COUNTER -eq 2  ]; then   

         xdotool windowactivate "$id"
         echo "in wondows   " 
      fi 
           COUNTER=$[$COUNTER +1]


done   
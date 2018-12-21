#!/bin/bash
a="$(xdotool getactivewindow)"
COUNTER=1
echo $a  
 

   

xdotool search --class "terminal" | while read id
do

   if [ "$id" -ne "$a" ]; then
       echo $id "no es igual a " $a


       xdotool windowactivate $id &>/dev/null
       c=$(xdotool getactivewindow)
       echo "pid " pidof $c 
         
      if [ $COUNTER -gt 2 ]; then   
                xdotool key alt+F4
                sleep 0.2
      fi 
           COUNTER=$[$COUNTER +1]


         
         
   fi 
done   
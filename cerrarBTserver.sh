
pidInicio1=`cut -d  " " -f 1  /home/pi/HB/PPIDejecutarBTserver.txt`
echo "Contenido del archivo1: "$pidInicio1
kill -9 $pidInicio1
rm /home/pi/HB/PPIDejecutarBTserver.txt


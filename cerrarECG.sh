
pidInicio1=`cut -d  " " -f 1  /home/pi/HB/PPIDejecutarECG.txt`
echo "Contenido del archivo1: "$pidInicio1
kill -9 $pidInicio1
rm /home/pi/HB/PPIDejecutarECG.txt


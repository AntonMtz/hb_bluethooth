
pidInicio1=`cut -d  " " -f 1  /home/pi/HB/PPIDservidorRTSP.txt`
echo "Contenido del archivo1: "$pidInicio1

pidInicio2=`cut -d  " " -f 1  /home/pi/HB/PPIDejecutarServidorRTSP.txt`
echo "Contenido del archivo2: "$pidInicio2


pidInicio3=`cut -d  " " -f 1  /home/pi/HB/PPIDejecutarPlayStream.txt`
echo "Contenido del archivo2: "$pidInicio3




kill -9 $pidInicio1
kill -9 $pidInicio2
kill -9 $pidInicio3

rm /home/pi/HB/PPIDservidorRTSP.txt
rm /home/pi/HB/PPIDejecutarServidorRTSP.txt
rm /home/pi/HB/PPIDejecutarPlayStream.txt






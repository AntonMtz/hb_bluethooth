echo "$$" > PPIDejecutarServidorRTSP.txt
echo "$$" >> allPids.txt
ffserver -f /etc/ffserver.conf & ffmpeg -threads 2 -r 5 -s 320X240 -f video4linux2 -i /dev/video0 http://localhost:8091/feed1.ffm 


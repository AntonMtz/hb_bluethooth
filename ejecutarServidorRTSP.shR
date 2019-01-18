echo "$$" > PPIDejecutarServidorRTSP.txt
echo "$$" >> allPids.txt
ffserver -f /etc/ffserver.conf & ffmpeg -r 15   -s 640X480 -f video4linux2 -i /dev/video0 http://localhost:8091/feed1.ffm 


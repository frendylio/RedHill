
#!/bin/bash
gnome-terminal -- /bin/sh -c 'sim_vehicle.py -v ArduCopter -l 21.296713,-157.815434,0,0 -I 1 --sysid=1 --out=127.0.0.1:14750'
gnome-terminal -- /bin/sh -c 'sim_vehicle.py -v ArduCopter -l 21.296718,-157.816711,0,0 -I 2 --sysid=2 --out=127.0.0.1:14760'
gnome-terminal -- /bin/sh -c 'mavproxy.py --master=udp:127.0.0.1:14560 --master=udp:127.0.0.1:14570 --source-system=1 --console --map'
# Sleep 10 second since simulations needs to load first ...
sleep 10
gnome-terminal -- /bin/sh -c 'python test.py 127.0.0.1:14750 127.0.0.1:14760' #; exec bash'

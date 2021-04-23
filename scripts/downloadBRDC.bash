# This script is to download the BRDC file from NASA to run spoofing
wget --no-check-certificate "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/$(date -u +%Y)/brdc/brdc$(date -u +%j0.%g)n.gz"
uncompress brdc$(date -u +%j0.%g)n.gz
./gps-sdr-sim -e brdc$(date -u +%j)0.$(date -u +%g)n -l 21.3999500-159.819726,20 -o gpssim.bin -d 60

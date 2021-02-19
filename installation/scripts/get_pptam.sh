#!/bin/bash 

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=PPTAM%20Setup
echo "  ____  ____ _____  _    __  __   ____       _               ";
echo " |  _ \|  _ \_   _|/ \  |  \/  | / ___|  ___| |_ _   _ _ __  ";
echo " | |_) | |_) || | / _ \ | |\/| | \___ \ / _ \ __| | | | '_ \ ";
echo " |  __/|  __/ | |/ ___ \| |  | |  ___) |  __/ |_| |_| | |_) |";
echo " |_|   |_|    |_/_/   \_\_|  |_| |____/ \___|\__|\__,_| .__/ ";
echo "                                                      |_|    ";

cd ~

# Install Grafana
# sudo apt-get install -y apt-transport-https
# sudo apt-get install -y software-properties-common wget
# wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
# echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
# sudo apt-get update
# sudo apt-get install grafana -y

# Cloning PPTAM from github
git clone --depth 1 https://github.com/pptam/pptam-tool.git

cd pptam-tool
echo Done.
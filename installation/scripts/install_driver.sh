#!/bin/bash 
set -e

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=Driver%20setup
echo "  ____       _                           _               ";
echo " |  _ \ _ __(_)_   _____ _ __   ___  ___| |_ _   _ _ __  ";
echo " | | | | '__| \ \ / / _ \ '__| / __|/ _ \ __| | | | '_ \ ";
echo " | |_| | |  | |\ V /  __/ |    \__ \  __/ |_| |_| | |_) |";
echo " |____/|_|  |_| \_/ \___|_|    |___/\___|\__|\__,_| .__/ ";
echo "                                                  |_|    ";

# Docker swarm installation and writing join token into file
docker swarm init --advertise-addr $1 --listen-addr $1
docker swarm join-token -q worker > /vagrant/.join-token-worker

# Java installation
apt install -y openjdk-8-jdk ant python3.7
echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/" >> /etc/environment

# Making sure python works
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
sudo update-alternatives --set python /usr/bin/python3.6

# Installion of Jupyter Notebook
cd /home/vagrant
echo Downloading Miniconda...
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p /home/vagrant/miniconda
conda config --set auto_activate_base false

echo export PATH=/home/vagrant/miniconda/bin:$PATH >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc

conda install -c r r-essentials -y
conda install -c anaconda jupyter -y

cp -r /vagrant/configuration/jupyter /home/vagrant/.jupyter
# jupyter notebook --generate-config
# jupyter notebook password 

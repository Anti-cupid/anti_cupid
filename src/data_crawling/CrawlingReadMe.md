install requirements.

installed tor reasoned response timeout.

''''
sudo apt-get install tor

sudo vi /etc/tor/torrc
SocksPort 9050 (# 제거)

sudo service tor restart

pip install requests[socks]
''''
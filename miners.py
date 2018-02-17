import socket, urllib, json
from device import *
username          = 'LegionMetal'
workername        = socket.gethostname()
password              = 'legion1'

ccminer = '/home/miner/miners/ccminer/ccminer'
equihash = '/home/miner/miners/equihash/miner'
neoscrypt = '/home/miner/miners/nsgminer/nsgminer'
lyra2v2 = '/home/miner/miners/vertminer-nvidia/vertminer'


# All miner configuration here.  Add/Change/Delete pairs as nessisary
#Altcommunity
#Bytecoin 
BitcoinGold           = '%s --server us-east1.equihash-hub.miningpoolhub.com --user %s.%s --pass x --port 20595 --api' % (equihash, username, workername)
DGBGroestl           = '%s -a myr-gr -o stratum+tcp://hub.miningpoolhub.com:20499 -u %s.%s -p x' % (ccminer, username, workername)
#Decred
#DigitalNote
#Electroneum
Ethereum              = 'ethminer --opencl-device 0 -G -S us-east.ethash-hub.miningpoolhub.com:20535 -O %s.%s:x' % (username, workername)
EthereumClassic       = 'ethminer --opencl-device 0 -G -S us-east.ethash-hub.miningpoolhub.com:20555 -O %s.%s:x' % (username, workername)
Expanse               = 'ethminer --opencl-device 0 -G -S us-east.ethash-hub.miningpoolhub.com:20565 -O %s.%s:x' % (username, workername)
Feathercoin           = '%s -o stratum+tcp://hub.miningpoolhub.com:20510 -u %s.%s -p x' % (neoscrypt, username, workername)
GroestlCoin           = '%s -a groestl -o stratum+tcp://hub.miningpoolhub.com:20486 -u %s.%s -p x' % (ccminer, username, workername)
#Halcyon
#Hush
#Karbowanec
#Komodo
#LBRY
#Metaverse
Monacoin              = '%s -o stratum+tcp://hub.miningpoolhub.com:20593 -u %s.%s -p x -d %s' % (lyra2v2, username, workername, device)
Monero                = '%s -a cryptonight -o stratum+tcp://us-east.monero.miningpoolhub.com:20580 -u %s.%s -p x' % (ccminer, username, workername)
Musicoin              = 'ethminer --opencl-device 0 -G -S us-east.ethash-hub.miningpoolhub.com:20585 -O %s.%s:x' % (username, workername)
MyriadGroestl        = '%s -a myr-gr -o stratum+tcp://us-east1.myriadcoin-groestl.miningpoolhub.com:20479 -u %s.%s -p x' % (ccminer, username, workername)
#Orbitcoin
#PascalLite
#Pascalcoin
#Phoenixcoin
#Pirl
#Sibcoin
#Soilcoin
#Sumokoin
#Ubiq
Vertcoin              = '%s -o stratum+tcp://hub.miningpoolhub.com:20507 -u %s.%s -p x -d %s' % (lyra2v2, username, workername, device)
Zcash                 = '%s --server us-east1.zcash.miningpoolhub.com --user %s.%s --pass x --port 20570 --api' % (equihash, username, workername)
Zclassic              = '%s --server us-east.equihash-hub.miningpoolhub.com --user %s.%s --pass x --port 20575 --api --Fee 0' % (equihash, username, workername)
Zencash               = '%s --server us-east.equihash-hub.miningpoolhub.com --user %s.%s --pass x --port 20594 --api' % (equihash, username, workername)

def equihash_api():
    try:
        response = urllib.urlopen('http://127.0.0.1:42000/getstat')
    except:
        print("Unable to connect to miner API")
        return "{}"
    return response.read()

mine_map = { 'ZCL': Zclassic,
             'ZEN': Zencash,
             'BTG': BitcoinGold,
             'ZEC': Zcash,
             'MONA': Monacoin,
             'VTC': Vertcoin,
             'ETH': Ethereum,
             'FTC': Feathercoin, }

mine_api = { 'ZCL': equihash_api,
             'ZEC': equihash_api,
             'ZEN': equihash_api,
             'BTG': equihash_api,
           }

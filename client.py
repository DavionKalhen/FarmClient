#!/usr/bin/env python

import socket, time, fcntl, os, select, datetime, subprocess, sys
import subprocess
try:
    from miners import *    
except ImportError:
    ps = subprocess.Popen(('lspci'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', 'NVIDIA'), stdin=ps.stdout, stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', 'VGA'), stdin=grep.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('wc', '-l'), stdin=grep.stdout)
    print "There are compatable %s devices" % output.strip()
    with open('device.py', 'w') as the_file:
        devices = int(output.strip())
        devl = ""
        for i in range(0, devices):
            devl += "%d," % i
        if devl[-1] == ',':
            devl = devl[:-1]
        the_file.write('device = "%s"' % devl)
    from miners import *

mining = 'None'
TCP_IP = 'www.nashmoving.com'
TCP_PORT = 5001
BUFFER_SIZE = 20
PING = 60

register = "register %s" % socket.gethostname()
update = "update %s" % mining
response = { 
                "welcome" : register,
           }
s = None

def pipe_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

def reconnect():
    global s
    retries = 1
    while 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "Socket successfully created."
            s.connect((TCP_IP, TCP_PORT))
            print "Connected to Server."
            s.setblocking(0)
            print "Set to non-blocking"
            break
        except socket.error as err:
            print("Socket failed with error %s" %(err))
            print("Retry #%d in 30 seconds." % retries)
            retries += 1
            time.sleep(30)

reconnect()
miner = None

def mine(token):
    global miner, mining
    print("Switching miner")
    if miner is not None:
        try:
            miner.kill()
        except OSError: #Most likely already killed.
            pass
        try:
            output, errors = miner.communicate()
            print(output)
            print(errors)
            time.sleep(30) #give time for api socket to close
        except ValueError: #Already ded.
            pass
    try:
        tomine = mine_map[token]
    except KeyError:
        print("Got unknown token from server. %s" % token)
    else:
        miner = subprocess.Popen(tomine.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Now mining %s" % token)
        mining = token
    
outbuf = []
start_mining = False

def socket_send(s, text):
    try:
        s.send(text + "\r\n")
    except socket.error as e:
        print("Server connection lost. Could not send %s.\n%s\nAttempting reconnect" % (text, e))
        reconnect()

def socket_recv(s, size):
    try:
        data = s.recv(size)
    except socket.error as e:
        print("Server connection lost. Unable to recv() data.\n%s\nAttempting reconnect." % e)
        reconnect()
        return ""
    return data
last_start = datetime.datetime.now()
ping = PING
while 1:
    ready = select.select([s], [], [], 1)
    if ready[0]:
        data = socket_recv(s, BUFFER_SIZE)

        if data.startswith('mine'):
            token = data[data.find(' '):].strip()
            start_mining = True
            print("Server updated us. Most profitable coin to mine is %s." % token)
            if token == mining:
                print("We are already minging %s" % token)
            else:
                mine(token)
        elif data.startswith('stats'):
            socket_send(s, 'stats %s' % mine_api[mining]())
        elif data.startswith('restart'):
            print("Server thinks we need to restart our miner.")
            if datetime.datetime.now() - last_start < datetime.timedelta(minutes=5):
                print("We restarted the miner less than 5 minutes ago. We shall wait.")
            else:
                mine(mining)
        elif data.startswith('update'):                
            print("Server thinks we need to update our client. Updating.")
            if miner:
                miner.kill()
            p = subprocess.Popen('git pull'.split(' '),
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
            (out, err) = p.communicate()
            print(out)
            print(err)
            print("Client update attempted.")
            print("Restarting client.")
            p = subprocess.Popen('./client.py',
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
            sys.exit(1)
        elif data.startswith('stop'):
            print("Server thinks we need to stop")
            if miner:
                miner.kill()
        elif data.startswith('smi'):
            print("Server has requested SMI")
            p = subprocess.Popen('nvidia-smi', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (out, err) = p.communicate()
            socket_send(s, 'smi %s' % out.replace('\n', '[/'))
        elif data.startswith('pong'):
            print("Server ponged us.")
        else:
            try:
                resp = response[data.lower().strip()]
                socket_send(s, resp)
                print("Responding with %s" % resp)
            except KeyError:
                print("Got unknown response from server. %s" % data)
                #Check for disconnect.
                socket_send(s, "ping")

    if start_mining and miner.poll() is not None:
        print("Miner stopped, restarting.")
        mine(mining)
    elif miner:
        out = pipe_read(miner.stdout)
        err = pipe_read(miner.stderr)
        if len(out.strip()) > 0:
            print(out)
        if len(err.strip()) > 0:
            print(err)

    ping -= 1
    
    if ping <= 0:
        socket_send(s, 'ping')
        ping = PING
    
s.close()

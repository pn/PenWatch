#!/usr/bin/env python

STORE_DIR="/proc/scsi/usb-storage"

AUTHORIZED= {
    # 'SerialNumber':'DeviceName'
    '08135200B2971D04':'RedPen',
}

import os,re,time,subprocess

def dSerByName(name):
    for k in AUTHORIZED.keys():
        if AUTHORIZED[k]==name:
            return k
    return ""


def get_auth_devices():
    #returns list of serial numbers of mounted devices that are authorized
    devices = {}
    try:
       for f in os.listdir(STORE_DIR):
           did = re.findall("Serial Number: ([A-Za-z0-9]+)", file("%s/%s" % (STORE_DIR,f), "r").read() )
           if len(did)>0 and did[0] in AUTHORIZED.keys():
               devices[did[0]] = AUTHORIZED[did[0]]
    except:
        pass
    return devices


def watch( period=1, onMountHash=None, onDemountHash=None ):
    last_seen = get_auth_devices()
    print "currently mounted authorized devices: %s\n\nstarting to watch..." % (last_seen)

    def def_onMount(dev):
        print "New device has been mounted: %s" % dev

    def def_onDemount(dev):
        print "Device %s has been unmounted" % dev
    
    if onMountHash == None: 
        default_method_hash = {}
        for k in AUTHORIZED.keys():
            default_method_hash[k] = def_onMount
        onMountHash = default_method_hash

    if onDemountHash == None: 
        default_method_hash = {}
        for k in AUTHORIZED.keys():
            default_method_hash[k] = def_onDemount
        onDemountHash = default_method_hash

    while True:
        try:
            for d in get_auth_devices().keys():
                if not d in last_seen.keys(): #new device plugged in
                    onMountHash[d](d)
            for d in last_seen.keys():
                if not d in get_auth_devices().keys(): #device plugged off
                    onDemountHash[d](d)
            last_seen = get_auth_devices()
            time.sleep(period)
        except KeyboardInterrupt:
            print "Exiting"
            break


def onRedPenMount(dev):  
    print "Device %s has been mounted" % (dev)
    print "UnLocking screen..."
    subprocess.call( ['gnome-screensaver-command', '--deactivate'] )


def onRedPenDeMount(dev):
    print "Device %s has been demounted" % (dev)
    print "Locking screen..."
    subprocess.call( ['gnome-screensaver-command', '--lock'] )


if __name__ == "__main__":
    watch(1,
        {dSerByName('RedPen'):onRedPenMount},
        {dSerByName('RedPen'):onRedPenDeMount}
    )

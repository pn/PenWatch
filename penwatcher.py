#!/usr/bin/env python

STORE_DIR="/proc/scsi/usb-storage"
AUTHORIZED= [
    '08135200B2971D04',
]

import os,re,time

def get_auth_devices():
    #returns list of serial numbers of mounted devices that are authorized
    devices = []
    for f in os.listdir(STORE_DIR):
        did = re.findall("Serial Number: ([A-Za-z0-9]+)", file("%s/%s" % (STORE_DIR,f), "r").read() )
        if len(did)>0 and did[0] in AUTHORIZED: 
            devices.append(did[0])
    return devices



def watch( period=1, onMount=None, onDemount=None):
    last_seen = get_auth_devices()
    print "currently mounted authorized devices: %s\n\nstarting to watch..." % (last_seen)

    def def_onMount(dev):
        print "New device has been mounted: %s" % dev

    def def_onDemount(dev):
        print "Device %s has been unmounted" % dev
    
    if onMount == None: onMount = def_onMount
    if onDemount == None: onDemount = def_onDemount

    while True:
        for d in get_auth_devices():
            if not d in last_seen: #new device plugged in
                onMount(d)
        for d in last_seen:
            if not d in get_auth_devices(): #device plugged off
                onDemount(d)
        last_seen = get_auth_devices()
        time.sleep(period)

if __name__ == "__main__":
    watch()

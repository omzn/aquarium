#!/usr/bin/python

import sys
import time
from time import strftime
import os
import httplib
import urllib
import json
 
def getAquaData():
    conn = httplib.HTTPConnection("se.is.kit.ac.jp")
    conn.request("GET", "/aquarium/aquajson.cgi")
    response = conn.getresponse()
    #print response.status, response.reason
    data = response.read()
    conn.close()
    return json.loads(data)

def main():
    now = time.localtime()
    print "<< Aquarium status on %s >>" % strftime("%Y-%m-%d %H:%M",now)

    aquaJson = getAquaData()
    #print json.dumps(aquaJson, sort_keys = True, indent = 4)

    print "[Temperature]"
    temp = aquaJson['temp']
    tempkeys = temp.keys()
    tempkeys.sort()
    for k in tempkeys:
        print "  %7s: %4s 'C" % (k, temp[k]['current'])

    print "[Pressure]"
    print "  %s hPa" % aquaJson['pressure']['current']

    print "[Humidity]"
    print "  %s %%" % aquaJson['humidity']['current']

    print "[Lightings]"
    for k in ['light1','light2']:
        data = aquaJson[k]
        if data['status'] == "off":
            print "  %6s: %3s (will turn on at %s)" % (k, data['status'], data['ontime'])
        else:
            print "  %6s: %3s (will turn off at %s)" % (k, data['status'], data['offtime'])

    print "[Coolers]"
    for k in ['ac1','fan1','fan2','fan3']:
        data = aquaJson[k]
        print "  %4s: %3s (since %s)" % (k,aquaJson[k]['current'],aquaJson[k]['time'])

    print "[Droid]"
    print "  Mode: %s" % aquaJson['droid']['mode']
    print "  Camera: %s" % aquaJson['droid']['camera']
    print "  Position: H %2s V %2s S %3s,%3s" % (aquaJson['droid']['tank_pos'],aquaJson['droid']['lift_pos'],aquaJson['droid']['swing_h'],aquaJson['droid']['swing_v'])
    print "[Feed in %s]" % aquaJson['feed']['date']
    print "  tank1: %s" % aquaJson['feed']['tank_0']
    print "  tank2: %s" % aquaJson['feed']['tank_1']
    print "  tank3: %s" % aquaJson['feed']['tank_2']
    print "  tank4: %s" % aquaJson['feed']['tank_3']

if __name__ == '__main__':
    main()

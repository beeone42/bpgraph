#!/usr/bin/env python
import requests, time, pyspeedtest, os, sys, json, rrdtool, tempfile, shutil, subprocess, pyping

def open_and_load_config(fname):
    if os.path.exists(fname):
        with open(fname, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print "File [%s] doesn't exist, aborting." % (fname)
        sys.exit(1)

def check_files(config):
    if not os.path.exists(config['graphs_root']):
        print "graphs_root [%s] doesn't exist, aborting." % (config['graphs_root'])
        sys.exit(1)
    if not os.path.exists(config['rrd_file']):
        print "rrd_file [%s] doesn't exist, we need to create it..." % (config['rrd_file'])
        # rrdtool create bp.rrd --start now-1d DS:nb:GAUGE:600:0:U RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:96 RRA:AVERAGE:0.5:12:168 RRA:AVERAGE:0.5:72:124 RRA:AVERAGE:0.5:288:366
        rrdtool.create(str(config['rrd_file']),
                       '--start', 'now-1d',
                       'DS:nb:GAUGE:600:0:U',
                       'RRA:AVERAGE:0.5:1:288',
                       'RRA:AVERAGE:0.5:3:96',
                       'RRA:AVERAGE:0.5:12:168',
                       'RRA:AVERAGE:0.5:72:124',
                       'RRA:AVERAGE:0.5:288:366'
                       )
        print "rrd_file [%s] created." % (config['rrd_file'])
    if not os.path.exists(config['graphs_root'] + '/index.html'):
        print "index [%s]/index.html doesn't exist, we need to create it..." % (config['graphs_root'])
        shutil.copyfile('index.html', config['graphs_root'] + '/index.html')

def update_rrd(config, speed):
    rrdtool.update(str(config['rrd_file']), 'N:' + str(speed))

def graph_rrd(config, inter, suffix):
    rrdtool.graph(
        str(config['graphs_root']) + 'bp' + suffix + '.png',
        'COMMENT:bp' + suffix + '    ',
        '-E', '-w', '480', '-h', '180', '--step', '300',
        '--start', 'now-' + inter, '--end', 'now',
        'DEF:occupees=' + str(config['rrd_file']) + ':nb:AVERAGE',
        'CDEF:div=occupees,4,/',
        'AREA:div#FFFF00',
        'AREA:div#FFC020::STACK',
        'AREA:div#FF8040::STACK',
        'AREA:div#FF4020::STACK',
        'LINE2:occupees#FF0000:B/s'
        )

def ping(config):
    c = int(config['ping_count'])
    r =  pyping.ping('8.8.8.8', count = c)
    res = c - r.packet_lost
    return res

def iperf(config):
    tmp = subprocess.check_output(["iperf", "-c", config['iperf_srv'], "-p", config['iperf_port'], "-t", "10", "-y", "C"])
    res = tmp.split(',')[-1].strip()
    return res

def get_speed(config):
    speed = 0
    if (config['url'] == "ping"):
        speed = ping(config)
        return speed
    if (config['url'] == "iperf"):
        speed = iperf(config)
        return speed
    if (config['url'] == "speedtest"):
        speedtest = pyspeedtest.SpeedTest()
        speed = speedtest.download()
        return speed
    if (speed == 0):
        start = time.clock()
        r = requests.get(config['url'], stream = False, timeout=1)
        end = time.clock()
        l = r.headers.get('content-length')
        t = end - start
        if (l is None) or (t == 0):
            return 0
        speed = int(l) / t
    return speed

if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.argv[0]))
    config = open_and_load_config("config.json")
    check_files(config)
    speed = get_speed(config)
    print speed
    update_rrd(config, speed)
    graph_rrd(config, '8h', '')
    graph_rrd(config, '1d', '-day')
    graph_rrd(config, '1w', '-week')
    graph_rrd(config, '31d', '-month')
    graph_rrd(config, '1y', '-year')

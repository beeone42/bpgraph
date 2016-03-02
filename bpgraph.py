import pyspeedtest, os, sys, json, rrdtool, tempfile

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

config = open_and_load_config("config.json")
check_files(config)
speedtest = pyspeedtest.SpeedTest()
speed = speedtest.download()
print speed
rrdtool.update(str(config['rrd_file']), 'N:' + str(speed * 1000.0))


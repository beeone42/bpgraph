# bpgraph

Test your available download bandwidth with speedtest.net and generate graphs with rrdtool

![alt tag](https://cloud.githubusercontent.com/assets/11945268/13462460/d36821da-e087-11e5-9ab6-528deb2a82bf.png)

## Requirements

- pyspeedtest: https://pypi.python.org/pypi/pyspeedtest/1.2
- python-rrdtool: https://pypi.python.org/pypi/python-rrdtool/1.4.7

## Installation

```
apt-get install python-dev python-pip libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev
pip install -r requirements.txt
```

add this to your crontab

```
*/5 *  *   *   *     /home/user/bpgraph/bpgraph.py > /dev/null &
```

## Usage

Just let cron run the script and watch the graph on your webserver

`http://localhost/bp/`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


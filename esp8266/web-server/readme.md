# Web server applications

These applications use https://github.com/pfalcon/picoweb. To install this package either install picoweb using `upip` on 
the board or use https://github.com/peterhinch/micropython-samples/blob/master/micropip/micropip.py and run: 
``` 
mkdir libraries
micropip.py install -p libraries picoweb
ampy -p /dev/ttyUSB0 put libraries /lib
```
(`ampy` can be installed with `pip install adafruit-ampy`)


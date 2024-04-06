# ESP with MicroPython

This repository is about working on the ESP8266 with MicroPython (in particular the NodeMCU dev board).



## Initial setup

### Python venv
1. Install `python3`
2. Create a virtualenv using `python -m venv .venv`
3. Activate the virtualenv using `.\.venv\Scripts\Activate.ps1`
4. Install the requirements using `pip install -r host-requirements.txt`


## CircuitPython deps
```shell
circup install -r device-requirements.txt
```


# REPL
```shell
// Windows
plink -serial \\.\COM5 -sercfg 115200,8,1,N,N
// OSX
screen /dev/cu.xxxxxxx
```


## Sample MQTT Invokes
```
mqtt publish -t alertdisplay/setTimer -m pan,60
mqtt publish -t alertdisplay/removeTimer -m pan
mqtt publish -t alertdisplay/setIcon -m chicken,true
mqtt publish -t alertdisplay/setPower -m true
```

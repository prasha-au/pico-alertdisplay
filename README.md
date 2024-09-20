# Pico AlertDisplay

A CircuitPython project to integrate a simple P5 LED Panel with my [Homenode](https://prasha.au/project/homenode) automation system.

A Pi Pico W listens for MQTT messages and shows:
- timers from Google Home
- the weather
- other various alerts from the system as icons


## Preview

https://github.com/user-attachments/assets/800a4657-f4b4-47d5-b7f3-ee6615eddd4a


## Initial setup

### Python venv
1. Install `python3`
2. Create a virtualenv using `python -m venv .venv`
3. Activate the virtualenv using `.\.venv\Scripts\Activate.ps1`
4. Install the requirements using `pip install -r host-requirements.txt`


### CircuitPython Device Deps
```shell
circup install -r device-requirements.txt
```


## Developing

Using REPL is the best way to quickly test things. The [displaytest.py](./src/displaytest.py) file has rough code for quickly displaying things.

### REPL
```shell
// Windows
plink -serial \\.\COM5 -sercfg 115200,8,1,N,N
// OSX
screen /dev/cu.xxxxxxx
```



### Sample MQTT Invokes
```pip i
mqtt publish -t alertdisplay/setTimer -m pan,60
mqtt publish -t alertdisplay/removeTimer -m pan
mqtt publish -t alertdisplay/setIcon -m chicken,true
mqtt publish -t alertdisplay/setPower -m true
```


### Screen Item Layouts
```
I I W         // (x: (2, 22, 45), y: 1)
I I W         // (x: (2, 22, 45), y: 16)

T T T
I I I

T T T
T T T
```


### Creating Icons

You can use [Piskel](https://www.piskelapp.com/) and import the BMP files to edit them.

Piskel can export to PNG and you can use the command below (on OSX) to convert it to BMP.

```bash
sips -s format jpeg test.png --out test.jpg
```




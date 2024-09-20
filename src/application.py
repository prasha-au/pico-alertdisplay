import adafruit_minimqtt.adafruit_minimqtt as MQTT
import os
import wifi
import socketpool
import display
import asyncio
import time


DEVICE_ID = 'alertdisplay'

class Timer:
  id = None
  expiry = None

  def __init__(self, id, seconds):
    self.id = id
    self.expiry = time.monotonic() + seconds

  def get_seconds_left(self):
    return self.expiry - time.monotonic()

  def is_valid(self):
    return self.get_seconds_left() > -10

  def to_display_str(self):
    seconds_left = self.get_seconds_left()
    if seconds_left <= 0:
      return "! %s" % self.id
    else:
      seconds = seconds_left % 3600
      minutes = seconds // 60
      seconds %= 60
      return "%02d:%02d %s" % (minutes, seconds, self.id)

  def to_display_color(self):
    seconds_left = self.get_seconds_left()
    if seconds_left <= 10:
      return 0xff0000
    elif seconds_left <= 30:
      return 0xff9600
    else:
      return 0x444444


timers = {}

async def update_timers():
  global timers
  while True:
    sorted_timers = sorted(timers.values(), key=lambda x: x.get_seconds_left())

    if len(sorted_timers) >= 2:
      display.set_timer_1(sorted_timers[0].to_display_str(), sorted_timers[0].to_display_color())
      display.set_timer_2(sorted_timers[1].to_display_str(), sorted_timers[1].to_display_color())
    elif len(sorted_timers) == 1:
      display.set_timer_1(sorted_timers[0].to_display_str(), sorted_timers[0].to_display_color())
      display.set_timer_2("")
    else:
      display.set_timer_1("")
      display.set_timer_2("")

    display.refresh_display()
    await asyncio.sleep(0.2)



def on_message(client, topic, message):
  action = topic.replace(f'{DEVICE_ID}/', '')
  print(f'New action {action} with message {message}')

  if action == 'setPower':
    display.set_power(message == 'true')
  elif action == 'addTimer':
    global timers
    timer_id, timer_seconds = message.split(",")
    timers[timer_id] = Timer(timer_id, int(timer_seconds))
  elif action == 'removeTimer':
    global timers
    if message in timers:
      del timers[message]
  elif action == 'setIcon':
    icon, is_shown = message.split(',')
    is_shown = is_shown == 'true'
    display.set_icon_visibility(icon, is_shown)
  elif action == 'setWeather':
    temp, temp_pct, icon = message.split(',')
    display.set_weather(int(temp), int(temp_pct), icon)


async def mqtt_event_loop():
  print("Starting MQTT event loop")
  pool = socketpool.SocketPool(wifi.radio)

  mqtt_client = MQTT.MQTT(
    broker=os.getenv('MQTT_URL'),
    socket_pool=pool,
    socket_timeout=0.2,
    connect_retries=1,
  )

  mqtt_client.on_message = on_message

  print("Attempting to connect to %s" % mqtt_client.broker)

  while True:
    try:
      mqtt_client.connect()
      break
    except MQTT.MMQTTException as e:
      print('failed connect')
      time.sleep(5)

  mqtt_actions = ['setPower', 'addTimer', 'removeTimer', 'setIcon', 'setWeather']
  for action in mqtt_actions:
    print(f'Subscribing to {DEVICE_ID}/{action}')
    mqtt_client.subscribe(f'{DEVICE_ID}/{action}')

  mqtt_client.publish(f'{DEVICE_ID}/hello', '{}')

  while True:
    mqtt_client.loop(0.2)
    await asyncio.sleep(1)



async def application():
  display.init_display()

  wifi.radio.hostname = 'pico-alertdisplay'

  wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

  print("Starting wifi")

  mqtt_task = asyncio.create_task(mqtt_event_loop())

  display_task = asyncio.create_task(update_timers())

  print("Gathering tasks")
  await asyncio.gather(
    mqtt_task, display_task
  )

def run_application():
  asyncio.run(application())


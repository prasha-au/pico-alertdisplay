import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import os
import wifi
import socketpool
import time
import display
import asyncio


class Timer:
  id = None
  seconds = 0

  def __init__(self, id, seconds):
    self.id = id
    self.seconds = seconds

  def decrement(self):
    self.seconds -= 1

  def is_valid(self):
    return self.seconds > -10


  def to_display_str(self):
    if self.seconds <= 0:
      return "! %s" % self.id
    else:
      seconds = self.seconds % 3600
      minutes = seconds // 60
      seconds %= 60
      return "%02d:%02d %s" % (minutes, seconds, self.id)

  def to_display_color(self):
    if self.seconds <= 10:
      return 0xff0000
    elif self.seconds <= 30:
      return 0xff9600
    else:
      return 0x444444



timers = {}

async def update_timers():
  global timers
  while True:

    for timer in timers.values():
      timer.decrement()
      if not timer.is_valid():
        del timers[timer.id]

    sorted_timers = sorted(timers.values(), key=lambda x: x.seconds)

    if len(sorted_timers) > 0:
      display.set_line_1(sorted_timers[0].to_display_str(), sorted_timers[0].to_display_color())
    else:
      display.set_line_1("")
    if len(sorted_timers) > 1:
      display.set_line_2(sorted_timers[1].to_display_str(), sorted_timers[1].to_display_color())
    else:
      display.set_line_2("")

    await asyncio.sleep(1)



async def mqtt_event_loop():
  print("Starting MQTT event loop")
  pool = socketpool.SocketPool(wifi.radio)

  mqtt_client = MQTT.MQTT(
      broker=os.getenv('MQTT_URL'),
      socket_pool=pool,
  )


  def on_message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))
    if topic == "picotest/msg":
      display.set_line_1(message)
    elif topic == "picotest/setTimer":
      global timers
      timer_id, timer_seconds = message.split(",")
      timers[timer_id] = Timer(timer_id, int(timer_seconds))



  mqtt_client.on_message = on_message



  print("Attempting to connect to %s" % mqtt_client.broker)
  mqtt_client.connect()

  mqtt_topic = "picotest/msg"
  print("Subscribing to %s" % mqtt_topic)
  mqtt_client.subscribe(mqtt_topic)

  mqtt_topic = "picotest/setTimer"
  print("Subscribing to %s" % mqtt_topic)
  mqtt_client.subscribe(mqtt_topic)

  while True:
    mqtt_client.loop(1)
    await asyncio.sleep(0)




async def application():

  wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

  print("Starting wifi")

  timer_task = asyncio.create_task(update_timers())

  mqtt_task = asyncio.create_task(mqtt_event_loop())

  display.init_display()

  display_task = asyncio.create_task(display.get_display_task())



  print("Gathering tasks")
  await asyncio.gather(
    mqtt_task, display_task, timer_task
  )

def run_application():
  asyncio.run(application())


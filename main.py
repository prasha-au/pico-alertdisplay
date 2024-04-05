import time
import microcontroller
import application


try:
  application.run_application()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 10 seconds")
    time.sleep(10)
    microcontroller.reset()
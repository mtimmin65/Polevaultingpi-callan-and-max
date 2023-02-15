import time 
import board
import adafruit_mpu6050
import busio
import adafruit_mpl3115a2
from adafruit_display_text import label
import adafruit_displayio_ssd1306 
import terminalio 
import displayio
import digitalio



displayio.release_displays()

sda_pin = board.GP12  #sets up i2c
scl_pin = board.GP13
i2c = busio.I2C(scl_pin, sda_pin)  #sets up accelerometer
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
sda_pin = board.GP14  #sets up i2c
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)  #sets up accelerometer
current_time = time.monotonic() 
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=board.GP28)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

time_list = []
altitude_list = []  #sets up lists
xAccel_list = []
yAccel_list = []

 

while True:
    #    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
     #   print('Altitude: {0:0.3f} meters'.format(sensor.altitude))
      #  print("")
       # print(time.monotonic()) 
         altitude = sensor.altitude #read altitude
         altitude_list.append(sensor.altitude)
         print("Altitude: {0:0.3f} meters".format(altitude)) #print altitude readings
         xAccel = mpu.gyro[0]
         xAccel_list.append(mpu.gyro[0]) #saves values for collection later
         yAccel = mpu.gyro[0]
         yAccel_list.append(mpu.gyro[0]) #saves values for collection later
         print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
         time_list.append(time.monotonic())
         splash = displayio.Group()  #create the display group

         title = "ANGULAR VELOCITY" #add title block to display group
         text_area = label.Label(terminalio.FONT, text=title, color=0xFFFF00, x=5, y=5)
         splash.append(text_area) 

         title = f"Altitude: {sensor.altitude}" 
         text_area = label.Label(terminalio.FONT, text=title, color=0xFFFF00, x=5, y=15)
         splash.append(text_area)  
            
         title = f"y: {mpu.gyro[0]}" 
         text_area = label.Label(terminalio.FONT, text=title, color=0xFFFF00, x=5, y=30)
         splash.append(text_area) 

         title = f"z: {mpu.gyro[0]}" 
         text_area = label.Label(terminalio.FONT, text=title, color=0xFFFF00, x=5, y=45)
         splash.append(text_area)

         title = f"Time: {time.monotonic()}"
         text_area = label.Label(terminalio.FONT, text=title, color=0xFFFF00, x=5, y=60)
         splash.append(text_area)




         display.show(splash) #send display group to screen

         if time.monotonic() >20:
           
               break   #stop code taking values
print(time_list) 
print(altitude_list)
print(xAccel_list)
print(yAccel_list)

with open("/data.txt", "a") as datalog:
        for i in range(len(time_list)):
            input_values = f" {time_list[i]}, {altitude_list[i]}, {xAccel_list[i]}, {yAccel_list[i]}\n"
            datalog.write(input_values)  #save all time, altitude, temperature values in seperate lines in pico
            datalog.flush()

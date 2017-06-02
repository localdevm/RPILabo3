import RPi.GPIO as GPIO
import time
from datetime import datetime as dt

file = None
ToggleAlarm = False
Alarm = False
AlarmText = False
start = end = elapsed = 0
status = ""


GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(22, GPIO.FALLING, bouncetime=200)


def LED():
 if Alarm:
  GPIO.output(17, 1)
  time.sleep(0.2)
  GPIO.output(17, 0)
  time.sleep(0.2)


def button():
 global ToggleAlarm, Alarm, AlarmText, test, start, end, elapsed
 
 if Alarm: 
  if GPIO.input(22) == 1:
   start = time.time()
  if GPIO.input(22) == 0:
   end = time.time()
   elapsed = end - start
  if elapsed >= 5:
   Alarm = False
   AlarmText = False
   elapsed = 0
   print('Alarm Disengaged!')

 else:
  if GPIO.event_detected(22):
   if ToggleAlarm:
    ToggleAlarm = False
    print('Alarm Off')
   else:
    ToggleAlarm = True
    print('Alarm on')
  

def sensor():
 global AlarmText, LEDalarm, Alarm, Triggered
 if GPIO.input(27) and ToggleAlarm:
  if not AlarmText:
   try:
    timeStamp()
   finally:
    AlarmText = True
    print('ALARM! ALARM! ALARM! ALARM! ALARM!')
    Alarm = True
 else:
  GPIO.output(17, 0)


def timeStamp():
 try:
  file = open("testfile.txt", 'a')
 except IOError:
  print("Unable to create file on disk.")
  file.close()
 finally:
  file.write(time.strftime("%d-%m-%y %H-%M-%S")+'\n')
  file.close()
  time.sleep(0.1)


def deleteEntry():
 try:
  file = open("testfile.txt", 'r')
  lines = file.readlines()
  file.close()
  file = open("testfile.txt", 'w')
  print(lines)
  print('\n')
  for i in lines:
   print(i)
   ver = raw_input('moet ik deze lijn verwijderen ja = j, nee = n' + '\n')
   if ver != 'j':
    print("onthouden")
    file.write(i)

 except IOError:
  print("Unable to open file on disk.")
  file.close()
 finally:
  #file.truncate()
  file.close()
  time.sleep(0.1)
  changeOption()


def deleteEntries():
 try:
  f = open('testfile.txt', 'r')
  lines = f.readlines()
  f.close()
  f = open('testfile.txt','w')
  x = raw_input('Geef de begin datum in:')
  y = raw_input('Geef de eind datum in:')
  for i in lines:
   a = dt.strptime(i[0:17], "%d-%m-%y %H-%M-%S")
   print(a)
   b = dt.strptime(x, "%d-%m-%y %H-%M-%S")
   c = dt.strptime(y, "%d-%m-%y %H-%M-%S")
   if not(b <= a <= c):
    f.write(i)
   print(b)

 except IOError:
  print("Unable to open file on disk.")
  f.close()
 finally:
  f.close()
  time.sleep(0.1)
  changeOption()


def changeOption():
 global status
 status = raw_input('Use Alarm = "e", Timestamp per lijn = "r", Timestamp Range = "t" \n')


def chooseOption():
 if status == 'e':
  sensor()
  button()
  LED()
 if status == 'r':
  deleteEntry()
 if status == 't':
  deleteEntries()


def main():
 changeOption()
 while True:
  chooseOption()

try:
 if __name__ == "__main__":
  main()

except KeyboardInterrupt:
 print('Interrupted')

finally:
 GPIO.output(17, 0)
 print('closed session')

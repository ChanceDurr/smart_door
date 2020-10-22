from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
	output = reader.read()
	print(output)
finally:
	GPIO.cleanup()

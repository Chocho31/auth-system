#!/usr/bin/env python

import RPi.GPIO as GPIO
import mfrc522
import signal

continue_reading = True

# Capture SIGINT signal for cleanup when the sciprt is exited
def end_read(signal, frame):
	global continue_reading
	continue_reading = False
	GPIO.cleanup()

# Hook SIGINT
signal.signal(signal.SIGINT, end_read)

# Initialize object of class mfrc522 for access to rc522
reader = mfrc522.MFRC522()

print("mfrc522 test run")
print("Press Ctrl-C to stop")
print("Place tag to read...")

# main loop
# Continuously checks for rfid tags and if one is near it will get the UID
while continue_reading:

	# Scan for tags
	(status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

	# If tag is found
	if status == reader.MI_OK:
		print("Card detected")

	# Get UID of the tag
	(status, uid) = reader.MFRC522_Anticoll()

	# If UID was extracted successfully it is printed on the screen
	if status == reader.MI_OK:
		print("Card read UID: " + str(uid[0]) + ", "
			+ str(uid[1]) + ", " + str(uid[2]) + ", "
			+ str(uid[3]) + ", " + str(uid[4]))


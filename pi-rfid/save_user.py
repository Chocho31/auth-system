#!/usr/bin/env python

import mfrc522
import mysql.connector as mysql
import signal
import time
import RPi.GPIO as GPIO

continue_reading = True

def uid_to_string(uid):
	return "".join(map(str, uid))

# Capture SIGINT signal for cleanup when the sciprt is exited
def end_read(signal, frame):
	global continue_reading
	continue_reading = False
	GPIO.cleanup()

# Hook SIGINT
signal.signal(signal.SIGINT, end_read)

try:
	db_connection = mysql.connect(
		host='localhost',
		database='rfid',
		user='admin',
		password='33a55b88d'
	)

	cursor = db_connection.cursor(prepared=True)

	reader = mfrc522.MFRC522()

	print("Press Ctrl-C to stop")
	print("Place tag to read...")

	while continue_reading:
		(status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

		if status == reader.MI_OK:
			print("Card detected")

			(status, uid) = reader.MFRC522_Anticoll()

			if status == reader.MI_OK:
				card_uid = uid_to_string(uid)

				query = "SELECT id FROM users WHERE rfid_uid = %s"
				cursor.execute(query, (card_uid,))
				cursor.fetchall()

				if cursor.rowcount >= 1:
					print("User already exists.")
					overwrite = input("Do you want to overwrite? (y/n) ")

					if overwrite[0] == 'Y' or overwrite[0] == 'y':
						query = "UPDATE users SET name = %s WHERE rfid_uid = %s"
					else:
						print("Place tag to read...")
						continue

				else:
					query = "INSERT INTO users(name, rfid_uid) VALUES(%s, %s)"

				username = input("Enter user name: ")
				cursor.execute(query, (username, card_uid))

				db_connection.commit()

				print("User " + username + " saved")
				time.sleep(2)
 
			print("Place tag to read...")

except mysql.Error as error:
	print("MySQL connector error")

finally:
	if db_connection.is_connected():
		cursor.close()
		db_connection.close()
		print("MySQL connection is closed")


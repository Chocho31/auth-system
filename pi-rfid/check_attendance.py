#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import signal
import mfrc522
import mysql.connector as mysql

continue_reading = True

def uid_to_string(uid):
	return "".join(map(str, uid))

def end_read(signal, frame):
	global continue_reading
	continue_reading = False
	GPIO.cleanup()

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

				query = "SELECT id, name FROM users WHERE rfid_uid = %s"
				cursor.execute(query, (card_uid,))
				result = cursor.fetchone()

				if cursor.rowcount >= 1:
					print("Welcome " + result[1])
					query = "INSERT INTO attendance(user_id) VALUES(%s)"
					cursor.execute(query, (result[0],))
					db_connection.commit()

				else:
					print("Unrecognized card. User does not exist.")

			time.sleep(2)


except mysql.Error as error:
	print("MySQL connector error")

finally:
	if db_connection.is_connected():
		cursor.close()
		db_connection.close()
		print("MySQL connection is closed")

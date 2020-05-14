#!/usr/bin/env python

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import pickle
from time import sleep
import mysql.connector as mysql

with open('labels', 'rb') as f:
	dict = pickle.load(f)
	f.close()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

font = cv2.FONT_HERSHEY_SIMPLEX

db_connection = mysql.connect(
	host='localhost',
	database='rfid',
	user='admin',
	password='33a55b88d'
)

cursor = db_connection.cursor(prepared=True)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = frame.array
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

	for (x, y, w, h) in faces:
		roiGray = gray[y:y+h, x:x+w]

		id_, conf = recognizer.predict(roiGray)

		for name, value in dict.items():
			if value == id_:
				print(name)

		if conf <= 70:
			# set GPIO relay pin to 1
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			cv2.putText(frame, name + str(conf), (x, y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)

			query = "SELECT id FROM users WHERE name = %s"
			cursor.execute(query, (name,))
			result = cursor.fetchone()

			query = "INSERT INTO attendance(user_id) VALUES(%s)"
			cursor.execute(query, (result[0],))
			db_connection.commit()

		# else set GPIO relay pin to 0

	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)

	rawCapture.truncate(0)

	if key == 27:
		break

cv2.destroyAllWindows()

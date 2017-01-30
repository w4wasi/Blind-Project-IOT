import struct
import serial
import cv2
import numpy as np
import time
ser = serial.Serial('/dev/ttyACM0', 9600)
cap = cv2.VideoCapture(1)
iR='a'
nR=True
uR=True
dR=True
lR=True
rR=True
mR=True
minArea=500
while(1):
	iR=ser.read()
	print (iR)
	if (iR=='r'):
		break
	elif (iR=='g'):
		break
	elif (iR=='b'):
		break
while (1):
	_,frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	if ser.inWaiting():
		iR=ser.read()
	if(iR=='R'):
		lowerR=np.array([0,0,0])
		upperR=np.array([0,0,0])
	if(iR=='G'):
		lowerR=np.array([0,0,0])
		upperR=np.array([0,0,0])
	if(iR=='B'):
		lowerR=np.array([0,0,0])
		upperR=np.array([0,0,0])
	if(iR=='r'):
		lowerR=np.array([0,83,139])
		upperR=np.array([22,193,255])
	elif (iR=='g'):
		lowerR=np.array([59,54,63])
		upperR=np.array([105,176,129])
	elif (iR=='b'):
		lowerR=np.array([115,93,87])
		upperR=np.array([162,201,165])
	maskR = cv2.inRange(hsv, lowerR, upperR)
	momentsR = cv2.moments(maskR, True)
	if momentsR['m00'] >= minArea:
		x = momentsR['m10'] / momentsR['m00']
		y = momentsR['m01'] / momentsR['m00']
		cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
		if(x>0):
			if(x<299):
				print "go left"
				if(lR==True):	
					ser.write('l')
					lR=False
					uR=True
					dR=True
					rR=True
					mR=True
					nR=True
		if (x>330):
			if (x<640):
				print "go right"
				if(rR==True):
					ser.write('r')
					rR=False
					lR=True
					uR=True
					dR=True
					mR=True
					nR=True
		if (x>300):
			if(x<329):
				if(y>0):
					if(y<225):
						print "go up"
						if(uR==True):
							ser.write('u')
							rR=True
							lR=True
							uR=False
							dR=True
							mR=True
							nR=True
		if (x>300):
			if(x<329):
				if(y>225):
					if(y<255):
						print "got it"
						if(mR==True):
							ser.write('X')
							rR=True
							lR=True
							uR=True
							dR=True
							mR=False
							nR=True
		if (x>300):
			if(x<329):
				if(y>255):
					if(y<340):
						print "go down"
						if(dR==True):
							ser.write('d')
							rR=True
							lR=True
							uR=True
							dR=False
							mR=True
							nR=True
	else:
		print "not found"
		if(nR==True):
			ser.write('x')
			rR=True
			lR=True
			uR=True
			dR=True
			mR=True
			nR=False
			
	cv2.imshow('frame',frame)
	cv2.imshow('mask',maskR)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
	if(iR=='F'):
		cv2.destroyAllWindows()
		break
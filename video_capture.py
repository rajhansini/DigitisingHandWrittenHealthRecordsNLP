import numpy as np
import cv2
import urllib.request
import time
import script
import json

url='http://10.40.0.223:8080/shot.jpg'
import os

	
while True:
	# time.sleep(5)
	# Use urllib to get the image from the IP camera
	imgResp = urllib.request.urlopen(url)
	
	# Numpy to convert into a array
	imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
	
	# Finally decode the array to OpenCV usable format ;) 
	img = cv2.imdecode(imgNp,-1)
	
	
	# put the image on screen
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	cv2.imshow('IPWebcam.png',img)
	
	
	#To give the processor some less stress


	# Quit if q is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	elif cv2.waitKey(1) == ord('c'):
		# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)s
		# ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

		duration = 2  # seconds
		freq = 440  # Hz
		os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


		cv2.imwrite( 'IPWebcam.png', img )
		catch  = script.get_str('IPWebcam.png')
		entry = script.findMatch(catch)

		try :
			name = ("_".join(entry['Name'].split()))
		except :
			try :
				name = ("_".join(entry['Patient'].split()))
			except :
				name = "Some_patient"

		entryJson = json.dumps(entry)
		print(entryJson)
		file_id=os.path.splitext('IPWebcam.png')[0]
		myfname = '%s_%s.json'%(name,file_id)
		f = open(myfname, 'w')
		f.write(entryJson)
		f.close()

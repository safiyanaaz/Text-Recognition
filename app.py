from flask import Flask,render_template,url_for,request
import pandas as pd
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import re
import pytesseract
from gtts import gTTS
from flask import jsonify
import speech_recognition as sr
import os
import time
import pyttsx3
from flask_assets import Bundle, Environment
import os,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd 
import pythoncom


app = Flask(__name__)


@app.route('/')
def index():
	pythoncom.CoInitialize()

	engine = pyttsx3.init()
	rate = engine.getProperty('rate')   # getting details of current speaking rate
	engine.setProperty('rate', 125)
	volume = engine.getProperty('volume')
	engine.setProperty('volume',1.0)   
	voices = engine.getProperty('voices')    
	engine.say("Welcome to the app for Visually Impaired People Please Speak Retrieve or Click Picture")
	engine.runAndWait()
	engine.stop()
	r2=sr.Recognizer()
	with sr.Microphone() as source:
		print('Speak retrieve or click picture')
		speak=r2.listen(source)
		start=r2.recognize_google(speak)
		print(start)
	if "retrieve" in start:
		engine.say("Speak the name of audio file you want to retrieve")
		engine.runAndWait()
		#os.system(r"audiosproject\retrieve.wav")
		r3=sr.Recognizer()
		with sr.Microphone() as source:
			print("Speak audio name")
			audio_name_retrieve=r3.listen(source)
			name=r3.recognize_google(audio_name_retrieve)
			audioo="{0}.wav".format(name)
			list_files =os.listdir(".")
			if audioo in list_files:
				os.system(audioo)
			else:
				engine.say("Sorry No such audio Found")
				#engine.runAndWait()
	elif "click picture" in start:
		print('Click Picture')
	return render_template('index.html')


@app.route('/predict',methods=['GET', 'POST'])

def predict():
	pythoncom.CoInitialize()
	engine = pyttsx3.init()
	rate = engine.getProperty('rate')   # getting details of current speaking rate
	engine.setProperty('rate', 125)
	volume = engine.getProperty('volume')
	engine.setProperty('volume',1.0)   
	voices = engine.getProperty('voices')

	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ramizkey.json'
	client = vision.ImageAnnotatorClient()
	if request.method=='POST':
		input1= request.form.get("input1") if request.form.get("input1") else None
		base64_data = re.sub('^data:image/.+;base64,', '',input1)
		im = Image.open(BytesIO(base64.b64decode(base64_data)))
		im.save('image.png', 'PNG')
		print('image saved')
	file= "image.png"
	imagename = "demo"
	with io.open(file,'rb') as image:
		content = image.read()
	image=vision.types.Image(content=content)
	response = client.text_detection(image=image)
	texts = response.text_annotations
	df = pd.DataFrame(columns=['locale','description'])
	for text in texts:
		mytext=text.description
		print(text.description)
		break

	
	f = open("{0}.txt".format(imagename), 'w')
	f.write(mytext)
	f.close()
	f = open('{0}.txt'.format(imagename))
	x = f.read()

	language = 'en'
	audio = gTTS(text = x , lang = language , slow = False)
	
	r1=sr.Recognizer()
	#os.system(r"audiosproject\audio_name.wav")
	engine.say("Please Speak the name in which you want to save your audio file")
	engine.runAndWait()
	
	with sr.Microphone() as source:
		print('Speak now')
		
		audio_name=r1.listen(source)
		text_audio_name=r1.recognize_google(audio_name)
		text_audio_name=text_audio_name.replace(" ","")
		print(text_audio_name)
		engine.say("Your audio is saved as {0}.We are processing your audio Please Wait".format(text_audio_name))
		engine.runAndWait()
	text_audio_name = 'test'
	audio.save("{0}.wav".format(text_audio_name))
	os.system("{0}.wav".format(text_audio_name))
	print('saved audio')
	
	return render_template('result.html',text=mytext)


if __name__ == '__main__':
    app.run(debug=True)
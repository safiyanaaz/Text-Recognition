import os,io
from google.cloud import vision
from google.cloud.vision import types
from io import BytesIO
from PIL import Image
import pandas as pd 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ramizkey.json'
client = vision.ImageAnnotatorClient()

file = 'test.jpeg'
with io.open(file,'rb') as image:
	content = image.read()
#img2 = img.crop((1,20,50,80))

image=vision.types.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations
df = pd.DataFrame(columns=['locale','description'])

#print(texts)

for text in texts:
	print(text.description)
	break
	#df = df.append(dict(locale=text.locale,description=text.description),ignore_index=True)
#print(df)


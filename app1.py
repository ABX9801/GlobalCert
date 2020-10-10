import re
import os
import cv2
import string
import PIL.Image
import numpy as np
import pytesseract
import pandas as pd
from PIL import Image
import streamlit as st
import shutil
from pytesseract import Output
from pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files /Tesseract-OCR'

st.markdown('<style>body{background-color:powderblue;}</style>',unsafe_allow_html=True)

st.sidebar.header("Certificate Generator😷🔬")
ch = st.sidebar.selectbox(
    "Choice",
    [
        "Home",
        "Certificate Generator",
        "Gallery"
    ],
    key="main_select",
    )

if ch == "Home":
	a = "Certificate Generator😷🔬"
	st.title(a)

	a = '<p style="text-align: justify;font-size:20px;">Certificate Generator is the system which will be used to generate certificates '
	a+='automatically, just by uploading a csv file and the template for the certificate.'
	a+=' We will be using tesseract OCR for identifying blank spaces, then we will fill in the spaces with the input given'
	a+='by the user. We will also br providing a few templates which can be directly used to generate certificates.'
	a+=' </p><br>'

	st.markdown(a,unsafe_allow_html=True)

	a ="<p style='text-align: justify;font-size:20px;'>This project gives its users the power/abilty to generate certificates in bulk.<br><br>"
	a+=" <b>Features</b><ul><li style='text-align: justify;font-size:20px;'>Interactive Dashboard to generate certificates easily</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Template upload Option to generate certificates</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Preview of the certificates</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Bulk Certificate generator</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Download option to save certificates.</li></ul></p>"

	st.markdown(a,unsafe_allow_html=True)

	a = "<p style='text-align: justify;font-size:20px;'>Please choose Certificate Generator from the sidebar to proceed.</p>"
	st.markdown(a,unsafe_allow_html=True)

elif ch=="Certificate Generator":
	a = "Certificate Generator Tool!! 😷🔬"
	st.title(a)
	a = '<p style="text-allign: justify; font-size: 20px;">Select a csv file and the certificate template.</p>'
	st.markdown(a,unsafe_allow_html=True)
	a = '<p style="font-size: 30px;">Instructions for uploading the files:</p>'
	a+='<ol><li>File should have 3 columns named <b>Name</b>, <b>Company</b> and <b>Position</b></li>'
	a+='<li>The Name column will contain the Names.</li><li>The Position column will contain the Position</li>'
	a+='<li>The template should be of either <b>png</b> or <b>jpeg</b> or <b>jpg</b></li></ol>'
	st.markdown(a,unsafe_allow_html=True)

	uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
	uploaded_image = st.sidebar.file_uploader("Choose a Template file", type = ["png","jpeg","jpg"])

	if uploaded_file is not None and uploaded_image is not None:
		#print(uploaded_file)
		#print(uploaded_image)
		df = pd.read_csv(uploaded_file)
		b = df.columns
		if 'Name' in b:
			if 'Company' in b:
				if 'Position' in b:
					output = pytesseract.image_to_string(PIL.Image.open(uploaded_image).convert("RGB"), lang='eng')
					output = output.strip()
					z = output.split("\n")
					o =[]
					for i in z:
						if i!='' and i!=' ':
							o.append(i)
					a = o[0]
					a = a.split(" ")
					a = a[0]
					b = o[1]
					b = b.split(" ")
					b = b[0]
					c = o[2]
					c = c.split(" ")
					c = c[0]
					d = o[3]
					d = d.split(" ")
					d = d[0]
					img = PIL.Image.open(uploaded_image).convert("RGB")
					img  = np.array(img)
					img = img[:, :, ::-1].copy() 
					#file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
					#img = cv2.imdecode(file_bytes, 1)
					#cv2.imread(path)
					e = pytesseract.image_to_data(img, output_type=Output.DICT)
					i = e['text'].index(a)
					j = e['text'].index(b)
					k = e['text'].index(c)
					l = e['text'].index(d)
					name = np.array(df['Name']).tolist()
					position = np.array(df['Position']).tolist()
					company = np.array(df['Company']).tolist()
					os.mkdir('Certificates')
					for z in range(len(name)):
						img1 = img.copy()
						textsize = cv2.getTextSize(name[z], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
						x = (img1.shape[1] - textsize[0]) // 2
						x1 = (e['left'][j]+e['left'][i])//2
						if x-x1 > 0.2*img1.shape[1]:
						    x = x1
						y = (e['top'][j]+e['top'][i])//2 + e['height'][i]
						cv2.putText(img1,name[z], (x,y), cv2.FONT_HERSHEY_COMPLEX , 1, (0,0,0),2, cv2.LINE_AA)

						(x, y, w, h) = (e['left'][k], e['top'][k], e['width'][k], e['height'][k])
						textsize = cv2.getTextSize(company[z], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
						x = (img1.shape[1] - textsize[0]) // 2 
						x1 = (e['left'][j]+e['left'][k])//2
						if x-x1 > 0.2*img1.shape[1]:
						    x = x1
						y = (e['top'][j]+e['top'][k])//2 + e['height'][j]
						cv2.putText(img1,company[z], (x,y), cv2.FONT_HERSHEY_COMPLEX , 1, (0,0,0),2, cv2.LINE_AA)

						(x, y, w, h) = (e['left'][l], e['top'][l], e['width'][l], e['height'][l])
						textsize = cv2.getTextSize(position[z], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
						x = (img1.shape[1] - textsize[0]) // 2 
						x1 = (e['left'][k]+e['left'][l])//2
						if x-x1 > 0.2*img1.shape[1]:
						    x = x1
						y = (e['top'][k]+e['top'][l])//2 + e['height'][k]
						cv2.putText(img1,position[z], (x,y), cv2.FONT_HERSHEY_SIMPLEX , 1, (0,0,0),2, cv2.LINE_AA)

						cv2.imwrite("./Certificates/{}_{}.png".format(name[z],z),img1)
					file_name = "certificates.zip"
					shutil.make_archive('certificates', 'zip', 'Certificates')
					gg = '<a href="certificates.zip" download>Download my CV</a>'
					st.markdown(gg,unsafe_allow_html=True)
				else:
					st.markdown('<h2>The uploaded file does not adhere to the instructions.<h2>',unsafe_allow_html=True)
			else:
				st.markdown('<h2>The uploaded file does not adhere to the instructions.<h2>',unsafe_allow_html=True)
		else:
			st.markdown('<h2>The uploaded file does not adhere to the instructions.<h2>',unsafe_allow_html=True)

	
else:
	st.title("sdlfmlksmflksdmfl")

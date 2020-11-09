# -*- coding: utf-8 -*-
"""Caffe.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qBb-0HpJq9ozK10aq5ByWzH9pMESkvP4
"""

#!apt install caffe-cpu

# Commented out IPython magic to ensure Python compatibility.
import cv2
from PIL import Image
import caffe
import os
import numpy as np
#import matplotlib.pyplot as plt
# %matplotlib inline

cur_net_dir = 'VGG_S_rgb'
DEMO_DIR = './demodir/DemoDir'

mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]



# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



	
net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=((256, 256))
)
	
#plt.rcParams['figure.figsize'] = (10, 10)
#plt.rcParams['image.interpolation'] = 'nearest'
#plt.rcParams['image.cmap'] = 'gray'


categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']

def showimage(im):
    if im.ndim == 3:
        im = im[:, :, ::-1]
#    plt.set_cmap('jet')
#    plt.imshow(im,vmin=0, vmax=0.2)
    

def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    #showimage(data)

def whatsthatface(imagepath="josie.JPG"):
	'''Identify an individual face given the name of an image. Returns category and probability'''
	results = []

	# Read the input image
	img = cv2.imread(imagepath)


	# Convert into grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Detect faces
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)
	

	count = 0

	# Draw rectangle around the faces
	for (x, y, w, h) in faces:
		count = count+1
		frame = img[y:y+h, x:x+h]
		
		cv2.imwrite("temp"+str(count)+".jpg", frame)

		input_image = caffe.io.load_image("temp"+str(count)+".jpg")
		prediction = VGG_S_Net.predict([input_image],oversample=False)
		print(prediction)
		results.append('{0}'.format(categories[prediction.argmax()]))

	if len(results)==0:
		input_image = caffe.io.load_image(imagepath)
		prediction = VGG_S_Net.predict([input_image],oversample=False)
		print(prediction)
		results.append('{0}'.format(categories[prediction.argmax()]))


	return '\n'.join(results)


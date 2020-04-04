import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QRadioButton, QGroupBox, QCheckBox, QDoubleSpinBox, QLabel
from PyQt5 import QtGui
import cv2
import os
import get_inference




Files_list = []

file_index = 0

model = "FRCNN"

threshold = 0.7

label_list = []

def select_folder():
	dialog = QFileDialog()
	folder_path = dialog.getExistingDirectory(None, "Select Folder")
	global Files_list
	
	for r, d, f in os.walk(folder_path):
		if len(d) > 0:
			print ("invalid folder")
			break
		for file in f:
			Files_list.append(os.path.join(r,file))
	print (Files_list)

	

	return folder_path


def next_image():
	
	global Files_list
	global file_index

	if file_index < len(Files_list)-1:
		file_index = file_index + 1
	else:
		file_index = 0

	cv2.namedWindow('Window1')
	img = cv2.imread(Files_list[file_index])
	cv2.imshow('Window1',img)
	cv2.waitKey(3000)
	cv2.destroyAllWindows()
	
	
	print (Files_list, file_index)

	

def previous_image():
	
	global Files_list
	global file_index

	if file_index == 0:
		file_index = len(Files_list) - 1

	elif file_index >1:
		file_index = file_index - 1

	elif file_index==1:
		file_index = 0

	cv2.namedWindow('Window1')
	img = cv2.imread(Files_list[file_index])
	cv2.imshow('Window1',img)
	cv2.waitKey(3000)
	cv2.destroyAllWindows()

def select_model(b):

	global model
	print (model)

	if b.text() == 'FRCNN':
		if b.isChecked() == True:	
			model = 'FRCNN'

	elif b.text() == 'Mobilenet':
		if b.isChecked() == True:
			model = 'Mobilenet'

	elif b.text() == 'SSD':
		if b.isChecked() == True:
			model = 'SSD'

	

def select_detection_threshold(b):
	global threshold

	threshold = b.value()
	print (threshold)
	
def select_labels(b):

	global label_list

	if b.isChecked() == True:
		label_list.append(b.text())
	else:
		label_list.remove(b.text())

	print (label_list)

def Detect_objects():

	if model == 'FRCNN':
		get_inference.get_model_folder("faster_rcnn_inception_v2_coco_2018_01_28")

	elif model == 'SSD':
		get_inference.get_model_folder("ssd_inception_v2_coco_2018_01_28")

	elif model == 'Mobilenet':
		get_inference.get_model_folder("ssd_mobilenet_v1_coco_2018_01_28")

	get_inference.num_classes(len(label_list), threshold, label_list)

	get_inference.print_stat()

	
	img = cv2.imread(Files_list[file_index])

	coordinates, items = get_inference.get_roi_label(img)

	coo_new = []
	items_new = []

	for i in range(len(items)):
		for label in label_list:

			if items[i] == label:
				items_new.append(items[i])
				coo_new.append(coordinates[i])
	

	print (coordinates)
	print (items)

	print (coo_new)
	print (items_new)
	
	for i in range(len(coo_new)):

		if items_new[i] == 'car':
			cv2.rectangle(img, (coo_new[i][2],coo_new[i][0]), (coo_new[i][3], coo_new[i][1]),(0,255,0),2)

		elif items_new[i] == 'bus':
			cv2.rectangle(img, (coo_new[i][2],coo_new[i][0]), (coo_new[i][3], coo_new[i][1]),(255,0,0),2)

		elif items_new[i] == 'person':
			cv2.rectangle(img, (coo_new[i][2],coo_new[i][0]), (coo_new[i][3], coo_new[i][1]),(0,0,255),2)

		elif items_new[i] == 'bicycle':
			cv2.rectangle(img, (coo_new[i][2],coo_new[i][0]), (coo_new[i][3], coo_new[i][1]),(0,0,0),2)

		else:
			cv2.rectangle(img, (coo_new[i][2],coo_new[i][0]), (coo_new[i][3], coo_new[i][1]),(255,255,255),2)

	cv2.namedWindow('Window1')

	cv2.imshow('Window1',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	
	#get_inference.print_stat()

	



if __name__ == '__main__':




	

	app = QApplication(sys.argv)
	w = QWidget()
	w.resize(1000,500)
	w.move(300,300)
	w.setWindowTitle('Object Detection tool')


	layout = QGridLayout()

	button1 = QPushButton('Open Folder')
	button1.setToolTip('Click to open desired folder')
	button1.clicked.connect(select_folder)
	layout.addWidget(button1,0,0)

	button2 = QPushButton('Next Image')
	button2.setToolTip('Click to get the next image')
	button2.clicked.connect(next_image)
	layout.addWidget(button2,1,0)
	
	button3 = QPushButton('Previous Image')
	button3.setToolTip('Click to get the previous image')
	button3.clicked.connect(previous_image)
	layout.addWidget(button3,2,0)

	button4 = QPushButton('Detect')
	button4.setToolTip('Click to detect objects')
	button4.clicked.connect(Detect_objects)
	layout.addWidget(button4,3,2)

	groupbox= QGroupBox("Select one out of the three models")
	ha = QVBoxLayout()

	button5 = QRadioButton('FRCNN')
	button5.model = "FRCNN"
	button5.toggled.connect(lambda : select_model(button5))
	ha.addWidget(button5)

	button6 = QRadioButton('Mobilenet')
	button6.model = "Mobilenet"
	button6.toggled.connect(lambda : select_model(button6))
	ha.addWidget(button6)

	button7 = QRadioButton('SSD')
	button7.model = "SSD"
	button7.toggled.connect(lambda : select_model(button7))
	ha.addWidget(button7)

	groupbox.setLayout(ha)
	layout.addWidget(groupbox,0,2)

	groupbox= QGroupBox("Select single or multiple labels")
	ha = QVBoxLayout()

	button8 = QCheckBox('car')
	button8.stateChanged.connect(lambda : select_labels(button8))
	ha.addWidget(button8)

	button9 = QCheckBox('person')
	button9.stateChanged.connect(lambda : select_labels(button9))
	ha.addWidget(button9)

	button10 = QCheckBox('bus')
	button10.stateChanged.connect(lambda : select_labels(button10))
	ha.addWidget(button10)

	button11 = QCheckBox('bicycle')
	button11.stateChanged.connect(lambda : select_labels(button11))
	ha.addWidget(button11)

	button12 = QCheckBox('traffic light')
	button12.stateChanged.connect(lambda : select_labels(button12))
	ha.addWidget(button12)

	groupbox.setLayout(ha)
	layout.addWidget(groupbox,1,2)

	groupbox=QGroupBox("")
	ha = QVBoxLayout()
	
	l1 = QLabel("Detection Threshold")
	ha.addWidget(l1)

	button13 = QDoubleSpinBox()
	button13.setMinimum(0)
	button13.setMaximum(1)
	button13.setSingleStep(0.05)
	button13.valueChanged.connect(lambda : select_detection_threshold(button13))

	ha.addWidget(button13)

	groupbox.setLayout(ha)
	layout.addWidget(groupbox,2,2)

	
	w.setLayout(layout)
	
	w.show()

	sys.exit(app.exec_())

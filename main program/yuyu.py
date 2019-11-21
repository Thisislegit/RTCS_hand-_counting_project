#!/usr/bin/env python3

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import os
import time
import pygame 
import threading
from hand_counting import hand_count
import cv2
#pygame.init()
#pygame.mixer.init()
from pykeyboard import *
from mutagen.mp3 import MP3

global music_path 
music_path = None
#mp3 = MP3(music_path)

import time, threading
k = PyKeyboard()
global flag 
global flag2
global frame
flag = False
flag2 = True

def hand():
	global flag, flag2, frame, music_path
	#flag = False
	#flag2 = True
	while(True):
		count = hand_count(ret, frame)
	#time.sleep(1)
		flag = False
		flag2 = True
		if count == 1:
			flag2 = True
			if (flag == True and flag2 == True) or (flag == False and flag2 == True):
				k.press_key('q')
				k.release_key('q')
				time.sleep(2)

		elif count == 2:
			if flag == True and flag2 == True:
				k.press_key('q')
				k.release_key('q')
				time.sleep(2)
			music_path = '2.mp3'
			flag = True		#start play at this moment	
			
			time.sleep(2)
		elif count == 3:
			if flag == True and flag2 == True:
				k.press_key('q')
				k.release_key('q')
				time.sleep(2)
			music_path = '3.mp3'
			flag = True		#start play at this moment	
			
			time.sleep(2)
		elif count == 4:
			
			if flag == True and flag2 == True:
				k.press_key('q')
				k.release_key('q')
				time.sleep(2)
			music_path = '4.mp3'
			flag = True		#start play at this moment	
			
			time.sleep(2)
			
		elif count ==5:
			if flag == True and flag2 == True:
				k.press_key('q')
				k.release_key('q')
				time.sleep(2)
			music_path = '5.mp3'
			flag = True		#start play at this moment	
			
			time.sleep(2)
			
		else:
			print('error')
			#choose which to play
		#print('music path is {}'.format(music_path))
		print('count is {}\n'.format(count))
		print('flag is {}\n'.format(flag))
		print('flag2 is {}\n'.format(flag2))
		
		#k.press_key('p')		#pause play
		#k.release_key('p')

		#time.sleep(2)			#quit this song
		
		

def loop():
	global flag, flag2, music_path
	flag2 = True
	while(True):
		if flag and flag2:
			flag = False
			flag2 = False
			os.system('mplayer %s' % music_path)

		
		


event_obj = threading.Event()
event_obj.clear()


print('thread %s is running...' % threading.current_thread().name)
t1 = threading.Thread(target=loop, name='LoopThread')
t2 = threading.Thread(target=hand)
t1.setDaemon(True)
t2.setDaemon(True)

cv2.namedWindow("hand")
vc = cv2.VideoCapture(0)  
count = 2
ret, frame  = vc.read()

t2.start()
t1.start()


while True:
	ret, frame  = vc.read()
	if cv2.waitKey(1) & 0xFF == ord('a'): 
		 break



print('thread %s ended.' % threading.current_thread().name)

 	    
cv2.destroyAllWindows()

#track=pygame.mixer.music.load("1.mp3")
#music_path = '1.mp3'
#mp3 = MP3(music_path)
#print(mp3)
#os.system('mplayer %s' % music_path)
#time.sleep(5)
vc.release()

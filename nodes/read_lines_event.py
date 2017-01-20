#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from naoqi import ALProxy 
import codecs
import time
import re
import random

# Debug
import rospy
from std_msgs.msg import String
from memory.msg import Animation


pairs_dict = {	'[0, 1]' : False,
				'[2, 3]' : False,
				'[4, 5]' : False,
				'[6, 7]' : False,
				'[8, 9]' : False
			 }


story_dict ={	'[200, 201]': 1, 
				'[210, 211]': 2,
				'[220, 221]': 3,
				'[230, 231]': 4,
				'[240, 241]': 5,
				'[2, 3]': 7
			}

reaction_states = { "low": [1, 2, 3, 4, 5],
				  	"medium": [6, 7, 8, 9, 10],
				  	"high": [11, 12, 13, 14, 15] }


mistake_level_states = { "low": [1],
						 "medium": [3],
						 "high": [5]}

story_selection_state = {}

""" Recieve the key stroke from key publisher node
	[1]: tell the robot made a mistake in reading the story
	[2]: tell the robot to choose a new story and repeat the process
	[3]: tell the robot to stop the tracker and go to resting mode

"""
KEY_MAPPING = { 'f': [2], 
				'g': [2], 
				'h': [2],
				'b': [3],
				'n': [3],
				'm': [3],
				'e': [4],
				'r': [4],
				't': [4],
				's': [1]  
				}


def storySelection():
	""" Select a story from the text files of each story and return it

	"""

	with open('chick_story_en.txt') as f:
		lines_content = f.read().splitlines()
		print lines_content

	for line in lines_content:
		found = re.search("2, 3", line)
		if not found == None:
			print line
			print line[:found.start()] + line[found.end():]
			print
			selectedStory = line[:found.start()] + line[found.end():]
			break



	return selectedStory


def tag_detection_old(msg):
	print msg.data

	tag = msg.data
	#lst = eval(msg.data)
	#print lst



	#selectedStory = storySelection()
	with open('chick_story_en.txt') as f:
		lines_content = f.read().splitlines()
		#print lines_content

	line_tag = tag.replace('[', '').replace(']', '')
	print line_tag
	for line in lines_content:
		found = re.search(line_tag, line)
		if not found == None:
			print line
			print line[:found.start()] + line[found.end():]
			
			selectedStory = line[:found.start()] + line[found.end():]
			selectedStory = selectedStory.replace('[', '').replace(']', '')
			print selectedStory
			break

	story.say(selectedStory)

	if msg.data == '[2, 3]' or msg.data == '[3, 2]':
		if pairs_dict['[2, 3]'] == False:
			print "test         [2, 3]"
			#if counter == 1:
			#rospy.loginfo("read the story...")
			story.say("\\rspd=70\\ A red Fox \\pau=500\\ in green socks \\pau=500\\")
			pairs_dict['[2, 3]'] = True

	if msg.data == '[4, 5]' or msg.data == '[4, 5]':
		if pairs_dict['[4, 5]'] == False:
			print "test         [4, 5]"
			#if counter == 1:
			#rospy.loginfo("read the story...")
			story.say("\\rspd=70\\ doing tricks with orange rocks")
			pairs_dict['[4, 5]'] = True


def tag_detection(msg):

	tag = msg.data
	tag = tag.replace('[', '').replace(']', '')
	with open('chick_story_en.txt') as f:
		lines_array = f.read().splitlines()

	for line in lines_array:
		found = re.search(tag, line)
		if not found == None:
			selectedStory = line[:found.start()] + line[found.end():]
			selectedStory = selectedStory.replace('[', '').replace(']', '')
			#print selectedStory
			break

	

	if pairs_dict[msg.data] == False:
		story.say(selectedStory)
		pairs_dict[msg.data] = True

	if msg.data == '[2, 3]' or msg.data == '[3, 2]':
		if pairs_dict[msg.data] == False:
			print "test         [2, 3]"
			#if counter == 1:
			#rospy.loginfo("read the story...")
			story.say("\\rspd=70\\ A red Fox \\pau=500\\ in green socks \\pau=500\\")
			pairs_dict['[2, 3]'] = True

	if msg.data == '[4, 5]' or msg.data == '[4, 5]':
		if pairs_dict['[4, 5]'] == False:
			print "test         [4, 5]"
			#if counter == 1:
			#rospy.loginfo("read the story...")
			story.say("\\rspd=70\\ doing tricks with orange rocks")
			pairs_dict['[4, 5]'] = True


def faceTrackingStarted(faceSize):
	""" Robot starts to track the users face

	"""

	# First, wake up
	#reaction.wakeUp()
	reaction.rest()

	# Add target to track
	targetName = "Face"
	faceWidth = faceSize
	tracker.registerTarget(targetName, faceWidth)

	# Then, start tracker
	tracker.track(targetName)


def faceTrackingEnded(msg):
	""" Robot stops to track the users face and go into resting mode after certain keys are pressed

	"""

	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]

	# Stop tracker
	if reac == [4]:
		tracker.stopTracker()
		tracker.unregisterAllTargets()
		reaction.rest()


def IntroduceNao():
	"""
	Nao starts introducing itself when the book cover is in front of him 
	"""

	'''if msg.data in story_dict:
		storyNum = story_dict[msg.data]
		print storyNum'''

	'''if msg.data == '[0, 1]' or msg.data == '[1, 0]':
		if pairs_dict['[0, 1]'] == False:
			print "test         [0, 1]"
			pairs_dict['[0, 1]'] = True'''
	story.setLanguage('English')
	story.say("\\rspd=70\\ Hello \\pau=500\\ My name is nao \\pau=500\\ I really like reading short stories")
	story.say("\\rspd=70\\ Do you want to listen to them?")
	time.sleep(2)
	story.say("\\rspd=70\\ If you like, please bring the story book")
	time.sleep(5)
			


def main():
	
	global story
	story = ALProxy("ALTextToSpeech", "nao.local", 9559)
	
	global conversration
	conversation = ALProxy("ALTextToSpeech", "nao.local", 9559)

	global reaction
	reaction = ALProxy("ALMotion", "nao.local", 9559)
	
	global audioreaction
	audioreaction = ALProxy("ALAudioPlayer", "nao.local", 9559)
	
	global tracker
	tracker = ALProxy("ALTracker", "nao.local", 9559)

	# Initialize the node
	rospy.init_node('read_lines_event')

	storyNum = 1
	pub = rospy.Publisher('story_number', String, queue_size=1)
	pub.publish(str(storyNum))
	#storySelection()

	# Face tracking activated
	facesize = 0.1
	global restingEnabled 
	restingEnabled = False
	faceTrackingStarted(facesize)

	# Select a story and activity level
	global selectedStory
	#selectedStory = storySelection()
	correctFlag = False
	activityLevel = rospy.get_param('actlevel', 'medium')
	#mistakeNum = numberOfMistakesSelection(activityLevel)

	time.sleep(5)
	IntroduceNao()

	#rospy.Subscriber('tag_id_state', String, IntroduceNao)


	rospy.Subscriber('tag_id_state', String, tag_detection)

	#

	#readTheTaggedStory(selectedStory, correctFlag)
	#readTheTaggedStoryWithLevel(selectedStory, correctFlag, mistakeNum)

	#rospy.Subscriber('button_start', String, startTheStoryReading)

	#rospy.Subscriber('button_wrong', String, mistakeDetected)

	#rospy.Subscriber('keys', String, faceTrackingEnded)

	#rospy.Subscriber('keys', String, repeatTheStoryReading)
	
	try:
		while True:
			time.sleep(1)
    	except restingEnabled == True:
        	print
        	print "Interrupted by user, shutting down"
        	myBroker.shutdown()
        	sys.exit(0)



if __name__ == "__main__":


	main()
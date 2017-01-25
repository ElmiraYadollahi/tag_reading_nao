#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Int64, Int64MultiArray, String
from geometry_msgs.msg import Point, PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers

tag_states = { 0, 1, 2 , 3, 4, 5, 6, 2222, 4444}
tag_pairs = [[0, 1], [1, 0], [2, 3], [3, 2]]

#global avail_pair
#global flag
global counter
#avail_pair = []
#flag = False
counter = 0
class TagsCOG():

	def __init__(self):
		rospy.init_node("ar_tags_poses")

		# Read in an optional list of valid tag ids
		self.tag_ids = rospy.get_param('~tag_ids', None)

		# Publish the COG on the /target_pose topic as a PoseStamped message
		self.tag_pub = rospy.Publisher("target_pose", PoseStamped, queue_size=5)

		global counter
		counter = 0
		global avail_tags
		avail_tags = []
		global avail_pair
		avail_pair = []

		rospy.Subscriber("ar_pose_marker", AlvarMarkers, self.get_tags)



		#print "hello"
		rospy.loginfo("Publishing combined tag COG on topic /target_pose...")
		print "test point 1"


	def get_tags(self, msg):

		# Initialize the COG as a PoseStamped message
		tag_cog = PoseStamped()

		# Get the number of markers
		n = len(msg.markers)

		#counter = 0
		#avail_tags = []
		#avail_pair = []
		global avail_pair
		global counter

		# If no markers detected, just retutn 
		if n == 0:
			return

		#print "test point 2"


		# Iterate through the tags and sum the x, y and z coordinates
		for tag in msg.markers:

			# Skip any tags that are not in our list
			if self.tag_ids is not None and not tag.id in self.tag_ids:
				continue

			# Sum up the x, y and z position coordinates of all tags
			tag_cog.pose.position.x += tag.pose.pose.position.x
			tag_cog.pose.position.y += tag.pose.pose.position.y
			tag_cog.pose.position.z += tag.pose.pose.position.z

			#print "test point 3"

			#calculate_distance(tag.pose.pose.position.x, tag.pose.pose.position.y)
			if tag.id in tag_states:
				avail_tags.append(tag.id)
				#print "test point 4"
				if tag.id not in avail_pair:
					avail_pair.append(tag.id)
					#print "test point 5"
				tag_state_pub = rospy.Publisher("id_state", Int64, queue_size=5)
				tag_state_pub.publish(tag.id)
				print avail_pair
				if len(avail_pair) == 3:
					avail_pair = []
				#avail_pair = avail_tags
				if avail_pair in tag_pairs:
					#print "test point 6"
					pair_state_pub = rospy.Publisher("pair_state", Int64, queue_size=5)
					pair_state_pub.publish(avail_pair[0])
					pair_state_pub.publish(avail_pair[1])
					flag = True
					global counter
					counter += 1
					story(avail_pair, counter)
					avail_pair = []
					print "skip"
					



			# Compute the COG
			tag_cog.pose.position.x /= n
			tag_cog.pose.position.y /= n
			tag_cog.pose.position.z /= n

			# Give the tag a unit orientation
			tag_cog.pose.orientation.w = 1

			# Add a time stamp and frame_id
			tag_cog.header.stamp = rospy.Time.now()
			tag_cog.header.frame_id = msg.markers[0].header.frame_id
			#tag_cog.header.seq = self.tag_ids

			# Publish the COG
			self.tag_pub.publish(tag_cog)


	def timer_callback(avail_pair):
		avail_pair = []
		print 'timer called at ' + str(event.current_real)

		return avail_pair
	#def recognize_text(self):

		# Recognize the tag and read associated text
		#if 


	#def calculate_distance(x, y):
		
		# find the tags 

def story(avail_pair, counter):
	print avail_pair

	if avail_pair == [0, 1] or avail_pair == [1, 0]:
		print "test 2"
		counter += 1
		if counter == 1:
			print "test 3"
			#if counter == 1:
			#rospy.loginfo("read the story...")
			story_pub = rospy.Publisher('story_state', String, queue_size=10)
			story_pub.publish("read the story")

	if avail_pair == [2, 3] or avail_pair == [3, 2]:
		print "test 4"

if  __name__ == '__main__':
	
	try:
		TagsCOG()
		#story()
		rospy.spin()
	except rospy.ROSInterruptException:
		rospy.loginfo("AR Tag Tracker node terminated.")
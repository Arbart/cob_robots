#!/usr/bin/env python
import roslib
roslib.load_manifest('cob_hardware_test')

import sys
import unittest
import rospy
import rostest

from cob_hardware_test.srv import *
from std_msgs.msg import String
from simple_script_server import *
from pr2_controllers_msgs.msg import *


def dialog_client(dialog_type, message):
    #dialog type: 0=confirm 1=question
	rospy.wait_for_service('dialog')
	try:
		dialog = rospy.ServiceProxy('dialog', Dialog)
		resp1 = dialog(dialog_type, message)
		return resp1.answer
	except rospy.ServiceException, e:
		print "Service call failed: %s" % e

class HardwareTest(unittest.TestCase):
	def __init__(self, *args):

		super(HardwareTest, self).__init__(*args)
		rospy.init_node('test_hardware_test')
		torso_joint_states = []
		self.message_received = False
		self.sss = simple_script_server()

		try:
				# move_
				if not rospy.has_param('~move_x'):
					self.fail('Parameter move_x does not exist on ROS Parameter Server')
				self.move_x = rospy.get_param('~move_x')

				if not rospy.has_param('~move_y'):
					self.fail('Parameter move_ does not exist on ROS Parameter Server')
				self.move_y = rospy.get_param('~move_y')

				if not rospy.has_param('~move_theta'):
					self.fail('Parameter move_ does not exist on ROS Parameter Server')
				self.move_theta = rospy.get_param('~move_theta')

		except KeyError, e:
				self.fail('Parameters not set properly')


	def test_base(self):
		self.sss.init("base")
		self.assertTrue(dialog_client(0, 'Ready to move base?' ))
		handle = self.sss.move_base_rel("base", [self.move_x, self.move_y, self.move_theta])
		self.assertEqual(handle.get_state(), 3)
		self.assertTrue(dialog_client(1, 'Did I move?'))

if __name__ == '__main__':

	try:
		rostest.run('rostest', 'test_hardware_test', HardwareTest, sys.argv)
	except KeyboardInterrupt, e:
		pass
	print "exiting"

# some tests how to work with enums

from enum import Enum

class RobotArm(Enum):
	free = 0
	kettle = 1
	teacup = 2
	teabag = 3

print RobotArm['kettle']

a = RobotArm.kettle

print RobotArm['kettle'] == a

print a.name == 'kettle'

print '!!!'

print RobotArm(3)
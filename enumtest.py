# some tests how to work with enums

from enum import Enum
import random

class RobotArm(Enum):
	free = 0
	kettle = 1
	teacup = 2
	teabag = 3

class Teacupstate():
	unknown = 0
	clean = 1
	dirty = 2
	taken = 3

print RobotArm['kettle']

a = RobotArm.kettle

print RobotArm['kettle'] == a

print a.name == 'kettle'

print '!!!'

print RobotArm(3)

test = [Teacupstate.unknown for _ in range(75)]
print test
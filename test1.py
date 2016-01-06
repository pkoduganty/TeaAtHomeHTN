import sys
sys.stdout = open('log_test1.log', 'w')

import teaathome
import pyhop
import random

pyhop.declare_operators(teaathome.goto, teaathome.open, teaathome.grasp, teaathome.place, teaathome.close, teaathome.check, teaathome.weigh, teaathome.placein, teaathome.turnonkettlebase, teaathome.access, teaathome.opencoldtap, teaathome.pourintocup)
pyhop.declare_methods('taskmaketea', teaathome.maketea)
print('')
pyhop.print_operators()
print('')
pyhop.print_methods()
print('')

def test1():
	"""!@brief (Helper function) Create a state object for test 1.
	@return state state
	"""
	# TODO
	state = pyhop.State('Test1')
	return state

print('')
print('''Running: pyhop.pyhop(test1(),[('taskmaketea','robot','teabag', 1)],verbose=2)''')
print('')

pyhop.pyhop(test1(),[('taskmaketea','robot','teabag', 1)],verbose=2)

sys.stdout.close()

sys.stdout = sys.__stdout__
print('Result log file: logs/test1.log')

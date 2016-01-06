import sys
sys.stdout = open('log_test3.log', 'w')

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

def test3():
	"""!@brief (Helper function) Create a state object for test 3.
	@return state state
	"""
	state = pyhop.State('Test3')
	return state

print('')
print('''Running test3: pyhop.pyhop(test3(),[('taskmaketea','robot','teabag', 2)],verbose=2)''')
print('')

pyhop.pyhop(test3(),[('taskmaketea','robot','teabag', 2)],verbose=2)

sys.stdout.close()

sys.stdout = sys.__stdout__
print('Result log file: logs/test3.log')

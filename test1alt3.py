import teaathome
import pyhop
import random
import sys
reload(teaathome)
reload(pyhop)

sys.stdout = open('logs/test1alt3.log', 'w')

def test1():
	"""!@brief (Helper function) Create a state object for test 1 with a slightly different environment.
	The kettle is open, empty and it is on location shelf1.
	@return state state
	"""
	state = pyhop.State('Test1 alt 2')
	state.TOTAL_NUMBER_OF_TEACUPS = 1
	state.NUMBER_OF_DIRTY_TEACUPS = 0
	state.loc = {'robot':teaathome.Location.startlocation, 'teacup1':teaathome.Location.countertop, 'coldtap':teaathome.Location.kitchensink, 'kettle':teaathome.Location.shelf1, 'teabag':teaathome.Location.countertop}
	teacups = 1
	while teacups <= state.TOTAL_NUMBER_OF_TEACUPS:
		state.loc['teacup'+str(teacups)] = teaathome.Location.countertop
		teacups = teacups + 1
		
	state.accessible = {'kettle':teaathome.Accessible.yes, 'kettlebase':teaathome.Accessible.yes, 'coldtap':teaathome.Accessible.yes, 'teabag':teaathome.Accessible.yes}
	teacups = 1
	while teacups <= state.TOTAL_NUMBER_OF_TEACUPS:
		state.accessible['teacup'+str(teacups)] = teaathome.Accessible.yes
		teacups = teacups + 1
		
	state.itemstate = {'kettle':{'openstate':teaathome.Itemstate.open, 'fillstate':teaathome.Itemstate.empty, 'tempstate':teaathome.Itemstate.cold}, 'coldtap':{'openstate':teaathome.Itemstate.closed}}

	for x in range(1, state.TOTAL_NUMBER_OF_TEACUPS + 1):
		state.itemstate['teacup'+str(x)] = {'cleanstate':teaathome.Itemstate.clean, 'fillstate':teaathome.Itemstate.empty, 'tempstate':teaathome.Itemstate.cold}
	#dirtycups = 1
	'''while dirtycups <= state.NUMBER_OF_DIRTY_TEACUPS:
		cup = 'teacup'+str(random.randint(1,state.TOTAL_NUMBER_OF_TEACUPS))
		if(state.itemstate[cup]['cleanstate'] == teaathome.Itemstate.unknown):
			state.itemstate[cup]['cleanstate'] = teaathome.Itemstate.dirty
			dirtycups = dirtycups + 1'''
	'''cleancups = 0
	while cleancups <= state.NUMBER_OF_DIRTY_TEACUPS:
		cup = 'teacup'+str(random.randint(1, state.TOTAL_NUMBER_OF_TEACUPS))
		if(state2.itemstate[cup]['cleanstate'] == Itemstate.unknown):
			state2.itemstate[cup]['cleanstate'] = Itemstate.clean
			cleancups = cleancups + 1'''
		
	state.currentcup = ''
	return state

print('''Running: pyhop.pyhop(teaathome.setupRobotArm(test1()),[('taskmaketea','robot','teabag', 1)],verbose=2)''')
print('')

teaathome.setupTeaAtHome()
pyhop.print_operators()
print('')
pyhop.print_methods()
print('')

pyhop.pyhop(teaathome.setupRobotArm(test1()),[('taskmaketea','robot','teabag', 1)],verbose=2)

sys.stdout.close()

sys.stdout = sys.__stdout__
print('Result log file: logs/test1alt3.log')

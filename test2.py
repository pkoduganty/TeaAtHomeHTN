import teaathome
import pyhop
import random
import sys
reload(teaathome)
reload(pyhop)

sys.stdout = open('logs/test2.log', 'w')

def test2():
	"""!@brief (Helper function) Create a state object for test 2.
	@return state state
	"""
	state = pyhop.State('Test2')
	state.TOTAL_NUMBER_OF_TEACUPS = 76
	state.NUMBER_OF_DIRTY_TEACUPS = 30
	state.loc = {'robot':teaathome.Location.startlocation, 'coldtap':teaathome.Location.kitchensink, 'kettle':teaathome.Location.kettlebase, 'teabag':teaathome.Location.countertop}
	teacups = 1
	while teacups <= state.TOTAL_NUMBER_OF_TEACUPS:
		state.loc['teacup'+str(teacups)] = teaathome.Location((random.randint(6, 13)))
		teacups = teacups + 1
		
	state.accessible = {'kettle':teaathome.Accessible.yes, 'kettlebase':teaathome.Accessible.yes, 'coldtap':teaathome.Accessible.yes, 'teabag':teaathome.Accessible.yes}
	teacups = 1
	while teacups <= state.TOTAL_NUMBER_OF_TEACUPS:
		state.accessible['teacup'+str(teacups)] = teaathome.Accessible.yes
		teacups = teacups + 1
		
	state.itemstate = {'kettle':{'openstate':teaathome.Itemstate.closed, 'fillstate':teaathome.Itemstate.empty, 'tempstate':teaathome.Itemstate.cold}, 'coldtap':{'openstate':teaathome.Itemstate.closed}}

	for x in range(1, state.TOTAL_NUMBER_OF_TEACUPS + 1):
		state.itemstate['teacup'+str(x)] = {'cleanstate':teaathome.Itemstate.unknown, 'fillstate':teaathome.Itemstate.empty, 'tempstate':teaathome.Itemstate.cold}
	dirtycups = 1
	while dirtycups <= state.NUMBER_OF_DIRTY_TEACUPS:
		cup = 'teacup'+str(random.randint(1,state.TOTAL_NUMBER_OF_TEACUPS))
		if(state.itemstate[cup]['cleanstate'] == teaathome.Itemstate.unknown):
			state.itemstate[cup]['cleanstate'] = teaathome.Itemstate.dirty
			dirtycups = dirtycups + 1
	"""cleancups = 0
	while cleancups <= numcupsknownclean:
		cup = 'teacup'+str(random.randint(1, state.TOTAL_NUMBER_OF_TEACUPS))
		if(state2.itemstate[cup]['cleanstate'] == Itemstate.unknown):
			state2.itemstate[cup]['cleanstate'] = Itemstate.clean
			cleancups = cleancups + 1"""
		
	state.currentcup = ""
	return state

	#goal = pyhop.Goal('goal 2')
	#goal.loc = {'robot':Location.startlocation, 'kettle':Location.kettlebase, 'teabag':Location.inteacup}
	#goal.itemstate = {'kettle':{'openstate':Itemstate.closed, 'fillstate': Itemstate.empty}, 'coldtap':{'openstate':Itemstate.closed}}
	#goal.robotarm = {'robot':RobotArm.free}
	#pyhop.print_goal(goal)

print('''Running: pyhop.pyhop(teaathome.setupRobotArm(test2()),[('taskmaketea','robot','teabag', 1)],verbose=2)''')
print('')

teaathome.setupTeaAtHome()
pyhop.print_operators()
print('')
pyhop.print_methods()
print('')

pyhop.pyhop(teaathome.setupRobotArm(test2()),[('taskmaketea','robot','teabag', 1)],verbose=2)

sys.stdout.close()

sys.stdout = sys.__stdout__
print('Result log file: logs/test2.log')

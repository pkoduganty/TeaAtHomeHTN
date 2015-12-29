"""
Tea@home - Code for
"""

from enum import Enum
import pyhop
import random
reload(pyhop)

class Itemstate(Enum):
	closed = 0
	open = 1
	full = 2
	empty = 3
	hot = 4
	cold = 5
	clean = 6
	dirty = 7
	unknown = 8
	taken = 9

# string names must match with enum fields!
class RobotArm(Enum):
	free = 0
	kettle = 1
	teacup = 2
	teabag = 3
    
class Location(Enum):
	kettlebase = 0
	startlocation = 1
	kitchensink = 2
	countertop = 3
	robotarm = 4
	inteacup = 5
	"""cupboard 1"""
	shelf1 = 6
	shelf2 = 7
	shelf3 = 8
	shelf4 = 9
	"""cupboard 2"""
	shelf5 = 10	
	shelf6 = 11
	shelf7 = 12
	shelf8 = 13
   
class Accessible(Enum):
	no = 0
	yes = 1
	
numcupstotal = 5
numcupsknowndirty = 3

def getrandomcupstate(cup):
	if (cup == 'teacup' + str(numcupstotal)):
		return Itemstate.clean
	return (random.randint(6, 7))

"""@brief: Changes the location of the robot.
	@param: state current state
	@param: robot robot
	@param: location destination of the robot"""
def goto(state, robot, location):
	if state.loc[robot] != location:
		state.loc[robot] = location
	else:
		print("\n---Robot is allready at location - so goto does nothing!---")
	return state

"""@brief: Item is accessible if the robot and the item have the same location (simplified)
	@param: state current state
	@param: robot robot
	@param: item item"""
def access(state, robot, item):
	if state.loc[robot] == state.loc[item]:
		#state.accessible[x] == Accessible.yes;
		return state
	else: return False

"""@brief: Check if an item has a specific value
	@param: state current state
	@param: item item
	@param: key property of the item
	@param: expectedvalue reference to check against"""
def check(state, item, key, expectedvalue):
	if state.itemstate[item][key] == expectedvalue:
		return state
	else: return False
    
"""@brief: Operator to open an item
	@param: state current state
	@param: robot robot
	@param: item item to open"""
def open(state, robot, item):
	if state.loc[robot] == state.loc[item]:
		if state.robotarm[robot] == RobotArm.free:
			if state.itemstate[item]['openstate'] == Itemstate.closed:
				state.itemstate[item]['openstate'] = Itemstate.open
				return state
			else: return False
		else: return False
	else: return False

"""@brief: Operator to close an item
	@param: state current state
	@param: robot robot
	@param: item item to close"""
def close(state, robot, item):
	if state.loc[robot] == state.loc[item]:
		if state.robotarm[robot] == RobotArm.free:
			if state.itemstate[item]['openstate'] == Itemstate.open:
				state.itemstate[item]['openstate'] = Itemstate.closed
				return state
			else: return False
		else: return False
	else: return False

"""@brief: Determine if the item is full or empty
	@param: state current state
	@param: robot robot
	@param: item item
	@param: expectedvalue value it should have to go on"""
def weigh(state, robot, item, expectedvalue):
	if state.itemstate[item]['fillstate'] == expectedvalue:
		return state
	else: return False
    
"""@brief: Operator to grasp an item
	@param: state current state
	@param: robot robot
	@param: item item to grasp"""
def grasp(state, robot, item):
	if state.loc[robot] == state.loc[item]:
		if state.robotarm[robot] == RobotArm.free:
			state.robotarm[robot] = RobotArm[item]
			state.loc[item] = Location.robotarm
			return state
		else: return False
	else: return False

"""@brief: Operator to grasp an item
	@param: state current state
	@param: robot robot
	@param: item item to grasp
	@param: location location to place the item on"""
def place(state, robot, item, location):
	if state.loc[robot] == location:
		if state.robotarm[robot] == RobotArm[item]:
			state.loc[item] = location
			state.robotarm[robot] = RobotArm.free
			return state
		else: return False
	else: return False

"""@brief: Place teabag from robot arm into a teacup
	@param: state current state
	@param: robot robot
	@param: targetitem targetitem
	@param: robotitem item the robot is holding"""
def placein(state, robot, teacup, teabag):
	if state.loc[robot] == state.loc[teacup]:
		if state.robotarm[robot] == RobotArm[teabag]:
			if state.loc[teacup] == Location.countertop:
				state.loc[teabag] = Location.inteacup
				state.robotarm[robot] = RobotArm.free
				return state
			else: return False
		else: return False
	else: return False

"""@brief: Operator to boil water
	@param: state current state
	@param: robot robot
	@param: item item on top of the kettlebase"""
def turnonkettlebase(state, robot, item):
	if state.loc[robot] == Location.kettlebase:
		if state.robotarm[robot] == RobotArm.free:
			if state.loc[item] == Location.kettlebase:
				if state.itemstate[item]['fillstate'] == Itemstate.full:
					state.itemstate[item]['tempstate'] = Itemstate.hot
					return state
				else: return False
			else: return False
		else: return False
	else: return False

def opencoldtap(state, robot):
	if state.loc[robot] == state.loc['coldtap']:
		if state.robotarm[robot] == RobotArm.free:
			if state.itemstate['coldtap']['openstate'] == Itemstate.closed:
				state.itemstate['coldtap']['openstate'] = Itemstate.open
				if state.itemstate['kettle']['openstate'] == Itemstate.open:
					state.itemstate['kettle']['fillstate'] = Itemstate.full
					return state
				else: return False
			else: return False
		else: return False
	else: return False

def pourintocup(state, robot, teacup):
	if state.loc[robot] == state.loc[teacup]:
		if state.robotarm[robot] == RobotArm.kettle:
			if state.itemstate['kettle']['openstate'] == Itemstate.open:
				if state.itemstate['kettle']['tempstate'] == Itemstate.hot:
					if state.itemstate['kettle']['fillstate'] == Itemstate.full:
						state.itemstate[teacup]['fillstate'] = Itemstate.full
						state.itemstate[teacup]['tempstate'] = Itemstate.hot
						state.itemstate['kettle']['fillstate'] = Itemstate.empty
						state.itemstate['kettle']['tempstate'] = Itemstate.cold
						return state
					else: return False
				else: return False
			else: return False
		else: return False
	else: return False
	
pyhop.declare_operators(goto, open, grasp, place, close, check, weigh, placein, turnonkettlebase, access, opencoldtap, pourintocup)
print('')
pyhop.print_operators()
print('')

def maketea(state, robot, teabag, number):
	task = [('taskpreparehotwater', robot), ('taskgetcleancup', robot), ('taskfinalizetea', robot, teabag)]
	teas = 1
	while (teas <= number):
		task = task + task
		teas = teas + 1
	return task
pyhop.declare_methods('taskmaketea', maketea)

"""Prepare Kettle methods"""

def preparehotwater(state, robot):
	if (state.itemstate['kettle']['fillstate'] == Itemstate.full):
		if (state.itemstate['kettle']['tempstate'] == Itemstate.hot):
			return []
		else:
			if (state.loc['kettle'] != Location.kettlebase):
				tasks = [('goto', robot, 'kettle'), ('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, 'kettlebase'), ('place', robot, 'kettle', 'kettlebase'), ('taskboilwater', robot)]
			else:
				tasks = [('taskboilwater', robot)]
			return tasks 
	else:
		# Everything
		return [('tasplacekettleinsink', robot), ('taskfillkettle', robot), ('taskplacekettleonbase', robot), ('taskboilwater', robot)]
	"""('taskcheckkettlefill', robot), removed"""
pyhop.declare_methods('taskpreparehotwater', preparehotwater)

def checkkettlefill(state, robot):
	return [('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('check', 'kettle', 'openstate', Itemstate.closed), ('grasp', robot, 'kettle'), ('weigh', robot, 'kettle', Itemstate.empty), ('place', robot, 'kettle', Location.kettlebase)]
pyhop.declare_methods('taskcheckkettlefill', checkkettlefill)

def placekettleinsink(state, robot):
	return [('goto', robot, state.loc['kettle']), ('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.kitchensink), ('place', robot, 'kettle', Location.kitchensink)]
pyhop.declare_methods('tasplacekettleinsink', placekettleinsink)

def fillkettle(state, robot):
	return [('open', robot, 'kettle'), ('opencoldtap', robot), ('close', robot, 'coldtap'), ('close', robot, 'kettle')]
pyhop.declare_methods('taskfillkettle', fillkettle)

def placekettleonbase(state, robot):
	return [ ('taskbringkettletobase', robot), ('place', robot, 'kettle', Location.kettlebase)]
pyhop.declare_methods('taskplacekettleonbase', placekettleonbase)

def bringkettletobase(state, robot):
	return [('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.kettlebase)]
pyhop.declare_methods('taskbringkettletobase', bringkettletobase)

def boilwater(state, robot):
	return [ ('goto', robot, state.loc['kettle']), ('turnonkettlebase', robot, 'kettle')]
pyhop.declare_methods('taskboilwater', boilwater)

"""prepare cup methods"""

def getcleancup(state, robot):
	return [('taskcheckcupdirty', robot), ('taskplacecup', robot)]
pyhop.declare_methods('taskgetcleancup', getcleancup)

def checkcupdirty(state, robot):
	teacupnum = 1
	teacup = 'teacup' + str(teacupnum)
	task = []
	for x in xrange(numcupstotal):
		task = task + [('goto', robot, state.loc[teacup]), ('access', robot, teacup), ('grasp', robot, teacup), ('check', teacup, 'cleanstate', Itemstate.clean)]
		state.itemstate[teacup]['cleanstate'] = getrandomcupstate(teacup)
		if(state.itemstate[teacup]['cleanstate'] == Itemstate.clean):
			return task
	return task
pyhop.declare_methods('taskcheckcupdirty', checkcupdirty)

def placecup(state, robot):
	tasks = [('place', robot, 'teacup', Location.countertop)]
	if state.loc['robot'] != Location.countertop:
		tasks = [('goto', robot, Location.countertop)] + tasks
	return tasks
pyhop.declare_methods('taskplacecup', placecup)

"""brew tea"""

def finalizetea(state, robot, teabag):
	return[('taskprepareteabag', robot, teabag), ('taskbrewtea', robot)]
pyhop.declare_methods('taskfinalizetea', finalizetea)

def prepareteabag(state, robot, teabag):
	return [('taskgetteabag', robot, teabag), ('taskplacebagincup', robot, teabag) ]
pyhop.declare_methods('taskprepareteabag', prepareteabag)

def getteabag(state, robot, teabag):
	return [('goto', robot, state.loc['teabag']), ('access', robot, 'teabag'), ('grasp', robot, 'teabag')]
pyhop.declare_methods('taskgetteabag', getteabag)

def placebagincup(state, robot, teabag):
	return[('goto', robot, Location.countertop), ('access', robot, 'teacup'), ('placein', robot, 'teacup', teabag)]
pyhop.declare_methods('taskplacebagincup', placebagincup)

def brewtea(state, robot):
	return[('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('open', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.countertop), ('pourintocup', robot, 'teacup'), ('goto', robot, Location.kettlebase), ('place', robot, 'kettle', Location.kettlebase), ('close', robot, 'kettle')]
pyhop.declare_methods('taskbrewtea', brewtea)

print('')
pyhop.print_methods()
print('')

state2 = pyhop.State('state2')
state2.loc = {'robot':Location.startlocation, 'coldtap':Location.kitchensink, 'kettle':Location.kettlebase, 'teacup':Location.countertop, 'teabag':Location.countertop}
teacups = 1
while teacups < numcupstotal:
	state2.loc['teacup'+str(teacups)] = random.randint(6, 13)
	teacups = teacups + 1
	
state2.accessible = {'kettle':Accessible.yes, 'kettlebase':Accessible.yes, 'coldtap':Accessible.yes, 'teabag':Accessible.yes}
teacups = 1
while teacups < numcupstotal:
	state2.accessible['teacup'+str(teacups)] = Accessible.yes
	teacups = teacups + 1
	
state2.itemstate = {'kettle':{'openstate':Itemstate.closed, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}, 'teacup':{'cleanstate':Itemstate.clean, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}, 'coldtap':{'openstate':Itemstate.closed}}
teacups = 1
while teacups < numcupstotal:
	if(teacups < numcupsknowndirty):
		state2.itemstate['teacup'+str(teacups)] = {'cleanstate':Itemstate.dirty, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}
	else:
		state2.itemstate['teacup'+str(teacups)] = {'cleanstate':Itemstate.unknown, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}
	teacups = teacups + 1
	

state2.robotarm = {'robot':RobotArm.free}

goal2 = pyhop.Goal('goal1')
goal2.loc = {'robot':Location.startlocation, 'kettle':Location.kettlebase, 'teacup':Location.countertop, 'teabag':Location.inteacup}
goal2.itemstate = {'kettle':{'openstate':Itemstate.closed, 'fillstate': Itemstate.empty}, 'coldtap':{'openstate':Itemstate.closed}, 'teacup':{'fillstate':Itemstate.full, 'tempstate':Itemstate.hot}}
goal2.robotarm = {'robot':RobotArm.free}
pyhop.print_goal(goal2)

print('')
print("""
********************************************************************************
Call pyhop.pyhop(state1,[('taskmaketea','robot','teabag')]) with different verbosity levels
********************************************************************************
""")
print('')

"""print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
pyhop.pyhop(state1,[('taskmaketea','robot','teabag')])

print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
pyhop.pyhop(state1,[('taskmaketea','robot','teabag')],verbose=1)

print('- If verbose=2, Pyhop also prints a note at each recursive call:')
pyhop.pyhop(state1,[('taskmaketea','robot','teabag')],verbose=2)"""

print('- If verbose=3, Pyhop also prints the intermediate states:')
pyhop.pyhop(state2,[('taskmaketea','robot','teabag', 1)],verbose=3)

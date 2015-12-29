"""
Tea@home - Code for
"""

from enum import Enum
import pyhop
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

# string names must match with enum fields!
class RobotArm(Enum):
	free = 0
	kettle = 1
	teacup = 2
	teabag = 3
    
class Location(Enum):
	kettlebase = 0
	shelf = 1
	startlocation = 2
	kitchensink = 3
	countertop = 4
	robotarm = 5
	inteacup = 6
	
class TeacupState():
	clean = 0
	dirty = 1
	taken = 2
    
class Accessible(Enum):
	no = 0
	yes = 1

"""@brief: Changes the location of the robot.
	@param: state current state
	@param: robot robot
	@param: location destination of the robot"""
def goto(state, robot, location):
	if state.loc[robot] != location:
		state.loc[robot] = location
		return state
	else: return False

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

def maketea(state, robot, teabag):
	return [('taskpreparehotwater', robot), ('taskgetcleancup', robot), ('taskfinalizetea', robot, teabag)]
pyhop.declare_methods('taskmaketea', maketea)

"""Prepare Kettle methods"""

def preparehotwater(state, robot):
	if (state.itemstate['kettle']['tempstate'] == Itemstate.hot):
		return []
	else: return [('taskcheckkettlefill', robot), ('tasplacekettleinsink', robot), ('taskfillkettle', robot), ('taskplacekettleonbase', robot), ('taskboilwater', robot)]
pyhop.declare_methods('taskpreparehotwater', preparehotwater)	

def checkkettlefill(state, robot):
	return [('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('check', 'kettle', 'openstate', Itemstate.closed), ('grasp', robot, 'kettle'), ('weigh', robot, 'kettle', Itemstate.empty), ('place', robot, 'kettle', Location.kettlebase)]
pyhop.declare_methods('taskcheckkettlefill', checkkettlefill)

def placekettleinsink(state, robot):
	return [('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.kitchensink), ('place', robot, 'kettle', Location.kitchensink)]
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
	return [ ('turnonkettlebase', robot, 'kettle')]
pyhop.declare_methods('taskboilwater', boilwater)

"""prepare cup methods"""

def getcleancup(state, robot):
	return [('taskcheckcupdirty', robot), ('taskplacecup', robot)]
pyhop.declare_methods('taskgetcleancup', getcleancup)

def checkcupdirty(state, robot):
	return [('goto', robot, state.loc['teacup']), ('access', robot, 'teacup'), ('grasp', robot, 'teacup'), ('check', 'teacup', 'cleanstate', Itemstate.clean)]
pyhop.declare_methods('taskcheckcupdirty', checkcupdirty)

def placecup(state, robot):
	return [('goto', robot, Location.countertop), ('place', robot, 'teacup', Location.countertop)]
pyhop.declare_methods('taskplacecup', placecup)

"""brew tea"""

def finalizetea(state, robot, teabag):
	return[('taskprepareteabag', robot, teabag), ('taskbrewtea', robot)]
pyhop.declare_methods('taskfinalizetea', finalizetea)

def prepareteabag(state, robot, teabag):
	return [('taskgetteabag', robot, teabag), ('taskplacebagincup', robot, teabag) ]
pyhop.declare_methods('taskprepareteabag', prepareteabag)

def getteabag(state, robot, teabag):
	return [('goto', robot, Location.shelf), ('access', robot, 'teabag'), ('grasp', robot, 'teabag')]
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

state1 = pyhop.State('state1')
state1.loc = {'robot':Location.startlocation, 'coldtap':Location.kitchensink, 'kettle':Location.kettlebase, 'teacup':Location.countertop, 'teabag':Location.shelf}
state1.accessible = {'kettle':Accessible.yes, 'kettlebase':Accessible.yes, 'coldtap':Accessible.yes, 'teacup':Accessible.yes, 'teabag':Accessible.yes}
state1.itemstate = {'kettle':{'openstate':Itemstate.closed, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}, 'teacup':{'cleanstate':Itemstate.clean, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}, 'coldtap':{'openstate':Itemstate.closed}}
state1.robotarm = {'robot':RobotArm.free}

goal1 = pyhop.Goal('goal1')
goal1.loc = {'robot':Location.startlocation, 'kettle':Location.kettlebase, 'teacup':Location.countertop, 'teabag':Location.inteacup}
goal1.itemstate = {'kettle':{'openstate':Itemstate.closed, 'fillstate': Itemstate.empty}, 'coldtap':{'openstate':Itemstate.closed}, 'teacup':{'fillstate':Itemstate.full, 'tempstate':Itemstate.hot}}
goal1.robotarm = {'robot':RobotArm.free}
pyhop.print_goal(goal1)

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
pyhop.pyhop(state1,[('taskmaketea','robot','teabag')],verbose=3)

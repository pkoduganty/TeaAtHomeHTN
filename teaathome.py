"""
Tea@home - Code for
"""

from enum import Enum
import pyhop

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
	teacup1 = 2
	teabag = 3
    
class Location(Enum):
	kettlebase = 0
	countertop = 1
	door = 2
	kitchensink = 3
    
class Accessible(Enum):
	no = 0
	yes = 1

"""@brief: Changes the location of the robot. If the robot is holding an item, change the location of the item, too!
	@param: state current state
	@param: robot robot
	@param: location destination of the robot"""
def goto(state, robot, location):
	if state.loc[robot] != location:
		state.loc[robot] = location
		if state.robotarm[robot] != RobotArm.free:
			state.loc[state.robotarm[robot].name] = location
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
	@param: item item"""
def open(state, robot, item):
	if state.loc[robot] == state.loc[item]:
		if state.itemstate[item]['openstate'] == Itemstate.closed:
			if state.robotarm[robot] == Robotarm.free:
				state.itemstate[item]['openstate'] = Itemstate.open
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
		if state.robotarm == Robotarm.free:
			state.robotarm[robot] = Robotarm[item];
			return state
		else: return False
	else: return False

"""@brief: Operator to position an item
	@param: state current state
	@param: a robot
	@param: x item to position
	@param: y location to position on"""
def position(state, a, x, y):
	if state.loc[a] == y:
		if state.loc[x] == a:
			state.loc[x] = y
			state.robotarm[a] = Robotarm.free
			return state
		else: return False
	else: return False

"""@brief: Operator to place an item on corresponding item
	@param: state current state
	@param: a robot
	@param: x item to place
	@param: y item on which other item will be placed"""
def replace(state, a, x, y):
	if state.loc[a] == state.loc[y]:
		if state.loc[x] == a:
			if state.accessible[y] == Accessible.yes:
				state.loc[x] = y
				state.robotarm = Robotarm.free
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
		if state.itemstate[item]['openstate'] == Itemstate.open:
			if state.robotarm[robot] == Robotarm.free:
				state.itemstate[item]['openstate'] = Itemstate.closed
				return state
			else: return False
		else: return False
	else: return False

"""@brief: Operator to place an item next to another
	@param: state current state
	@param: a robot
	@param: x item to place
	@param: y item to place next to"""
def placenextto(state, a, x, y):
	if state.loc[a] == state.loc[y]:
		if state.loc[x] == a:
			state.loc[x] = state.loc[y]
			state.robotarm[a] = Robotarm.free
		else: return False
	else: return False

"""@brief: Operator to place item in another item
	@param: state current state
	@param: a robot
	@param: x item to be placed
	@param: y item in which other item will be placed"""
def placein(state, a, x, y):
	if state.loc[a] == state.loc[y]:
		if state.accessible[y] == Accessible.yes:
			if state.loc[x] == a:
				state.loc[x] = y
				return state
			else: return False
		else: return False
	else: return False

"""@brief: Operator to boil water in kettle
	@param: state current state
	@param: a robot
	@param: x kettle"""
def boilwaterinkettle(state, a, x):
	if state.loc[a] == state.loc[x]:
		if state.accessible[x] == Accessible.yes:
			if state.robotarm[a] == Robotarm.free:
				if state.itemfillstate[x] == Itemstate.full:
					state.itemfilstate[x] = Itemstate.hot
					return state
				else: return False
			else: return False
		else: return False
	else: return False

pyhop.declare_operators(goto, open, grasp, position, replace, close, placenextto, placein, boilwaterinkettle)
print('')
pyhop.print_operators()
print('')

def maketea(state, robot, teabag):
	return [('layer1.1', robot), ('layer1.2', robot, teabag), ('layer1.3', robot)]
pyhop.declare_methods('layer0', maketea)

def preparehotwater(state, robot):
    return [('layer2.1', robot)]
def getcleancup(state, robot):
    return [('layer2.2', robot)]
pyhop.declare_methods('layer1.1', preparehotwater, getcleancup)

def brewtea(state, robot, teabag):
    return [('layer2.3', robot, teabag)]
pyhop.declare_methods('layer1.2', brewtea)

def finalizetea(state, robot):
    return[('access', robot), ('open', robot, 'kettle'), ('grasp', robot, 'kettle'), ('pourintocup', robot, 'kettle'), ('replace', robot, 'kettle')]
pyhop.declare_methods('layer1.3', finalizetea)

def preparekettle(state, a):
	return [('layer3.1', a)]
def boilwater(state, a):
	return [('layer3.2', a)]
pyhop.declare_methods('layer2.1', preparekettle, boilwater)

def checkcupdirty(state, a):
    return [('access', a, x), ('grasp', a, x), ('check', a, x, y)]
def placecup(state, a):
    return [('goto', a, x), ('placenextto', a, y)]
pyhop.declare_methods('layer2.2', checkcupdirty, placecup)

def getteabag(state, robot, teabag):
    return[('goto', a, x), ('access', a, y), ('grasp', a, x)]
def placebagincup(state, a):
    return[('access', a, x), ('grasp', a, x), ('placein', a, x, y)]
pyhop.declare_methods('layer2.3', getteabag, placebagincup)

def checkkettlefill(state, robot):
    return [('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('check', 'kettle', 'openstate', Itemstate.closed), ('grasp', robot, 'kettle'), ('weigh', robot, 'kettle', Itemstate.empty)]
def placekettleinsink(state, robot):
    return [('goto', robot, Location.kitchensink), ('access', robot, 'kitchensink'), ('position', robot, 'kettle', Location.kitchensink)]
def fillkettle(state, robot):
    return [('open', robot, 'kettle'), ('open', robot, 'coldtap'), ('close', robot, 'coldtap'), ('close', robot, 'kettle')]
pyhop.declare_methods('layer3.1', checkkettlefill, placekettleinsink, fillkettle)

def bringkettletobase(state, robot):
    return [('grasp', robot, 'kettle'), ('goto', robot, Location.kettlebase)]
def placekettleonbase(state, robot):
    return [('replace', robot, 'kettle', Location.kettlebase), ('putonkettle', robot, 'kettle')]
pyhop.declare_methods('layer3.2', bringkettletobase, placekettleonbase)

print('')
pyhop.print_methods()
print('')

state1 = pyhop.State('state1')
state1.loc = {'robot':Location.door, 'kettle':Location.kettlebase, 'kettlebase':Location.countertop, 'kitchensink':Location.kitchensink, 'coldtap':Location.kitchensink, 'teacup':Location.countertop, 'peppermintTeaBag':Location.countertop}
state1.accessible = {'kettle':Accessible.yes, 'kettlebase':Accessible.yes, 'coldtap':Accessible.yes, 'teacup1':Accessible.yes, 'peppermintTeaBag':Accessible.yes}
state1.itemstate = {'kettle':{'openstate':Itemstate.closed, 'fillstate':Itemstate.empty, 'tempstate':Itemstate.cold}, 'teacup1':{'cleanstate':Itemstate.clean, 'fillstate':Itemstate.full}, 'coldtap':{'openstate':Itemstate.closed}}
state1.robotarm = {'robot':RobotArm.free}

print("""
********************************************************************************
Call pyhop.pyhop(state1,[('layer0','robot','peppermintTeaBag')]) with different verbosity levels
'''********************************************************************************
""")

"""print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
pyhop.pyhop(state1,[('travel','robot','home','park')])

print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
pyhop.pyhop(state1,[('travel','robot','home','park')],verbose=1)

print('- If verbose=2, Pyhop also prints a note at each recursive call:')
pyhop.pyhop(state1,[('travel','robot','home','park')],verbose=2)"""

print('- If verbose=3, Pyhop also prints the intermediate states:')
pyhop.pyhop(state1,[('layer0','robot','peppermintTeaBag')],verbose=3)

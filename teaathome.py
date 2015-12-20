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
	clean = 5
    
class RobotArm(Enum):
	free = 0
	occupied = 1
    
class Location(Enum):
	kettlebase = 0
	countertop = 1
	sink = 2
	door = 3
	kitchensink = 4
    
class Accessible(Enum):
	no = 0
	yes = 1

"""@brief: Operator to change location
	@param: state current state
	@param: a robot
	@param: x location to move to
"""
def goto(state,robot,location):
	# remove if and error case?
	if state.loc[robot] != location:
		state.loc[robot] = location
		return state
	else: return False
	
"""TODO
	Currently only check if location of robot and item is the same
	Not changing state
"""
def access(state,robot,item):
	if state.loc[robot] == state.loc[item]:
		#state.accessible[x] == Accessible.yes;
		return state
	else: return False
	
	
    
"""@brief: Operator to open item
	@param: state current state
	@param: a robot
	@param: x item to open"""
def open(state, a, x):
	if state.loc[a] == state.loc[x]:
		if state.accessible[x] == Accessible.yes:
			if state.itemopen[x] == Itemstate.closed:
				if state.handsfree[a] == Robotarm.free:
					state.itemopen[x] = Itemstate.open
					return state
				else: return False
			else: return False
		else: return False
	else: return False
    
"""@brief: Operator to grasp an item
	@param: state current state
	@param: a robot
	@param: x item to grasp"""
def grasp(state, a, x):
	if state.loc[a] == state.loc[x]:
		if state.accessible[x] == Accessible.yes:
			if state.handsfree == Robotarm.free:
				state.loc[x] = a
				state.handsfree[a] = Robotarm.occupied;
				return state
			else: return False
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
			state.handsfree[a] = Robotarm.free
			return state
		else: return False
	else: return False
    
"""@brief: Operator to open a tap
	@param: state current state
	@param: a robot
	@param: x tap to open"""
def opentap(state, a, x):
	if state.loc[a] == state.loc[x]:
		if state.accessible[x] == Accessible.yes:
			if state.handsfree[a] == Robotarm.free:
				if state.itemopen[x] == Itemstate.closed:
					state.itemopen[x] = Itemstate.open
					return state
				else: return False
			else: return False
		else: return False
	else: return False

"""@brief: Operator to close a tap
	@param: state current state
	@param: a robot
	@param: x tap to open"""
def closetap(state, a, x):
	if state.loc[a] == state.loc[x]:
		if state.accessible[x] == Accessible.yes:
			if state.handsfree[a] == Robotarm.free:
				if state.itemopen[x] == Itemstate.open:
					state.itemopen[x] = Itemstate.closed
					return state
				else: return False
			else: return False
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
				state.handsfree = Robotarm.free
				return state
			else: return False
		else: return False
	else: return False

"""@brief: Operator to close an item
	@param: state current state
	@param: a robot
	@param: x item to close"""
def close(state, a, x):
	if state.loc[a] == state.loc[x]:
		if state.accessible[x] == Accessible.yes:
			if state.itemopen[x] == Itemstate.open:
				if state.handsfree[a] == Robotarm.free:
					state.itemopen[x] = Itemstate.closed
					return state
				else: return False
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
			state.handsfree[a] = Robotarm.free
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
			if state.handsfree[a] == Robotarm.free:
				if state.itemstate[x] == fullItemstate.full:
					state.itemstate[x] = Itemstate.hot
					return state
				else: return False
			else: return False
		else: return False
	else: return False

pyhop.declare_operators(goto, open, grasp, position, opentap, closetap, replace, close, placenextto, placein, boilwaterinkettle)
print('')
pyhop.print_operators()

# task
def maketea(state, a, x):
	if state.accessible[x] == Accessible.yes:
   	 return [('layer1.1',a), ('layer1.2',a, x), ('layer1.3',a, x)]
	return False
pyhop.declare_methods('layer0', maketea)

def preparehotwater(state, a):
    return [('layer2.1', a)]
def getcleancup(state, a):
    return [('layer2.2', a)]
pyhop.declare_methods('layer1.1', preparehotwater, getcleancup)

def brewtea(state, a, x):
    return [('layer2.3', a , x)]
pyhop.declare_methods('layer1.2', brewtea)

def finalizetea(state, a, x):
    return[('access', a, x), ('grasp', a, x), ('open', a, x), ('pourintocup', a, x, y), ('replace', a, x, y)]
pyhop.declare_methods('layer1.3', finalizetea)

def preparekettle(state, a):
	return [('layer3.1', a)]
def boilwater(state, a):
	return [('layer3.2', a)]
pyhop.declare_methods('layer2.1', preparekettle, boilwater)

def checkcupdirty(state, a):
    return [('access', a, x), ('grasp', a, x), ('compare-to', a, x, y)]
def placecup(state, a):
    return [('goto', a, x), ('placenextto', a, y)]
pyhop.declare_methods('layer2.2', checkcupdirty, placecup)

def getteabag(state, a):
    return[('goto', a, x), ('access', a, y), ('grasp', a, x)]
def placebagincup(state, a):
    return[('access', a, x), ('grasp', a, x), ('placein', a, x, y)]
pyhop.declare_methods('layer2.3', getteabag, placebagincup)

def checkkettlefill(state, a):
    return [('goto', 'robot', Location.kettlebase), ('access', 'robot', 'kettle'), ('compareto', a, y, z), ('open', a, y), ('grasp', a, y), ('checkweight', a, y)]
def placekettleinsink(state, a):
    return [('goto', a, x), ('position', a, y, x)]
def fillkettle(state, a):
    return [('opentap', a, x), ('closetab', a, x), ('close', a, y)]
pyhop.declare_methods('layer3.1', checkkettlefill, placekettleinsink, fillkettle)

def bringkettletobase(state, a):
    return [('grasp', a, x), ('goto', a, y)]
def placekettleonbase(state, a):
    return [('replace', a, x, y), ('putonkettle', a, y)]
pyhop.declare_methods('layer3.2', bringkettletobase, placekettleonbase)

print('')
pyhop.print_methods()

state1 = pyhop.State('state1')
state1.loc = {'robot':Location.door, 'kettle':Location.kettlebase, 'kettlebase':Location.countertop, 'coldtap':Location.kitchensink, 'teacup':Location.countertop, 'peppermitTeaBag':Location.countertop}
state1.accessible = {'kettle':Accessible.yes, 'kettlebase':Accessible.yes, 'coldtap':Accessible.yes, 'teacup1':Accessible.yes, 'peppermintTeaBag':Accessible.yes}
state1.itemopen = {'kettle':Itemstate.closed, 'coldtap':Itemstate.closed}
state1.itemstate = {'kettle':Itemstate.empty, 'teacup1':Itemstate.clean}
state1.handsfree = {'robot':RobotArm.free}

"""state1.dist = {'home':{'park':8}, 'park':{'home':8}}"""

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

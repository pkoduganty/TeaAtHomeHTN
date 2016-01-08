"""
Code for tea at home
"""

from enum import Enum
import pyhop
import random
reload(pyhop)

class Itemstate(Enum):
	'''!@brief Properties for items.
	Every item has properties to describe it's current and desired state: 'openstate', 'fillstate', 'tempstate' and 'cleanstate'
	Values for these fields are members of Itemstate to make it more robust against errors, expecially against typos.
	'''
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

class RobotArm(Enum):
	'''!@brief Properties of the robot arm.
	All items the robot can carry with his arm have a corresponding enum field in RobotArm.
	Because of a dynamic number of teacups, the teacup fields are created programmatically and RobotArm is recreated during runtime.
	E.g. RobotArm.teacup1, RobotArm.teacup2, ..., RobotArm.teacup75
	'''
	free = 0
	kettle = 1
	teabag = 2

class Location(Enum):
	'''!@brief Properties for items which can be moved.
	We do NOT use a hierarchy of locations (e.g. multiple shelfs in a cupboard).
	It is implicitely given, that shelf 1-4 are in cupboard 1 and shelf 5-8 are in cupboard 2.
	Exception: We declare the teabag as "Location.inteacup" as simplified solution.
	'''
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
	'''!@brief Properties if the item can be reached.
	Theoretically, items can be locked or barred. This would be declared in the state object (observation of the world).
	In our solution, all items are accessible but the robot is still checking if this is truely the case.
	'''
	no = 0
	yes = 1

def getrandomcupstate(state, cup):
	"""!@brief (Helper function) Randomly get a clean or dirty cup.
	@param state current state
	@param cup cup
	@return Itemstate <Itemstate.clean: 6> or <Itemstate.dirty: 7>"""
	if (state.itemstate[cup]['cleanstate'] == Itemstate.unknown):
		if ((cup == 'teacup' + str(state.TOTAL_NUMBER_OF_TEACUPS)) and (state.TOTAL_NUMBER_OF_TEACUPS - state.NUMBER_OF_DIRTY_TEACUPS > 0)):
			return Itemstate.clean
		return Itemstate(random.randint(6, 7))
	else:
		return state.itemstate[cup]['cleanstate']

def goto(state, robot, location):
	"""!@brief (Operator) Changes the location of the robot.
	Returns a textual warning if the robot is already in this location.
	@param state current state
	@param robot robot
	@param location destination of the robot
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] != location:
		state.loc[robot] = location
	else:
		print("\n****Robot is already at location " + location.name + " - so goto does nothing!****")
	return state

def access(state, robot, item):
	"""!@brief (Operator) Simple location check.
	Item is considered as accessible if it has the same location as the robot (simplified).
	@param state current state
	@param robot robot
	@param item item
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == state.loc[item]:
		return state
	else: 
		print("\n****Cannot access object " + item + "****")
		return False

def check(state, item, key, expectedvalue):
	"""!@brief (Operator) Check if an item has a specific value.
	@param state current state
	@param item item
	@param key property of the item e. g. 'cleanstate', 'fillstate', ...
	@param expectedvalue reference to check against
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.itemstate[item][key] == expectedvalue:
		return state
	else:
		print("****check of item " + item + " to state + " + exceptedvalue.name + " failed****")
		return False
    
def openitem(state, robot, item):
	"""!@brief (Operator) Operator to open an item.
	@param state current state
	@param robot robot
	@param item item to open
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == state.loc[item]:
		if state.robotarm[robot] == RobotArm.free:
			if state.itemstate[item]['openstate'] == Itemstate.closed:
				state.itemstate[item]['openstate'] = Itemstate.open
				return state
			else: 
				print("****open item " + item + " failed, item allready open****")
				return False
		else:
			print("****open item " + item + " failed, robot arm not free****")
			return False
	else: 
		print("****open item " + item + " failed, robot not at location + " + state.loc[item].name + " but at + " + state.loc[robot].name + "****")	
		return False

def close(state, robot, item):
	"""!@brief (Operator) Operator to close an item.
	@param state current state
	@param robot robot
	@param item item to close
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == state.loc[item]:
		if state.robotarm[robot] == RobotArm.free:
			if state.itemstate[item]['openstate'] == Itemstate.open:
				state.itemstate[item]['openstate'] = Itemstate.closed
				return state
			else:
				print("****close item " + item + " failed, item is allready closed****")			
				return False
		else:
			print("****close item " + item + " failed, robot arm not free****")		
			return False
	else:
		print("****close item " + item + " failed, robot not at location + " + state.loc[item].name + " but at + " + state.loc[robot].name + "****")	
		return False

def weigh(state, robot, item, expectedvalue):
	"""!@brief (Operator) Determine if the item is full or empty.
	@param state current state
	@param robot robot
	@param item item
	@param expectedvalue The value it should have
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.itemstate[item]['fillstate'] == expectedvalue:
		return state
	else: return False
    
def grasp(state, robot, item):
	"""!@brief (Operator) Operator to grasp an item.
	@param state current state
	@param robot robot
	@param item item to grasp
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	print(state.robotarm[robot])
	if state.loc[robot] == state.loc[item]:
		if state.robotarm[robot] == RobotArm.free:
			state.robotarm[robot] = RobotArm[item]
			state.loc[item] = Location.robotarm
			return state
		else:
			print("****grasp item " + item + " failed, robot arm not free****")			
			return False
	else:
		print("****grasp item " + item + " failed, robot not at location + " + state.loc[item].name + " but at + " + state.loc[robot].name + "****")		
		return False

def place(state, robot, item, location):
	"""!@brief (Operator) Operator to grasp an item.
	@param state current state
	@param robot robot
	@param item The item the robot is currently holding
	@param location The location to place the item on
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == location:
		if state.robotarm[robot] == RobotArm[item]:
			state.loc[item] = location
			state.robotarm[robot] = RobotArm.free
			return state
		else:
			print("****place item " + item + " at " + location.name + " failed, robot arm not holding item****")			
			return False
	else:
		print("****place item " + item + " failed, robot not at location + " + location.name + " but at + " + state.loc[robot] + "****")		
		return False

def placein(state, robot, teacup, teabag):
	"""!@brief (Operator) Place teabag from robot arm into a teacup.
	@param state current state
	@param robot robot
	@param teacup The teacup at the location of the robot
	@param teabag The teabag the robot is currently holding
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == state.loc[teacup]:
		if state.robotarm[robot] == RobotArm[teabag]:
			if state.loc[teacup] == Location.countertop:
				state.loc[teabag] = Location.inteacup
				state.robotarm[robot] = RobotArm.free
				return state
			else:
				print("****placein item " + teabag + "in " + teacup + " failed, " + teacup + " not at location countertop but at + " + state.loc[teacup].name + "****")				
				return False
		else:
			print("****placein item " + teabag + "in " + teacup + " failed, robot arm instead holding" + state.robotarm[robot].name + "****")				
			return False
	else:
		print("****placein item " + teabag + "in " + teacup + " failed, robot not at location " + state.loc[teacup].name + "but at + " + state.loc[robot].name + "****")		
		return False

def turnonkettlebase(state, robot, item):
	"""!@brief (Operator) Turn on the kettlebase.
	Make hot water if the kettle is on top of it and full. Robotarm has to be empty in order to turn on the kettlebase.
	@param state current state
	@param robot robot
	@param item The item on top of the kettlebase
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == Location.kettlebase:
		if state.robotarm[robot] == RobotArm.free:
			if state.loc[item] == Location.kettlebase:
				if state.itemstate[item]['fillstate'] == Itemstate.full:
					state.itemstate[item]['tempstate'] = Itemstate.hot
					return state
				else:
					print("****turnonkettlebase failed, kettle not full****")					
					return False
			else:
				print("****turnonkettlebase failed" + item + "not at kettlebase but at " + state.loc[kettle].name + "****")				
				return False
		else:
			print("****turnonkettlebase failed, robot arm not free but holding" + state.robotarm[robot].name +  "****")
			return False
	else:
		print("****turnonkettlebase failed, robot not at location kettlebase but at + " + state.loc[robot].name + "****")			
		return False

def opencoldtap(state, robot):
	"""!@brief (Operator) Open the coldtap.
	TODO location check for kettle?!?! add param for item?
	@param state current state
	@param robot robot
	@return state Returns the state object (success) or
	@return False In error case (fail)"""
	if state.loc[robot] == state.loc['coldtap']:
		if state.robotarm[robot] == RobotArm.free:
			if state.itemstate['coldtap']['openstate'] == Itemstate.closed:
				state.itemstate['coldtap']['openstate'] = Itemstate.open
				if state.itemstate['kettle']['openstate'] == Itemstate.open:
					state.itemstate['kettle']['fillstate'] = Itemstate.full
					return state
				else:
					print("****opencoldtap failed, kettle not open****")				
					return False
			else:
				print("****opencoldtap failed, coldtap allready open****")			
				return False
		else:
			print("****opencoldtab failed, robot arm not free but holding + " + state.robotarm[robot].name + "****")
			return False
	else:
		print("****opencoldtab failed, robot not at location coldtap but at + " + state.loc[robot].name + "****")	
		return False

def pourintocup(state, robot, teacup):
	"""!@brief (Operator) Pour water into the teacup.
	@param state current state
	@param robot robot
	@param teacup teacup"""
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
					else: 
						print("****pourintocup failed, kettle not full****")
						return False
				else: 
					print("****pourintocup failed, water in kettle not hot****")
					return False
			else: 
				print("****pourintocup failed, kettle not open****")
				return False
		else: 
			print("****pourintocup failed, robot not holding kettle but " + state.robotarm[robot].name + "****")
			return False
	else: 
		print("****pourintocup failed, robot not at location " + state.loc[teacup].name + " but at + " + state.loc[robot].name + "****")
		return False

pyhop.declare_operators(goto, openitem, grasp, place, close, check, weigh, placein, turnonkettlebase, access, opencoldtap, pourintocup)

def maketea(state, robot, teabag, number):
	task = [('taskpreparehotwater', robot), ('taskgetcleancup', robot), ('taskfinalizetea', robot, teabag)]
	teas = 1
	while (teas < number):
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
		return [('tasplacekettleinsink', robot), ('taskfillkettle', robot), ('taskplacekettleonbase', robot), ('taskboilwater', robot)]
pyhop.declare_methods('taskpreparehotwater', preparehotwater)

def checkkettlefill(state, robot):
	return [('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('check', 'kettle', 'openstate', Itemstate.closed), ('grasp', robot, 'kettle'), ('weigh', robot, 'kettle', Itemstate.empty), ('place', robot, 'kettle', Location.kettlebase)]
pyhop.declare_methods('taskcheckkettlefill', checkkettlefill)

def placekettleinsink(state, robot):
	return [('goto', robot, state.loc['kettle']), ('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.kitchensink), ('place', robot, 'kettle', Location.kitchensink)]
pyhop.declare_methods('tasplacekettleinsink', placekettleinsink)

def fillkettle(state, robot):
	return [('openitem', robot, 'kettle'), ('opencoldtap', robot), ('close', robot, 'coldtap'), ('close', robot, 'kettle')]
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
	if state.TOTAL_NUMBER_OF_TEACUPS == 0:
		print("\n****No cups, no Tea!!!!!1111Elf****")
		return False
	else:
		return [('taskcheckcupdirty', robot)]
pyhop.declare_methods('taskgetcleancup', getcleancup)

""" damit plan failed, muessten -numcups- alternative methoden fuer check geschrieben werden"""

def checkcupdirty(state, robot):
	task = []
	teacup = ""
	for x in range(1, state.TOTAL_NUMBER_OF_TEACUPS + 1):
		teacup = 'teacup' + str(x)
		if(state.itemstate[teacup]['cleanstate']!=Itemstate.taken):
			teacuploc = state.loc[teacup]
			task = task + [('goto', robot, state.loc[teacup]), ('access', robot, teacup), ('grasp', robot, teacup)]
			state.itemstate[teacup]['cleanstate'] = getrandomcupstate(state, teacup)
			if(state.itemstate[teacup]['cleanstate'] == Itemstate.clean):
				print ("\nCup is clean!\n")
				task = task + [('taskplacecup', robot, teacup)]
				state.currentcup = teacup
				return task 
			print ("\nCup is dirty!\n")
			task = task + [('place', robot, teacup, teacuploc)]
			
	if(state.itemstate[teacup]['cleanstate'] == Itemstate.clean):
		state.currentcup = teacup
		return task
	else: 
		print("\n****I found only dirty cups, you have to clean some first!****")
		return False
pyhop.declare_methods('taskcheckcupdirty', checkcupdirty)

def placecup(state, robot, teacup):
	tasks = [('goto', robot, Location.countertop), ('place', robot, teacup, Location.countertop)]
	return tasks
pyhop.declare_methods('taskplacecup', placecup)

"""brew tea"""

def finalizetea(state, robot, teabag):
	return[('taskprepareteabag', robot, teabag), ('taskbrewtea', robot, teabag)]
pyhop.declare_methods('taskfinalizetea', finalizetea)

def prepareteabag(state, robot, teabag):
	return [('taskgetteabag', robot, teabag), ('taskplacebagincup', robot, teabag) ]
pyhop.declare_methods('taskprepareteabag', prepareteabag)

def getteabag(state, robot, teabag):
	return [('goto', robot, state.loc['teabag']), ('access', robot, 'teabag'), ('grasp', robot, 'teabag')]
pyhop.declare_methods('taskgetteabag', getteabag)

def placebagincup(state, robot, teabag):
	if(state.currentcup == ""):
		return False
	state.itemstate[state.currentcup]['cleanstate'] = Itemstate.taken
	return[('goto', robot, Location.countertop), ('access', robot, state.currentcup), ('placein', robot, state.currentcup, teabag)]
pyhop.declare_methods('taskplacebagincup', placebagincup)

def brewtea(state, robot, teabag):
	return[('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('openitem', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.countertop), ('pourintocup', robot, state.currentcup), ('goto', robot, Location.kettlebase), ('place', robot, 'kettle', Location.kettlebase), ('close', robot, 'kettle')]
pyhop.declare_methods('taskbrewtea', brewtea)

def setupRobotArm(state):
	teacups = []
	for x in range(1, state.TOTAL_NUMBER_OF_TEACUPS + 1):
		teacups = teacups + ['teacup' + str(x)]
		teacups = [m.name for m in RobotArm] +  teacups
		RobotArm = Enum('RobotArm', teacups)
	return state

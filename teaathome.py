"""!@mainpage Making tea at home
@section Authors
Felix Hampe
Daniel Pyka

@section Course
Planning and Scheduling WS2015/2016

@section Project
Making tea at home

@section Content
@subsection planner Pyhop HTN Planner
pyhop.py (documentation not included in doxygen)
@subsection teaathome Making tea at home plan
teaathome.py
@subsection official Tests for official tasks
test1.py
test2.py
test3.py
@subsection additional Tests for official tasks with alternative environments
test1alt1.py
test1alt2.py
test1alt3.py
test2alt1.py
test2alt2.py
test2alt3.py
test3alt1.py
test3alt2.py
test3alt3.py
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
		print("****Robot is already at location " + location.name + " - so goto does nothing!****")
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
		print("****Cannot access object " + item + "****")
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

def maketea(state, robot, teabag, number):
	"""!@brief (Method) Main method (root of the tree) for making tea at home.
	@param state current state
	@param robot robot
	@param teabag teabag
	@param number How many teas you want to brew"""
	task = [('taskpreparehotwater', robot), ('taskgetcleancup', robot), ('taskfinalizetea', robot, teabag)]
	teas = 1
	while (teas < number):
		task = task + task
		teas = teas + 1
	return task


"""Prepare Kettle methods"""

def preparehotwater(state, robot):
	"""!@brief (Method) Preparation of kettle.
	@param state current state
	@param robot robot"""
	return [('tasplacekettleinsink', robot), ('taskfillkettle', robot), ('taskplacekettleonbase', robot), ('taskboilwater', robot)]

def preparehotwater_fullk(state, robot):
	"""!@brief (Method) Preparation of kettle.
	The kettle is already full and may be in the kitchensink or somewhere else.
	@param state current state
	@param robot robot"""
#if (state.itemstate['kettle']['fillstate'] == Itemstate.full):
	if (state.loc['kettle'] != Location.kettlebase):
		tasks = [('goto', robot, 'kettle'), ('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, 'kettlebase'), ('place', robot, 'kettle', 'kettlebase'), ('taskboilwater', robot)]
		return tasks 
	else:
		return [('goto', robot, 'kettlebase'), ('taskboilwater', robot)]
#else:
#print("Kettle is not full!")
#return False"""

def preparehotwater_fullhotk(state, robot):
	"""!@brief (Method) Preparation of kettle.
	The kettle is already filled with hot water.
	@param state current state
	@param robot robot"""
	#if (state.itemstate['kettle']['tempstate'] == Itemstate.hot):
	#if (state.itemstate['kettle']['fillstate'] == Itemstate.full):
	#print ("Kettle is allready full and hot - do nothing!")
	return []
	#else: 
	#print("Kettle is not full!")
	#return False
	#else:
	#print("Water in Kettle is not hot!")
	#return False

		
def checkkettlefill(state, robot):
	"""!@brief (Method) Check if the kettle has water in.
	This method is not mandatory, because you could alread know from the state object, that the kettle may be full or empty.
	Using this method is a bit more flexible in some cases.
	@param state current state
	@param robot robot"""
	return [('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('check', 'kettle', 'openstate', Itemstate.closed), ('grasp', robot, 'kettle'), ('weigh', robot, 'kettle', Itemstate.empty), ('place', robot, 'kettle', Location.kettlebase)]

def placekettleinsink(state, robot):
	"""!@brief (Method) Place kettle in the kitchen sink.
	@param state current state
	@param robot robot"""
	return [('goto', robot, state.loc['kettle']), ('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.kitchensink), ('place', robot, 'kettle', Location.kitchensink)]

def fillkettle(state, robot):
	"""!@brief (Method) Fill the kettle in the kitchen sink.
	Open the coldtap and the kettle and close them afterwards.
	@param state current state
	@param robot robot"""
	return [('openitem', robot, 'kettle'), ('opencoldtap', robot), ('close', robot, 'coldtap'), ('close', robot, 'kettle')]
	
def fillkettle_kopen(state, robot):
	"""!@brief (Method) Fill the kettle in the kitchen sink.
	Open the coldtap, but the kettle is already open. Close both afterwards.
	@param state current state
	@param robot robot"""
	#if(state.itemstate['kettle']['openstate'] == Itemstate.open):"""
	return [('opencoldtap', robot), ('close', robot, 'coldtap'), ('close', robot, 'kettle')]
	#else:
	#print("Kettle is not open!")
	#return False

def placekettleonbase(state, robot):
	"""!@brief (Method) Bring the kettle back to the kettlebase and place it.
	@param state current state
	@param robot robot"""
	return [ ('taskbringkettletobase', robot), ('place', robot, 'kettle', Location.kettlebase)]

def bringkettletobase(state, robot):
	"""!@brief (Method) Grasp kettle and go to kettlebase.
	@param state current state
	@param robot robot"""
	return [('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.kettlebase)]

def boilwater(state, robot):
	"""!@brief (Method) Go to the kettle and turn on kettlebase.
	Kettle has to be on the kettlebase otherwise it returns error.
	@param state current state
	@param robot robot"""
	return [ ('goto', robot, state.loc['kettle']), ('turnonkettlebase', robot, 'kettle')]


#prepare cup methods

def getcleancup(state, robot):
	"""!@brief (Method) Check if number of requested teas is greater than 0.
	@param state current state
	@param robot robot"""
	if state.TOTAL_NUMBER_OF_TEACUPS == 0:
		print("****No cups, no Tea!!!!!1111Elf****")
		return False
	else:
		return [('taskcheckcupdirty', robot)]

#damit plan failed, muessten -numcups- alternative methoden fuer check geschrieben werden

def checkcupdirty(state, robot):
	"""!@brief (Method) Detect if an before unknown teacup is dirty or clean.
	Always start at the beginning of the teacup array to search for clean teacups.
	@param state current state
	@param robot robot"""
	task = []
	teacup = ""
	for x in range(1, state.TOTAL_NUMBER_OF_TEACUPS + 1):
		teacup = 'teacup' + str(x)
		if (state.itemstate[teacup]['cleanstate']!=Itemstate.taken):
			teacuploc = state.loc[teacup]
			task = task + [('goto', robot, state.loc[teacup]), ('access', robot, teacup), ('grasp', robot, teacup)]
			state.itemstate[teacup]['cleanstate'] = getrandomcupstate(state, teacup)
			if (state.itemstate[teacup]['cleanstate'] == Itemstate.clean):
				print (teacup + " is clean!")
				task = task + [('taskplacecup', robot, teacup)]
				state.currentcup = teacup
				return task 
			print (teacup + " is dirty!")
			task = task + [('place', robot, teacup, teacuploc)]
			
	if (state.itemstate[teacup]['cleanstate'] == Itemstate.clean):
		state.currentcup = teacup
		return task
	else: 
		print("****I found only dirty cups, you have to clean some first!****")
		return False

def placecup(state, robot, teacup):
	"""!@brief (Method) Place a teacup on the countertop.
	This is implicitely defined as next to the kettlebase.
	@param state current state
	@param robot robot
	@param teacup teacup"""
	tasks = [('goto', robot, Location.countertop), ('place', robot, teacup, Location.countertop)]
	return tasks

#Brew tea

def finalizetea(state, robot, teabag):
	"""!@brief (Method) Place a teabag into the teacup and brew tea.
	The type of teabag is the same for all teas.
	@param state current state
	@param robot robot
	@param teabag teabag"""
	return[('taskprepareteabag', robot, teabag), ('taskbrewtea', robot, teabag)]

def prepareteabag(state, robot, teabag):
	"""!@brief (Method) Tak a teabag and place it into the teacup.
	@param state current state
	@param robot robot
	@param teabag teabag"""
	return [('taskgetteabag', robot, teabag), ('taskplacebagincup', robot, teabag) ]

def getteabag(state, robot, teabag):
	"""!@brief (Method) Grasp a teabag.
	Go to the location of the teabag and grasp it.
	@param state current state
	@param robot robot
	@param teabag teabag"""
	return [('goto', robot, state.loc['teabag']), ('access', robot, 'teabag'), ('grasp', robot, 'teabag')]

def placebagincup(state, robot, teabag):
	"""!@brief (Method) Place a teabag into the teacup.
	Go to the countertop and place the teabag into the teacup if it is also at this location.
	@param state current state
	@param robot robot
	@param teabag teabag"""
	if(state.currentcup == ""):
		return False
	state.itemstate[state.currentcup]['cleanstate'] = Itemstate.taken
	return[('goto', robot, Location.countertop), ('access', robot, state.currentcup), ('placein', robot, state.currentcup, teabag)]

def brewtea(state, robot, teabag):
	"""!@brief (Method) Final step for making tea.
	This part was missing in the definition of the exercise.
	Basically pouring water into the teacup with teabag with going to the correct locations, grasping, closing etc.
	@param state current state
	@param robot robot
	@param teabag teabag"""
	return[('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('openitem', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.countertop), ('pourintocup', robot, state.currentcup), ('goto', robot, Location.kettlebase), ('place', robot, 'kettle', Location.kettlebase), ('close', robot, 'kettle')]

def brewtea_kopen(state, robot, teabag):
	"""!@brief (Method) Final step for making tea.
	This part was missing in the definition of the exercise.
	Basically pouring water into the teacup with teabag with going to the correct locations, grasping, closing etc.
	The kettle is already open.
	@param state current state
	@param robot robot
	@param teabag teabag"""
	#if(state.itemstate['kettle']['openstate'] == Itemstate.open):"""
	return[('goto', robot, Location.kettlebase), ('access', robot, 'kettle'), ('grasp', robot, 'kettle'), ('goto', robot, Location.countertop), ('pourintocup', robot, state.currentcup), ('goto', robot, Location.kettlebase), ('place', robot, 'kettle', Location.kettlebase), ('close', robot, 'kettle')]
	#else:
	#print("Kettle is not open!")
	#return False"""
	
def setupTeaAtHome():
	'''!@brief Setup tea at home.
	This method declares operators, tasks and methods to pyhop. This must be called BEFORE running pyhop with teaathome.
	'''
	pyhop.declare_operators(goto, openitem, grasp, place, close, check, weigh, placein, turnonkettlebase, access, opencoldtap, pourintocup)
	pyhop.declare_methods('taskmaketea', maketea)
	pyhop.declare_methods('taskpreparehotwater', preparehotwater_fullhotk, preparehotwater_fullk, preparehotwater)
	pyhop.declare_methods('taskcheckkettlefill', checkkettlefill)
	pyhop.declare_methods('tasplacekettleinsink', placekettleinsink)
	pyhop.declare_methods('taskfillkettle', fillkettle_kopen, fillkettle)
	pyhop.declare_methods('taskplacekettleonbase', placekettleonbase)
	pyhop.declare_methods('taskbringkettletobase', bringkettletobase)
	pyhop.declare_methods('taskboilwater', boilwater)
	pyhop.declare_methods('taskgetcleancup', getcleancup)
	pyhop.declare_methods('taskcheckcupdirty', checkcupdirty)
	pyhop.declare_methods('taskplacecup', placecup)
	pyhop.declare_methods('taskfinalizetea', finalizetea)
	pyhop.declare_methods('taskprepareteabag', prepareteabag)
	pyhop.declare_methods('taskgetteabag', getteabag)
	pyhop.declare_methods('taskplacebagincup', placebagincup)
	pyhop.declare_methods('taskbrewtea', brewtea_kopen, brewtea)

def setupRobotArm(state):
	'''!@brief Setup RobotArm enum.
	Dynamically create the RobotArm enum with all teacups#, where # are all numbers between 1 and state.TOTAL_NUMBER_OF_TEACUPS.
	@param state The state which is created for in a test case.
	@returns state The state which is then passed to pyhop.
	'''
	global RobotArm
	teacups = []
	teacups = ['free'] + ['kettle'] + ['teabag'] +  teacups
	for x in range(1, state.TOTAL_NUMBER_OF_TEACUPS + 1):
		teacups = teacups + ['teacup' + str(x)]
	teacups = [m.name for m in Enum] +  teacups
	RobotArm = Enum('RobotArm', teacups)
	state.robotarm = {'robot':RobotArm.free}
	return state

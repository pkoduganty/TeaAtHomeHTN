TeaAtHomeHTN
============

### Introduction
HTN planner "Pyhop" with a simple example "making tea at home" for the planning and scheduling course. Developed in Python version 2.7.


### Dependencies
Python 3.4 enum backport

https://pypi.python.org/pypi/enum34

There are several other enum libraries for python, make sure you have this one above!

In most cases, we use enumerations instead of strings to make it more robust against errors, especially against typos.

### Running TeaAtHome
From Python console, navigate to the directory of your local copy of the repository 

	import os
	os.chdir('/path/to/repository/on/your/pc')

and run the test cases:

    execfile('test1.py')
	execfile('test2.py')
	execfile('test3.py')

The log files are saved to the "logs" directory within your local repository.

---

### Pyhop, version 1.2.2

A simple HTN planning system written in Python

Copyright 2013 Dana S. Nau - <http://www.cs.umd.edu/~nau>

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

----

Pyhop is a simple HTN planner written in Python. 
It works in both Python 2.7 and 3.2. 

Pyhop was easy to implement (less than 150 lines of code), and if you understand the basic ideas of HTN planning ([this presentation](http://www.cs.umd.edu/~nau/papers/nau2013game.pdf) contains a quick summary),
Pyhop should be easy to understand.

Pyhop's planning algorithm is like the one in [SHOP](http://www.cs.umd.edu/projects/shop/), but with several differences that should make it easier to integrate it with ordinary computer programs:

  - Pyhop represents states of the world using ordinary variable bindings, not logical propositions. A state is just a Python object that contains the variable bindings.  For example, you might write s.loc['v'] = 'd' to say that vehicle v is at location d in state s.
  
  - To write HTN operators and methods for Pyhop, you don't need to learn a specialized planning language. Instead, you write them as ordinary Python functions. The current state (e.g., s in the above example) is passed to them as an argument.



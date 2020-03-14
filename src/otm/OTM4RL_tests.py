import os
import inspect
import numpy as np
from OTM4RL import OTM4RL

def get_config():
	this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	root_folder = os.path.dirname(os.path.dirname(this_folder))
	configfile = os.path.join(root_folder,'cfg', 'network_v6.xml')
	return configfile

def get_otm4rl():
	return OTM4RL(get_config())

# GET STATIC -----------------------------------------

# done
def test_get_link_ids():
	otm4rl = get_otm4rl()
	print(otm4rl.get_link_ids())
	del otm4rl

# done
def test_get_max_queues():
	otm4rl = get_otm4rl()
	print(otm4rl.get_max_queues())
	del otm4rl

# done
def test_get_signals():

	otm4rl = get_otm4rl()
	X = otm4rl.get_signals()

	print('node_id',X[2]['node_id'])
	for phaseid,phase in X[2]['phases'].items():
		print(phaseid,'road_conns',phase['road_conns'])
		print(phaseid,'yellow_time',phase['yellow_time'])
		print(phaseid,'red_clear_time',phase['red_clear_time'])
		print(phaseid,'min_green_time',phase['min_green_time'])

	del otm4rl

# not done
def test_get_controller_infos():
	otm4rl = get_otm4rl()
	X = otm4rl.get_controller_infos()

	print('cycle',X[2]['cycle'])
	print('offset',X[2]['offset'])
	for i,stage in enumerate(X[2]['stages']):
		print(i,'duration',stage['duration'])
		print(i,'phases',stage['phases'])

	del otm4rl

# GET STATE AND ACTION -----------------------------------------

# done
def test_get_queues():
	otm4rl = get_otm4rl()
	otm4rl.otmwrapper.run_simple(start_time=0,duration=3600,output_dt=10)
	queues = otm4rl.get_queues()
	print(queues)
	del otm4rl

# not done
def test_get_control():

	otm4rl = get_otm4rl()
	otm4rl.otmwrapper.initialize(float(0))
	otm4rl.otmwrapper.otm.advance(float(60))

	# action[controller_id] = active stage id
	control = otm4rl.get_control()

	print(control)

	del otm4rl

# SET STATE AND ACTION -----------------------------------------

# done
def test_set_queues():
	otm4rl = get_otm4rl()

	myqueues = {
	1: {"waiting": 3, "transit": 5},
	2: {"waiting": 5, "transit": 3}
	}

	otm4rl.otmwrapper.run_simple(start_time=0,duration=3000,output_dt=10)

	print( otm4rl.get_queues() )

	otm4rl.set_queues(myqueues)

	print( otm4rl.get_queues() )

	# always end by deleting the wrapper
	del otm4rl

# not done
def test_set_control():

	otm4rl = get_otm4rl()
	otm4rl.otmwrapper.initialize(float(0))
	otm4rl.otmwrapper.otm.advance(float(70))

	# action[controller_id] = active stage id

	print(otm4rl.get_control())

	otm4rl.set_control({1:1,2:0,3:1})
	# this line below hangs
	otm4rl.otmwrapper.otm.advance(float(100))

	print(otm4rl.get_control())

	del otm4rl

# RUN -----------------------------------------

def test_run_simulation():
	otm4rl = get_otm4rl()
	return otm4rl.run_simulation(600,600)


if __name__ == '__main__':
	# test_get_link_ids()
	# test_get_max_queues()
	# test_get_signals()
	# test_get_controller_infos() # not done
	# test_get_queues()
	# test_get_control() # not done
	# test_set_queues()
	test_set_control() # not done
	# test_run_simulation()

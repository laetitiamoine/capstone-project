import os
import inspect
import numpy as np
from OTM4RL import OTM4RL

def get_config():
	this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	root_folder = os.path.dirname(os.path.dirname(this_folder))
	configfile = os.path.join(root_folder,'cfg', 'network_v3.xml')
	return configfile

def get_otm4rl():
	return OTM4RL(get_config())

# done
def test_run_simulation():
	otm4rl = get_otm4rl()
	return otm4rl.run_simulation(600)

# done
def test_get_link_ids():
	otm4rl = get_otm4rl()
	print(otm4rl.get_link_ids())

# done
def test_get_queues():
	otm4rl = get_otm4rl()

	otm4rl.otmwrapper.run_simple(start_time=0,duration=3600,output_dt=10)

	queues = otm4rl.get_queues()
	print(queues)

	# always end by deleting the wrapper
	del otm4rl

# done
def test_get_max_queues():
	otm4rl = get_otm4rl()
	print(otm4rl.get_max_queues())
	del otm4rl

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

# done
def test_get_signal_controller_info():
	otm4rl = get_otm4rl()
	print(otm4rl.get_signal_controller_info())
	del otm4rl

# not done
def test_set_signals():


	# my_signals[controller_id] = green stage id
	my_signals = {}

	otm4rl = get_otm4rl()


	signal_info = otm4rl.get_signal_controller_info()




	advance_time = 60.

	otm4rl.otmwrapper.initialize(float(0))

	otm4rl.otmwrapper.otm.advance(advance_time)

	# print stage order ids currently green

	# create a signal command
	this_signal = signal_info[0]
	signal_command['id'] = this_signal['id']
	signal_command['green_stage_order'] = this_signal['stages'][0]['order']

	otm4rl.set_signal(signal_command)

	# print stage order ids currently green

	del otm4rl

if __name__ == '__main__':
	print(test_get_signal_controller_info())

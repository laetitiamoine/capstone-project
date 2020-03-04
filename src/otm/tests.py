import os
import inspect
import numpy as np
from OTM4RL import OTM4RL

def get_config():
	this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	root_folder = os.path.dirname(os.path.dirname(this_folder))
	configfile = os.path.join(root_folder,'cfg', 'network_v4.xml')
	return configfile

def get_otm4rl():
	return OTM4RL(get_config())

# done
def test_run_simulation():
	otm4rl = get_otm4rl()
	otm4rl.run_simulation(600,60)

# done
def test_get_link_ids():
	otm4rl = get_otm4rl()
	print(otm4rl.get_link_ids())

# done
def test_get_queues():
	otm4rl = get_otm4rl()

	advance_time = 60.
	duration = 120.
	time = 0.

	link_ids = otm4rl.get_link_ids()
	otm4rl.otmwrapper.otm.output().request_link_queues(link_ids,advance_time)
	otm4rl.otmwrapper.initialize(float(0))

	while(time<duration):
		otm4rl.otmwrapper.otm.advance(advance_time)
		queues = otm4rl.get_queues()
		time += advance_time;

	# always end by deleting the wrapper
	del otm4rl

# done
def test_get_max_queues():
	otm4rl = get_otm4rl()
	del otm4rl

# done
def test_set_queues():
	otm4rl = get_otm4rl()

	# create random map
	max_queues = otm4rl.get_max_queues()
	myqueues = { link_id:{'waiting':0,'transit':0} for link_id in otm4rl.get_link_ids()}
	for link_id in myqueues.keys():
		total_queue = np.random.random()*max_queues[link_id]
		p = np.random.random()
		myqueues[link_id]['waiting'] = round(p*total_queue)
		myqueues[link_id]['transit'] = round((1-p)*total_queue)

	advance_time = 60.

	otm4rl.otmwrapper.initialize(float(0))

	otm4rl.otmwrapper.otm.advance(advance_time)

	print("Before: ", otm4rl.get_queues()[26]['transit'])
	print("Desired: ",myqueues[26]['transit'])

	otm4rl.set_queues(myqueues)

	print("After: ",otm4rl.get_queues()[26]['transit'])

	# always end by deleting the wrapper
	del otm4rl

# RETURNS EMPTY
def test_get_controller_info():
	otm4rl = get_otm4rl()
	X = otm4rl.get_controller_info()


	print('cycle',X[2]['cycle'])
	print('offset',X[2]['offset'])
	for i,stage in enumerate(X[2]['stages']):
		print(i,'duration',stage['duration'])
		print(i,'phases',stage['phases'])

	del otm4rl

# TO DO
def test_get_signals():
	pass

# FAILS
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
	print(test_get_controller_info())

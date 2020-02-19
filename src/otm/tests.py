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

def test_run_simulation():
	otm4rl = get_otm4rl()
	otm4rl.run_simulation(600,60)

def test_get_link_ids():
	otm4rl = get_otm4rl()
	print(otm4rl.get_link_ids())

def test_get_queues():
	otm4rl = get_otm4rl()

	advance_time = 60.
	duration = 120.
	time = 0.

	otm4rl.otmwrapper.output().request_links_veh(link_ids,advance_time)
	otm4rl.otmwrapper.initialize(float(0))

	while(time<duration):
		otm4rl.otmwrapper.otm.advance(advance_time)
		queues = otm4rl.get_queues()
		print(queues)
		time += advance_time;

	# always end by deleting the wrapper
	del otm4rl

def test_set_signals():

	my_signals = {}
	# for each controller id
		# my_signals[controller_id] = np.random.choice(set of stage order ids)

	otm4rl = get_otm4rl()

	advance_time = 60.

	otm4rl.otmwrapper.initialize(float(0))

	otm4rl.otmwrapper.otm.advance(advance_time)

	# print stage order ids currently green

	otm4rl.set_signals(my_signals)

	# print stage order ids currently green

	del otm4rl

def test_get_max_queues():
	otm4rl = get_otm4rl()
	print(otm4rl.get_max_queues())
    del otm4rl

def test_reset_queues():
	otm4rl = get_otm4rl()

	# create random map
	myqueues = otm4rl.get_max_queues()
	for link_id in myqueues.keys():
		myqueues[link_id] = np.random.random(0,myqueues[link_id])

	advance_time = 60.

	otm4rl.otmwrapper.initialize(float(0))

	otm4rl.otmwrapper.otm.advance(advance_time)

	print( otm4rl.get_queues() )

	otm4rl.set_queues(myqueues)

	print( otm4rl.get_queues() )

	# always end by deleting the wrapper
	del otm4rl

def test_get_num_intersections():
	otm4rl = get_otm4rl()
	print(otm4rl.get_num_intersections())
    del otm4rl

if __name__ == '__main__':
	print(test_get_queue_for_link_id())

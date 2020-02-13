import os
import inspect
from OTM4RL import OTM4RL


def get_config():
	this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	root_folder = os.path.dirname(os.path.dirname(this_folder))
	configfile = os.path.join(root_folder,'cfg', 'network_v3.xml')
	return configfile

def get_otm4rl():
	return OTM4RL(get_config())

def test_run_simulation():
	otm4rl = OTM4RL(get_config())
	otm4rl.run_simulation(3600.0,60.0)


def test_get_queue_for_link_id():
	otm4rl = get_otm4rl()

	advance_time = 60.
	duration = 600.
	time = 0.

	otm4rl.otmwrapper.output().request_links_veh(link_ids,advance_time)
	otm4rl.otmwrapper.initialize(float(0))

	while(time<duration):
		otm4rl.otmwrapper.otm.advance(advance_time)
		queues = otm4rl.get_queues()
		time += advance_time;

	# always end by deleting the wrapper
	del otm

def test_set_signals():
	pass


def test_reset_queues():
	otm4rl = get_otm4rl()

	link_ids = otm4rl.get_link_ids()

	# create random map
	myqueues = {}
	for link_id in link_ids:
		myqueues[link_id] = random number...

	advance_time = 60.
	duration = 600.
	time = 0.

	otm4rl.otmwrapper.initialize(float(0))

	otm4rl.otmwrapper.otm.advance(advance_time)

	print( otm4rl.get_queues() )

	otm4rl.set_queues(myqueues)

	print( otm4rl.get_queues() ) 

	# always end by deleting the wrapper
	del otm


def test_get_link_ids():
	otm4rl = get_otm4rl()
	print(otm4rl.get_link_ids())

if __name__ == '__main__':
	print(test_get_queue_for_link_id())
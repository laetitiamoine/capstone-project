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

# done
def test_get_controllers():
	otm4rl = get_otm4rl()
	X = otm4rl.get_controller_infos()

	print('cycle',X[2]['cycle'])
	print('offset',X[2]['offset'])
	for i,stage in enumerate(X[2]['stages']):
		print(i,'duration',stage['duration'])
		print(i,'phases',stage['phases'])

	del otm4rl

# done
def test_get_signals():

	otm4rl = get_otm4rl()
	X = otm4rl.get_signals()
	
	print('node_id',X[2]['node_id'])
	for phaseid,phase in X[2]['phases'].items():
		print(phaseid,'rcs',phase['rcs'])
		print(phaseid,'y',phase['y'])
		print(phaseid,'r',phase['r'])
		print(phaseid,'ming',phase['ming'])

	del otm4rl

# done
def test_set_control():

	otm4rl = get_otm4rl()
	otm4rl.otmwrapper.initialize(float(0))
	otm4rl.otmwrapper.otm.advance(float(60))

	# action[controller_id] = active stage id
	otm4rl.set_control({1:1,2:3,3:3})
	otm4rl.otmwrapper.otm.advance(float(300))

	# print stage order ids currently green

	del otm4rl

# done
def test_get_control():

	otm4rl = get_otm4rl()
	otm4rl.otmwrapper.initialize(float(0))
	otm4rl.otmwrapper.otm.advance(float(60))

	# action[controller_id] = active stage id
	control = otm4rl.get_control()

	print(control)


	otm4rl.set_control({1:1,2:3,3:3})
	otm4rl.otmwrapper.otm.advance(float(10))

	print(control)


	del otm4rl

if __name__ == '__main__':
	print(test_get_control())

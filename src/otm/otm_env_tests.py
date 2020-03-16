import os
import inspect
import numpy as np
from otm_env import otmEnvDiscrete

def get_config():
	this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	root_folder = os.path.dirname(os.path.dirname(this_folder))
	configfile = os.path.join(root_folder,'cfg', 'network_v6.xml')
	return configfile

def get_env():
    return otmEnvDiscrete({"num_states": 2, "num_actions": 2, "time_step": 200}, get_config())

def test_decode_action():
    env = get_env()
    for i in range(8):
    	print(env.decode_action(i))
    del env

def test_encode_state():
    env = get_env()
    env.otm4rl.run_simulation(600)
    state = env.otm4rl.get_queues()
    print(env.encode_state(state))
    del env

def test_set_state():
	env = get_env()
	state = env.otm4rl.get_max_queues()
	for link_id in state.keys():
		p = np.random.random()
		state[link_id] = {"waiting": round(p*state[link_id]), "transit": round((1-p)*state[link_id])}
	env.set_state(state)
	print(state)
	print(env.state)
	print(env.otm4rl.get_queues())
	del env

def test_reset():
	env = get_env()
	print(env.reset())
	del env

def test_step():
	env = get_env()

	env.reset()
	print("Initial state:", env.encode_state(env.otm4rl.get_queues()))
	print(env.otm4rl.get_queues())

	action = np.random.choice(env.action_space)
	print("Action 1: ", env.decode_action(action))
	state, reward = env.step(action)
	print("Next state:", env.encode_state(env.otm4rl.get_queues()))
	print("Reward:", reward)
	print(env.otm4rl.get_queues())

	action = np.random.choice(env.action_space)
	print("Action 1: ", env.decode_action(action))
	state, reward = env.step(action)
	print("Next state:", env.encode_state(env.otm4rl.get_queues()))
	print("Reward:", reward)
	print(env.otm4rl.get_queues())

	del env

def test_plot_environment():
	env = get_env()
	env.otm4rl.initialize()
	env.plot_environment().show()
	env.otm4rl.advance(env.time_step)
	env.plot_environment().show()
	env.otm4rl.advance(env.time_step)
	env.plot_environment().show()
	env.otm4rl.advance(env.time_step)
	env.plot_environment().show()

if __name__ == '__main__':
	test_plot_environment()

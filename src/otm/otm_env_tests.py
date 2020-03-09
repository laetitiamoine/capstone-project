import os
import inspect
from otm_env import otmEnvDiscrete

def get_config():
	this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	root_folder = os.path.dirname(os.path.dirname(this_folder))
	configfile = os.path.join(root_folder,'cfg', 'network_v3.xml')
	return configfile

def get_env():
    return otmEnvDiscrete({"num_states": 2, "num_actions": 2}, get_config())

def test_decode_action():
    env = get_env()
    for i in range(8):
        print(env.decode_action(i))

def test_encode_state():
    env = get_env()
    env.otm4rl.run_simulation(600)
    state = env.otm4rl.get_queues()
    print(env.encode_state(state))

if __name__ == '__main__':
	print(test_decode_action())

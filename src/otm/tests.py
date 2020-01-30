from OTM4RL import OTM4RL


def test_create_otm4rl():
	configfile = '/home/gomes/Dropbox/gabriel/work/MEng/2019-2020/_supervised/traffic/capstone-project/cfg/network_v3.xml'
	otm4rl = OTM4RL(configfile)
	print(otm4rl)

def test_run_simulation():
	otm4rl = OTM4RL('/home/gomes/Dropbox/gabriel/work/MEng/2019-2020/_supervised/traffic/capstone-project/cfg/network_v3.xml')
	otm4rl.run_simulation(3600.0,60.0)
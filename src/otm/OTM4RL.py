from OTMWrapper import OTMWrapper
import gym
from gym import spaces
from gym.utils import seeding

class OTM4RL:

    def __init__(self, configfile, jaxb_only=False):
        self.otmwrapper = OTMWrapper(configfile)

    def run_simulation(self,duration,output_dt):
    	self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=output_dt)
        self.Y = self.otmwrapper.get_state_trajectory()

    def env_dynamics(self, state, action):
        # Return next state and reward
        pass

class otmEnvDiscrete:

    def __init__(self, env_info, configfile):

        self.action_space = spaces.Discrete(env_info.num_actions)
        self.observation_space = spaces.Discrete(env_info.num_states)
        self.otm = OTM4RL(configfile)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self, network_config):
        self.state = self.np_random.choice(env_info.num_states)
        return self.state

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        state, reward = self.otm.env_dynamics(self.state, action)
        self.state = state

        return self.state, reward

    def render(self, mode='human'):
        #plot the queue profile over time
        #render the network
        pass

    def close(self):
        #stop rendering
        pass

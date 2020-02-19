from OTMWrapper import OTMWrapper
import os
import inspect
# import gym
# from gym import spaces
# from gym.utils import seeding

class OTM4RL:

    def __init__(self, configfile, jaxb_only=False):
        this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        root_folder = os.path.dirname(os.path.dirname(this_folder))
        cfg = os.path.join(root_folder,'cfg', configfile)
        self.otmwrapper = OTMWrapper(cfg)

    def get_link_ids(self):
        return self.otmwrapper.otm.scenario().get_link_ids()

    def get_queues(self):
        otm = self.otmwrapper.otm
        queues = {}
        for data in otm.output().get_data():
            if "output.LinkVehicles" in data.toString():
                for link_id in self.get_link_ids():
                    queues[link_id] = data.get_value_for_link(link_id)
        return queues

    def get_max_queues(self):
        pass

    def reset_queues(queue_dictionary):
        pass

    def set_signals(signal_dictionary):
        pass

    def run_simulation(self,duration,output_dt):
        self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=output_dt)
        self.Y = self.otmwrapper.get_state_trajectory()

class otmEnvDiscrete:

    def __init__(self, env_info, configfile):

        self.env_info = env_info
        # self.action_space = spaces.Discrete(env_info.num_actions)
        # self.observation_space = spaces.Discrete(env_info.num_states)
        self.otm4rl = OTM4RL(configfile)
        # self.seed()

    # def seed(self, seed=None):
    #     self.np_random, seed = seeding.np_random(seed)
    #     return [seed]

    def encode_state():
        pass

    def set_state(self, state):
        self.otm4rl.reset_queues(state)
        self.state = self.encode_state(state)

     def reset(self):
         state = self.otm4rl.get_max_queues()
         for link_id in state.keys():
             state[link_id] = np.random.random(0,state[link_id])
         self.set_state(state)
         return self.state

    # def step(self, action):
    #     assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
    #
    #     state, reward = self.otm.env_dynamics(self.state, action)
    #     self.state = state
    #
    #     return self.state, reward
    #
    # def render(self, mode='human'):
    #     #plot the queue profile over time
    #     #render the network
    #     pass
    #
    # def close(self):
    #     #stop rendering
    #     pass

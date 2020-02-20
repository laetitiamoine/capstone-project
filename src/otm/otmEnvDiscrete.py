class otmEnvDiscrete:

    def __init__(self, env_info, configfile):

        self.otm4rl = OTM4RL(configfile)
        self.env_info = env_info
        self.num_intersections = self.otm4rl.get_num_intersections()
        self.action_space = range(env_info.num_actions ** self.num_intersections)
        self.observation_space = range(env_info.num_states ** (self.num_intersections * 2))
        # self.seed()

    # def seed(self, seed=None):
    #     self.np_random, seed = seeding.np_random(seed)
    #     return [seed]

    def encode_state(state):
        pass

    def decode_action(action):
        pass

    def compute_reward(state):
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

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        self.otm4rl.set_signals(self.decode_action(action))

        self.otm4rl.run_simulation(time_step, time_step)

        next_state = self.otm4rl.get_queues()

        self.state = self.encode_state(next_state)
        reward = self.compute_reward(self.state)

        return self.state, reward
    #
    # def render(self, mode='human'):
    #     #plot the queue profile over time
    #     #render the network
    #     pass
    #
    # def close(self):
    #     #stop rendering
    #     pass

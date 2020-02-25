class otmEnvDiscrete:

    def __init__(self, env_info, configfile):

        self.otm4rl = OTM4RL(configfile)
        self.num_states = env_info.num_states
        self.controllers = self.otm4rl.get_signal_controller_info()
        self.num_intersections = len(self.controllers)
        self.action_space = range(env_info.num_actions ** self.num_intersections)
        self.state_space = range(env_info.num_states ** (self.num_intersections * 2))
        self.max_queues = self.otm4rl.get_max_queues()
        # self.seed()

    # def seed(self, seed=None):
    #     self.np_random, seed = seeding.np_random(seed)
    #     return [seed]

    def encode_state(state):
        encoded_state = 0
        state_vec = []
        i = 0
        for controller in self.controllers:
            stages = controller["stages"]
            for stage in stages:
                in_link_ids = []
                agg_queue = 0
                max_queue = 0
                phase_ids = stage["phase_ids"]
                for phase_id in phase_ids:
                    road_connections = self.otm4rl.get_roadconnection_info(phase_id)
                    for road_connection in road_connections:
                        in_link_ids.append(road_connection["in_link"])
                in_link_ids = list(set(in_link_ids))
                for link_id in in_link_ids:
                    agg_queue += state[link_id]
                    max_queue += self.max_queues[link_id]
                encoded_stage_state = math.floor(agg_queue * self.num_states / max_queue))
                state_vec.append(encoded_stage_state)
                encoded_state += encoded_stage_state * (self.num_states ** i)
                i += 1
        return encoded_state, state_vec

    def decode_action(action):
        a = action
        action_vec = []
        while a != 0:
            action_vec.append(a % self.num_actions)
            a = a // self.num_actions
        action_vec.reverse()

        decoded_action = []
        i = 0
        for controller in self.controllers:
            signal_command = {"controller_id": controller["id"],
                              "green_stage_order": controller["stages"][decoded_action[i]]["order_id"]}
            decoded_action.append(signal_command)
            i += 1

        return decoded_action

    def set_state(self, state):
        self.otm4rl.reset_queues(state)
        self.state = self.encode_state(state)

    def reset(self):
         state = self.max_queues.copy()
         for link_id in state.keys():
             state[link_id] = np.random.random(0,state[link_id])
         self.set_state(state)
         return self.state

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        self.otm4rl.set_signals(self.decode_action(action))

        self.otm4rl.run_simulation(time_step)

        next_state = self.otm4rl.get_queues()

        self.state, state_vec = self.encode_state(next_state)
        reward = -state_vec.sum()

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

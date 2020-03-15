import numpy as np
from OTM4RL import OTM4RL

class otmEnvDiscrete:

    def __init__(self, env_info, configfile):

        self.otm4rl = OTM4RL(configfile)
        self.num_states = env_info["num_states"]
        self.num_actions = env_info["num_actions"]
        self.controllers = self.otm4rl.get_controller_infos()
        self.num_intersections = len(self.controllers)
        self.action_space = range(self.num_actions ** self.num_intersections)
        self.state_space = range(self.num_states ** (self.num_intersections * 2))
        self.max_queues = self.otm4rl.get_max_queues()
        self.time_step = env_info["time_step"]
        # self.seed()

    # def seed(self, seed=None):
    #     self.np_random, seed = seeding.np_random(seed)
    #     return [seed]

    def encode_state(self, state):
        encoded_state = 0
        state_vec = []
        i = 0
        for c_id, controller in self.controllers.items():
            stages = controller["stages"]
            for stage in stages:
                in_link_ids = []
                agg_queue = 0
                max_queue = 0
                phase_ids = stage["phases"]
                for phase_id in phase_ids:
                    road_connections = self.otm4rl.get_signals()[c_id]["phases"][phase_id]["road_conns"]
                    for road_connection in road_connections:
                        in_link_ids.append(self.otm4rl.get_road_connection_info(road_connection)["in_link"])
                in_link_ids = list(set(in_link_ids))
                for link_id in in_link_ids:
                    agg_queue += state[link_id]["waiting"]
                    max_queue += self.max_queues[link_id]
                encoded_stage_state = int(agg_queue * self.num_states / max_queue) if agg_queue != max_queue else self.num_states - 1
                state_vec.append(encoded_stage_state)
                encoded_state += encoded_stage_state * (self.num_states ** i)
                i += 1
        state_vec.reverse()
        return encoded_state, np.array(state_vec)

    def decode_action(self, action):
        a = action
        signal_command = dict(list(zip(self.controllers.keys(), np.zeros(self.num_intersections).astype(int))))
        i = self.num_intersections - 1
        while a != 0:
            controller_id = list(self.controllers.keys())[i]
            signal_command[controller_id] = a % self.num_actions
            a = a // self.num_actions
            i -= 1

        return signal_command

    def set_state(self, state):
        self.otm4rl.set_queues(state)
        self.state = self.encode_state(state)

    def reset(self):
         state = self.otm4rl.get_max_queues()
         for link_id in state.keys():
            p = np.random.random()
            transit_queue = p*state[link_id]
            q = np.random.random()
            waiting_queue = q*(state[link_id] - transit_queue)
            state[link_id] = {"waiting": round(waiting_queue), "transit": round(transit_queue)}
         self.otm4rl.run_simulation(10)
         self.set_state(state)
         return self.state

    def step(self, action):
        assert action in self.action_space, "%r (%s) invalid" % (action, type(action))

        self.otm4rl.set_control(self.decode_action(action))

        self.otm4rl.run_simulation(self.time_step)

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

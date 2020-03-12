from OTMWrapper import OTMWrapper
import os
import inspect

class OTM4RL:

    def __init__(self, configfile, jaxb_only=False):
        this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        root_folder = os.path.dirname(os.path.dirname(this_folder))
        cfg = os.path.join(root_folder,'cfg', configfile)
        self.otmwrapper = OTMWrapper(cfg)

    # GET STATIC -----------------------------------------

    def get_link_ids(self):
        return self.otmwrapper.otm.scenario().get_link_ids()

    def get_max_queues(self):
        max_queues = {}
        for link_id in self.otmwrapper.otm.scenario().get_link_ids():
            link = self.otmwrapper.otm.scenario().get_link_with_id(link_id)
            max_queues[link_id] = link.get_jam_density_vpkpl() * link.getFull_length() * link.getFull_lanes() / 1000
        return max_queues

    # returns map from signal id to to a signal object (a dict)
    # psig['node_id']
    # psig['phases'] a map from pphase id to phase object (a dict)
    #       x['rcs'] ... a set of road connection ids
    #       x['y'] ... yellow_time
    #       x['r'] ... red_clear_time
    #       x['ming'] ... min_green_time
    def get_signals(self):
        X = {}
        for oact in self.otmwrapper.otm.scenario().get_actuators():
            if str(oact.getType())=='signal':
                psig = {}
                psig['node_id'] = oact.getTarget_id()
                psig['phases'] = {}
                for phase in oact.get_phases():
                    x = {}
                    x['road_conns'] = phase.getRoad_connections()
                    x['yellow_time'] = phase.getYellow_time()
                    x['red_clear_time'] = phase.getRed_clear_time()
                    x['min_green_time'] = phase.getMin_green_time()
                    psig['phases'][phase.getId()] = x
                X[oact.getId()] = psig

        return X

    # returns map from controller id to a controller object (a dict)
    # X['cycle']
    # X['offset']
    # X['stages'] an ordered list of stage dicts:
    #   x['duration']
    #   x['phases']
    def get_controller_infos(self):
        X = {} # id to controller
        for ocntrl in self.otmwrapper.otm.scenario().get_controller_infos():
            if str(ocntrl.getType())=='sig_pretimed':

                cntrl = {}
                cntrl['cycle'] = ocntrl.getCycle()
                cntrl['offset'] = ocntrl.getOffset()

                stages = []
                for ostage in ocntrl.getStages():
                    stage = {}
                    stage['duration'] = ostage.getDuration()
                    stage['phases'] = ostage.getPhases()
                    stages.append(stage)

                cntrl['stages'] = stages
                X[ocntrl.getId()] = cntrl

        return X

    # def get_signal_controller_info(self):
    #     X = [{"controller_id": 1,
    #           "stages": [{"order_id": 1,
    #                       "phase_ids": [1, 6]},
    #                      {"order_id": 2,
    #                       "phase_ids": [7]},
    #                      {"order_id": 3,
    #                       "phase_ids": [12]},
    #                      {"order_id": 4,
    #                       "phase_ids": [13, 14]}]},
    #          {"controller_id": 2,
    #           "stages": [{"order_id": 1,
    #                       "phase_ids": [2, 5]},
    #                      {"order_id": 2,
    #                       "phase_ids": [8]},
    #                      {"order_id": 3,
    #                       "phase_ids": [11]},
    #                      {"order_id": 4,
    #                       "phase_ids": [15, 16]}]},
    #          {"controller_id": 3,
    #           "stages": [{"order_id": 1,
    #                       "phase_ids": [3, 4]},
    #                      {"order_id": 2,
    #                       "phase_ids": [9]},
    #                      {"order_id": 3,
    #                       "phase_ids": [10]},
    #                      {"order_id": 4,
    #                       "phase_ids": [17, 18]}]}
    #         ]

    #     # list of dictionary
    #     # for controller in self.otmwrapper.otm.scenario().get_controllers():
    #     #     if str(controller.getType())=='sig_pretimed':
    #     #         print(controller)
    #     #         print(controller.getPretimed_signal_info())
    #     #         schedule = controller.getPretimed_signal_info().getSchedule()
    #     #         stagelist = schedule[0].getStages()
    #     #         # cntrl = {}
    #     #         # cntrl['id'] = int(controller.getId())
    #     #         # cntrl['stages'] = []

    #     return X

    # GET STATE AND ACTION -----------------------------------------

    def get_queues(self):
        otm = self.otmwrapper.otm
        queues = {}
        for link_id in self.get_link_ids():
            X = self.otmwrapper.otm.scenario().get_link_queues(link_id)
            queues[link_id] = {'waiting':X.waiting(),'transit':X.transit()}
        return queues

    # returns a dictionary from controller id to stage index
    def get_control(self):
        X = {}
        for ctrl_id in self.otmwrapper.otm.scenario().get_controller_ids():
            cntrl = self.otmwrapper.otm.scenario().get_actual_controller_with_id(ctrl_id)
            X[ctrl_id] = cntrl.get_stage_index()
        return X

    # SET STATE AND ACTION -----------------------------------------

    def set_queues(self,queue_dictionary):
        for link_id, q4link in queue_dictionary.items():
            self.otmwrapper.otm.scenario().set_link_vehicles(link_id,int(q4link['waiting']),int(q4link['transit']))

    # action is a dictionary from controller id to stage index
    def set_control(self,action):
        for ctrl_id, stage_index in action.items():
            cntrl = self.otmwrapper.otm.scenario().get_actual_controller_with_id(ctrl_id)
            cntrl.set_stage_index(stage_index)

    # RUN -----------------------------------------

    def run_simulation(self,duration,output_dt):
        self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=output_dt)

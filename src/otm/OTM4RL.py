from OTMWrapper import OTMWrapper
import os
import inspect

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
        for link_id in self.get_link_ids():
            X = self.otmwrapper.otm.scenario().get_link_queues(link_id)
            queues[link_id] = {'waiting':X.waiting(),'transit':X.transit()}
        return queues

    def get_max_queues(self):
        max_queues = {}
        for link_id in self.otmwrapper.otm.scenario().get_link_ids():
            link = self.otmwrapper.otm.scenario().get_link_with_id(link_id)
            max_queues[link_id] = link.get_jam_density_vpkpl() * link.getFull_length() * link.getFull_lanes() / 1000
        return max_queues

    def get_signal_controller_info(self):
        X = [{"controller_id": 1,
              "stages": [{"order_id": 1,
                          "phase_ids": [1, 6]},
                         {"order_id": 2,
                          "phase_ids": [7]},
                         {"order_id": 3,
                          "phase_ids": [12]},
                         {"order_id": 4,
                          "phase_ids": [13, 14]}]},
             {"controller_id": 2,
              "stages": [{"order_id": 1,
                          "phase_ids": [2, 5]},
                         {"order_id": 2,
                          "phase_ids": [8]},
                         {"order_id": 3,
                          "phase_ids": [11]},
                         {"order_id": 4,
                          "phase_ids": [15, 16]}]},
             {"controller_id": 3,
              "stages": [{"order_id": 1,
                          "phase_ids": [3, 4]},
                         {"order_id": 2,
                          "phase_ids": [9]},
                         {"order_id": 3,
                          "phase_ids": [10]},
                         {"order_id": 4,
                          "phase_ids": [17, 18]}]}
            ]

        # list of dictionary
        # for controller in self.otmwrapper.otm.scenario().get_controllers():
        #     if str(controller.getType())=='sig_pretimed':
        #         print(controller)
        #         print(controller.getPretimed_signal_info())
        #         schedule = controller.getPretimed_signal_info().getSchedule()
        #         stagelist = schedule[0].getStages()
        #         # cntrl = {}
        #         # cntrl['id'] = int(controller.getId())
        #         # cntrl['stages'] = []

        return X

    def get_roadconnection_info(self, phase_id):
        #return [{roadconnection_id: ..., in_link: ..., out_link: ...}, {...}]
        pass

    def set_queues(self,queue_dictionary):
        for link_id, vehs in queue_dictionary.items():
            self.otmwrapper.otm.scenario().set_link_vehicles(link_id,int(vehs["waiting"]),int(vehs["transit"]))

    def set_signals(self,signal_command):
        self.otmwrapper.otm.scenario().set_signal_stage(signal_command['id'],signal_command['green_stage_order'])

    def run_simulation(self,duration):
        self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=10)

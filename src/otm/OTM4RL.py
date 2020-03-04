from OTMWrapper import OTMWrapper
import os
import inspect

# TO DO
# 1) Gabriel implement OTM set vehicles in link
# 2) Team hack get signal infrmation.
# 3) Gabriel implement OTM set_signal_stage

class OTM4RL:

    def __init__(self, configfile, jaxb_only=False):
        this_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        root_folder = os.path.dirname(os.path.dirname(this_folder))
        cfg = os.path.join(root_folder,'cfg', configfile)
        self.otmwrapper = OTMWrapper(cfg)

    def run_simulation(self,duration,output_dt):
        self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=output_dt)

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

    def set_queues(self,queue_dictionary):
        for link_id, q4link in queue_dictionary.items():
            self.otmwrapper.otm.scenario().set_link_vehicles(link_id,int(q4link['waiting']),int(q4link['transit']))

    # returns map from signal id to object
    # each controller is a dictionary with
    #   list of stages
    #       each stage is a dictionary with
    #       order
    #       phases (list of phase ids)
    # def get_signal_info(self):
    #     X = {} # id to controller
    #     for ocntrl in self.otmwrapper.otm.scenario().get_controllers():
    #         if str(ocntrl.getType())=='sig_pretimed':

    #             pcntrl = {}
    #             pcntrl['stages'] = []

    #             # print(controller)
    #             for sch in ocntrl.getSchedule():
    #                 # print(sch.getCycle())
    #                 # print(sch.getOffset())
    #                 # print(sch.getStart_time())
    #                 for stage in sch.getStages():
    #                     print(stage.getOrder())
    #                     print(stage.getDuration())
    #                     print(stage.getCycle_starttime())

    #             X[ocntrl.getId()] = pcntrl

    # returns map from controller id to an controller object (a dict)
    # cntrl['cycle']
    # cntrl['offset']
    # cntrl['stages'] an ordered list of stage dicts:
    #   stage['duration']
    #   stage['phases']
    # ordered list of stages
    # each stage is a dictionary with phases (a set) and duration (a float)
    def get_controller_info(self):
        X = {} # id to controller
        for ocntrl in self.otmwrapper.otm.scenario().get_controllers():
            if str(ocntrl.getType())=='sig_pretimed':

                cntrl = {}

                stages = []
                for schitem in ocntrl.getSchedule():
                    cntrl['cycle'] = schitem.getCycle()
                    cntrl['offset'] = schitem.getOffset()
                    for ostage in schitem.getStages():
                        stage = {}
                        stage['duration'] = ostage.getDuration()
                        stage['phases'] = ostage.getPhases()
                        stages.append(stage)

                cntrl['stages'] = stages
                X[ocntrl.getId()] = cntrl

        return X

    def set_signals(self,signal_command):
        self.otmwrapper.otm.scenario().set_signal_stage(signal_command['id'],signal_command['green_stage_order'])

    def get_signals(self):
        pass

    def get_roadconnection_info(self, phase_id):
        #return [{roadconnection_id: ..., in_link: ..., out_link: ...}, {...}]
        pass
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

    # returns a list of controllers
    # each controller is a dictionary with
    #   id
    #   list of stages
    #       each stage is a dictionary with
    #       order
    #       phases (list of phase ids)
    def get_signal_controller_info(self):
        X = [] # list of dictionary
        # for controller in self.otmwrapper.otm.scenario().get_controllers():
        #     if str(controller.getType())=='sig_pretimed':
        #         print(controller)
        #         print(controller.getPretimed_signal_info())
        #         schedule = controller.getPretimed_signal_info().getSchedule()
        #         stagelist = schedule[0].getStages()
        #         # cntrl = {}
        #         # cntrl['id'] = int(controller.getId())
        #         # cntrl['stages'] = []


        # X = [
        #     {COMPLETE THIS!!!}}
        # ]


        return X

    def get_roadconnection_info(self, phase_id):
        #return [{roadconnection_id: ..., in_link: ..., out_link: ...}, {...}]
        pass

    def set_queues(self,queue_dictionary):
        for link_id, q4link in queue_dictionary.items():
            self.otmwrapper.otm.scenario().set_link_vehicles(link_id,int(q4link['waiting']),int(q4link['transit']))

    def set_signals(self,signal_command):
        self.otmwrapper.otm.scenario().set_signal_stage(signal_command['id'],signal_command['green_stage_order'])


    def run_simulation(self,duration):
        self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=duration)

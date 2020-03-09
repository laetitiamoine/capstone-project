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
                    x['rcs'] = phase.getRoad_connections()
                    x['y'] = phase.getYellow_time()
                    x['r'] = phase.getRed_clear_time()
                    x['ming'] = phase.getMin_green_time()
                    psig['phases'][phase.getId()] = x
                X[oact.getId()] = psig

        return X      

    # returns map from controller id to an controller object (a dict)
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

    # action is a dictionar from controller id to stage index
    def set_control(self,action):
        for ctrl_id, stage_index in action.items():
            cntrl = self.otmwrapper.otm.scenario().get_actual_controller_with_id(ctrl_id)
            cntrl.set_stage_index(stage_index)

    # returns is a dictionary from controller id to stage index
    def get_control(self):
        X = {}
        for ctrl_id in self.otmwrapper.otm.scenario().get_controller_ids():
            cntrl = self.otmwrapper.otm.scenario().get_actual_controller_with_id(ctrl_id)
            X[ctrl_id] = cntrl.get_stage_index()
        return X

    def get_roadconnection_info(self, phase_id):
        #return [{roadconnection_id: ..., in_link: ..., out_link: ...}, {...}]
        pass
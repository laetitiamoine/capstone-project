from OTMWrapper import OTMWrapper


class OTM4RL:

    def __init__(self, configfile, jaxb_only=False):
        self.otmwrapper = OTMWrapper(configfile)

    def run_simulation(self,duration,output_dt):
    	self.otmwrapper.run_simple(start_time=0., duration=duration, output_dt=output_dt)

    def say_hello(self):
    	print("Hello!")


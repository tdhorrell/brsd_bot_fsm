from transitions import Machine
from random import choice
from time import sleep
import numpy as np

class BRSD_sm(object):
    def __init__(self):
        self.ready = False
        self.rand = False
        self.theta = 0
        self.dist = 0
        self.toy_array_x = [0, 0, 5, -5, 2, 2, 4, 0, 0, 0]
        self.toy_array_y = [0, 1, 2, 1, 2, -1, 3, 1, 1, 1]
        self.point_index = 0

    def calc_theta(self):
        self.dist = np.sqrt(self.toy_array_x[self.point_index]**2 + self.toy_array_y[self.point_index]**2)
        self.theta = np.rad2deg(np.arctan(self.toy_array_x[self.point_index] / self.toy_array_y[self.point_index]))
        
    def forward_ready(self, even_data):
        return (self.theta == 0 and self.dist > 0)

    def left_ready(self, even_data):
        return (self.theta < 0 and self.dist > 0)
    
    def right_ready(self, even_data):
        return (self.theta > 0 and self.dist > 0)
    
    def idle_ready(self, even_data):
        return self.dist <= 0
    
    def callback_f1(self, even_data):
        print("FORWARD CALLBACK")

# define machine states
states = ['i1', 'f1', 'l1', 'r1']

# define transition conditions
transitions = [
    ## idle transitions
    {'trigger': 'check', 'source': 'i1', 'dest': 'f1', 'conditions': 'forward_ready'},
    {'trigger': 'check', 'source': 'i1', 'dest': 'l1', 'conditions': 'left_ready'},
    {'trigger': 'check', 'source': 'i1', 'dest': 'r1', 'conditions': 'right_ready'},
    
    # forward transitions
    {'trigger': 'check', 'source': 'f1', 'dest': 'i1', 'conditions': 'idle_ready'},
    {'trigger': 'check', 'source': 'f1', 'dest': 'l1', 'conditions': 'left_ready'},
    {'trigger': 'check', 'source': 'f1', 'dest': 'r1', 'conditions': 'right_ready'},   

    # left transitions
    {'trigger': 'check', 'source': 'l1', 'dest': 'f1', 'conditions': 'forward_ready'},
    {'trigger': 'check', 'source': 'l1', 'dest': 'i1', 'conditions': 'idle_ready'},
    {'trigger': 'check', 'source': 'l1', 'dest': 'r1', 'conditions': 'right_ready'},

    # right transitions
    {'trigger': 'check', 'source': 'r1', 'dest': 'f1', 'conditions': 'forward_ready'},
    {'trigger': 'check', 'source': 'r1', 'dest': 'l1', 'conditions': 'left_ready'},
    {'trigger': 'check', 'source': 'r1', 'dest': 'i1', 'conditions': 'idle_ready'}]

class BRSD_machine(object):

    def __init__(self):
        # initialize machine
        self.model = BRSD_sm()
        self.machine = Machine(model=self.model, states=states, transitions=transitions, initial='i1', send_event=True)

        # running mode
        self.running = True

        # add callbacks
        self.machine.on_enter_f1('callback_f1')

    def run(self):
        while self.running:
            try:
                print('At state ' + self.model.state)
                print(f'\tX: ',self.model.toy_array_x[self.model.point_index],'\t\tY: ',self.model.toy_array_y[self.model.point_index])
                print(f'\tDist: ',self.model.dist,'\tTheta: ',self.model.theta)
                while not self.model.check():
                    sleep(1)
                    self.model.point_index += 1
                    self.model.calc_theta()
            except IndexError:
                print('\n*****\nEnd of Test Reached\n*****')
                break
            
brsd = BRSD_machine()
brsd.run()
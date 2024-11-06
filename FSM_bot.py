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
        self.bump_flag = False
        self.user_flag = True
        self.toy_array_x = [0, 0, 5, -5, 2, 2, 4, 0, 0, 0]
        self.toy_array_y = [0, 1, 2, 1, 2, -1, 3, 1, 1, 1]
        self.point_index = 0

    def calc_theta(self):
        self.dist = np.sqrt(self.toy_array_x[self.point_index]**2 + self.toy_array_y[self.point_index]**2)
        self.theta = np.rad2deg(np.arctan(self.toy_array_x[self.point_index] / self.toy_array_y[self.point_index]))
    
    # automatic pass transition
    def state_pass(self, even_data):
        return True


    # idle 1 transitions
    def i1_to_f1(self, even_data):
        return (self.theta > -5 and self.theta < 5 and self.dist > 0)

    def i1_to_l1(self, even_data):
        return (self.theta < -5 and self.dist > 0)

    def i1_to_r1(self, even_data):
        return (self.theta > 5 and self.dist > 0)


    # forward 1 transitions
    def f1_to_l1(self, even_data):
        return (self.theta < -5 and self.dist > 0)      

    def f1_to_r1(self, even_data):
        return (self.theta > 5 and self.dist > 0)  

    def f1_to_f2(self, even_data):
        return (self.theta >= -5 and self.theta <= 5 and self.dist > 0)


    # left 1 transitions
    def l1_to_l2(self, even_data):
        return (self.theta < -20 and self.dist > 0)

    def l1_to_f1(self, even_data):
        return (self.theta >= -5 and self.dist > 0)


    # left 2 transitions
    def l2_to_l1(self, even_data):
        return (self.theta > -20 and self.dist > 0)
    

    # right 1 transitions
    def r1_to_r2(self, even_data):
        return (self.theta > 20 and self.dist > 0)

    def r1_to_f1(self, even_data):
        return (self.theta <= 5 and self.dist > 0)
    

    # right 2 transitions
    def r2_to_r1(self, even_data):
        return (self.theta < 20 and self.dist > 0)
    
    # stop, backwards transitions can be handled by existing checks above
    # here are transitions INTO the stop states
    def state_to_s1(self, even_data):
        return self.bump_flag == True
    
    def state_to_s2(self, even_data):
        return self.user_flag == False

# define machine states
states = ['i1', 'f1', 'f2', 'l1', 'l2', 'r1', 'r2', 's1', 's2', 'b1']

# define transition conditions
transitions = [
    # idle 1 transitions
    {'trigger': 'check', 'source': 'i1', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'i1', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'i1', 'dest': 'f1', 'conditions': 'i1_to_f1'},
    {'trigger': 'check', 'source': 'i1', 'dest': 'l1', 'conditions': 'i1_to_l1'},
    {'trigger': 'check', 'source': 'i1', 'dest': 'r1', 'conditions': 'i1_to_r1'},
    
    # forward 1 transitions
    {'trigger': 'check', 'source': 'f1', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'f1', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'f1', 'dest': 'l1', 'conditions': 'f1_to_l1'},
    {'trigger': 'check', 'source': 'f1', 'dest': 'r1', 'conditions': 'f1_to_r1'},
    {'trigger': 'check', 'source': 'f1', 'dest': 'f2', 'conditions': 'f1_to_f2'},   

    # forward 2 transitions (can use same transitions as f1)
    {'trigger': 'check', 'source': 'f2', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'f2', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'f2', 'dest': 'l1', 'conditions': 'f1_to_l1'},
    {'trigger': 'check', 'source': 'f2', 'dest': 'r1', 'conditions': 'f1_to_r1'},
    # {'trigger': 'check', 'source': 'f2', 'dest': 'f1', 'conditions': 'f2_to_f1'}, 

    # left 1 transitions
    {'trigger': 'check', 'source': 'l1', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'l1', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'l1', 'dest': 'f1', 'conditions': 'l1_to_f1'},
    {'trigger': 'check', 'source': 'l1', 'dest': 'l2', 'conditions': 'l1_to_l2'},

    # left 2 transitions
    {'trigger': 'check', 'source': 'l2', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'l2', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'l2', 'dest': 'l1', 'conditions': 'l2_to_l1'},

    # right 1 transitions
    {'trigger': 'check', 'source': 'r1', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'r1', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'r1', 'dest': 'f1', 'conditions': 'r1_to_f1'},
    {'trigger': 'check', 'source': 'r1', 'dest': 'r2', 'conditions': 'r1_to_r2'},

    # right 2 transitions
    {'trigger': 'check', 'source': 'r2', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'r2', 'dest': 's2', 'conditions': 'state_to_s2'},
    {'trigger': 'check', 'source': 'r2', 'dest': 'r1', 'conditions': 'r2_to_r1'},

    # stop 1 transitions  
    {'trigger': 'check', 'source': 's1', 'dest': 'b1', 'conditions': 'state_pass'},

    # stop 2 transitions
    {'trigger': 'check', 'source': 's2', 'dest': 'l1', 'conditions': 'f1_to_l1'},
    {'trigger': 'check', 'source': 's2', 'dest': 'r1', 'conditions': 'f1_to_r1'},
    {'trigger': 'check', 'source': 's2', 'dest': 'f1', 'conditions': 'i1_to_f1'},

    # backwards 1 transitions
    {'trigger': 'check', 'source': 'b1', 'dest': 's1', 'conditions': 'state_to_s1'},
    {'trigger': 'check', 'source': 'b1', 'dest': 's2', 'conditions': 'state_to_s2'},    
    {'trigger': 'check', 'source': 'b1', 'dest': 'l1', 'conditions': 'f1_to_l1'},
    {'trigger': 'check', 'source': 'b1', 'dest': 'r1', 'conditions': 'f1_to_r1'},
    {'trigger': 'check', 'source': 'b1', 'dest': 'f1', 'conditions': 'i1_to_f1'}]

class BRSD_machine(object):

    def __init__(self):
        # initialize machine
        self.model = BRSD_sm()
        self.machine = Machine(model=self.model, states=states, transitions=transitions, initial='i1', send_event=True)

        # running mode
        self.running = True

        # state memory for testing verification
        self.state_mem = []

    def run(self):
        while self.running:
            try:
                # track current state data
                self.state_mem.append(self.model.state)
                print('At state ' + self.model.state)
                print(f'\tX: ',self.model.toy_array_x[self.model.point_index],'\t\tY: ',self.model.toy_array_y[self.model.point_index])
                print(f'\tDist: ',self.model.dist,'\tTheta: ',self.model.theta)

                # call the transition change
                self.model.point_index += 1
                self.model.calc_theta()
                self.model.check()
                sleep(1)

                # check stop flags
                if self.model.point_index == 4:
                    self.model.user_flag = False
                
                if self.model.point_index == 5:
                    self.model.user_flag = True

            except IndexError:
                print('\n*****\nEnd of Test Reached\n*****\n')
                break
            
brsd = BRSD_machine()
brsd.run()
print(f'State Memory: ',brsd.state_mem)
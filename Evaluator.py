
import math
import time

#1-D lattice total energy function evaluator class
#
class MagicPower:
    mazeMap=None
        
    @classmethod  
    def ObjFuct(cls,state):
        start = (10, 10)  
        goal = (1, 1)   
        step = 0
        isArrive = False
        for action in state:
            # 撞牆
            if cls.mazeMap[start][action] == 0:
                break
            
            step += 1
            if action == 'N':
                start = (start[0]-1, start[1])   
            elif action == 'S':
                start = (start[0]+1, start[1])   
            elif action == 'W':
                start = (start[0], start[1]-1)   
            elif action == 'E':
                start = (start[0], start[1]+1)   
                
            # 到達終點
            if start == goal:
                isArrive = True
            
        return {"isArrive": isArrive,"step": step}
        


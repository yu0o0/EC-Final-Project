
import math
import time

#1-D lattice total energy function evaluator class
#
class MagicPower:
    mazeMap=None
    act = ['N', 'E', 'S', 'W']
        
    @classmethod  
    def ObjFuct(cls,state):
        start = (10, 10)
        goal = (1, 1)
        goal2 = (10,10)
        step = 0
        isArrive = False
        isArrive2 = False
        visited = set()
        for action in state:
            # 撞牆
            if cls.mazeMap[start][action] == 0:
                break
            if action == 'N':
                tempStart = (start[0]-1, start[1])   
            elif action == 'S':
                tempStart = (start[0]+1, start[1])   
            elif action == 'W':
                tempStart = (start[0], start[1]-1)   
            elif action == 'E':
                tempStart = (start[0], start[1]+1)   
                
            # 到達終點
            if tempStart == goal:
                isArrive = True
                start = (1, 1)
                visited = set()
            elif isArrive == True:
                if tempStart == goal2:
                        isArrive2 = True
                        break
            
            if tempStart in visited:
                if cls.act.index(action) == 3:
                    action = cls.act[0]
                else:
                    action = cls.act[cls.act.index(action)+1]
                if cls.mazeMap[start][action] == 0:
                    break
                if action == 'N':
                    start = (start[0]-1, start[1])   
                elif action == 'S':
                    start = (start[0]+1, start[1])   
                elif action == 'W':
                    start = (start[0], start[1]-1)   
                elif action == 'E':
                    start = (start[0], start[1]+1)
                # break

            else:
                start = tempStart
            step += 1
            visited.add(start)

        return {"isArrive": isArrive,"isArrive2": isArrive2,"step": step}
    
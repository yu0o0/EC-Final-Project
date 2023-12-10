
import math
import time

#1-D lattice total energy function evaluator class
#
class ExploreMaze:
    mazeMap=None
    start = (1, 1)
    goal = None
    directions = ['N', 'E', 'S', 'W']
        
    @classmethod  
    def ObjFuct(cls,state):
        position = cls.start
        step = 0
        isArrive = False
        
        visited = []
        visited.append(position)
        end_flag = False
        for i,direction in enumerate(state):  
            while 1:
                # 撞牆
                if cls.mazeMap[position][direction] == 0:
                    # 下個方向沒路 且 不是左右轉
                    if not ( cls.mazeMap[position][state[i+1]]==1 \
                        and abs(cls.directions.index(state[i])-cls.directions.index(state[i+1]))==1 ):
                        end_flag = True
                    break

                if direction == 'N':
                    tempPosition = (position[0]-1, position[1])   
                elif direction == 'S':
                    tempPosition = (position[0]+1, position[1])   
                elif direction == 'W':
                    tempPosition = (position[0], position[1]-1)   
                elif direction == 'E':
                    tempPosition = (position[0], position[1]+1)   
                    
                visited.append(tempPosition)
                step += 1

                # 到達終點
                if tempPosition == cls.goal:
                    isArrive = True
                    end_flag = True
                    break
                
                position = tempPosition

            if end_flag:
                break
            
        return {"isArrive": isArrive, "step": step}, visited
        
    # @classmethod  
    # def ObjFuct(cls,state):
    #     start = (10, 10)  
    #     goal = (1, 1)   
    #     step = 0
    #     isArrive = False
    #     # visited = set()
    #     visited = []
    #     visited.append(start)
    #     for action in state:   
    #         # 撞牆
    #         if cls.mazeMap[start][action] == 0:
    #             break
    #         if action == 'N':
    #             tempStart = (start[0]-1, start[1])   
    #         elif action == 'S':
    #             tempStart = (start[0]+1, start[1])   
    #         elif action == 'W':
    #             tempStart = (start[0], start[1]-1)   
    #         elif action == 'E':
    #             tempStart = (start[0], start[1]+1)   
                
    #         # 到達終點
    #         if tempStart == goal:
    #             isArrive = True
    #             visited.append(goal)
    #             break
            
    #         # 檢查有無回頭
    #         if tempStart in visited:
    #             if cls.act.index(action) == 3:
    #                 action = cls.act[0]
    #             else:
    #                 action = cls.act[cls.act.index(action)+1]
    #             if cls.mazeMap[start][action] == 0:
    #                 break
    #             if action == 'N':
    #                 start = (start[0]-1, start[1])   
    #             elif action == 'S':
    #                 start = (start[0]+1, start[1])   
    #             elif action == 'W':
    #                 start = (start[0], start[1]-1)   
    #             elif action == 'E':
    #                 start = (start[0], start[1]+1)
    #             # break
    #         else:
    #             start = tempStart
    #         step += 1
    #         visited.append(start)
            
            
    #     return {"isArrive": isArrive,"step": step}, visited
      

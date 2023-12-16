# 1-D lattice total energy function evaluator class
#
class ExploreMaze:
    mazeMap = None
    start = (1, 1)
    goal = None
    directions = ['N', 'E', 'S', 'W']

    @classmethod
    def ObjFuct(cls, state):
        position = cls.start
        step = 0
        isArrive = False
        deadEnd = False

        path = []
        path.append(position)
        for action in state:
            # 撞牆
            if cls.mazeMap[position][action] == 0:
                break
            if action == 'N':
                tempPosition = (position[0]-1, position[1])
            elif action == 'S':
                tempPosition = (position[0]+1, position[1])
            elif action == 'W':
                tempPosition = (position[0], position[1]-1)
            elif action == 'E':
                tempPosition = (position[0], position[1]+1)

            # 到達終點
            if tempPosition == cls.goal:
                isArrive = True
                path.append(cls.goal)
                break

            # 檢查有無回頭
            if tempPosition in path:
                # if cls.directions.index(action) == 3:
                #     action = cls.directions[0]
                # else:
                #     action = cls.directions[cls.directions.index(action)+1]
                # if cls.mazeMap[position][action] == 0:
                #     break
                # if action == 'N':
                #     position = (position[0]-1, position[1])
                # elif action == 'S':
                #     position = (position[0]+1, position[1])
                # elif action == 'W':
                #     position = (position[0], position[1]-1)
                # elif action == 'E':
                #     position = (position[0], position[1]+1)
                break
            else:
                position = tempPosition
            step += 1
            path.append(position)

        # 死路
        if len([direction for direction, isRoad in cls.mazeMap[path[-1]].items() if isRoad]) == 1:
            deadEnd = True

        # 到終點距離
        distanceToGoal = abs(path[-1][0] - cls.goal[0]) + \
            abs(path[-1][1] - cls.goal[1])

        return {"isArrive": isArrive, "step": step, "distanceToGoal": distanceToGoal, "deadEnd": deadEnd}, path

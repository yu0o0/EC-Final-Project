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
        branch=[]
        path.append(position)
        for action in state:
            # 分支路口
            availabel_direction = [direction for direction, isRoad in cls.mazeMap[position].items() if isRoad]
            if len(availabel_direction) >= 3 \
                or (position == cls.start and len(availabel_direction)>=2):
                branch.append([step,position])

            # 撞牆
            if cls.mazeMap[position][action] == 0:
                break

            # if action == 'N':
            #     tempPosition = (position[0]-1, position[1])
            # elif action == 'S':
            #     tempPosition = (position[0]+1, position[1])
            # elif action == 'W':
            #     tempPosition = (position[0], position[1]-1)
            # elif action == 'E':
            #     tempPosition = (position[0], position[1]+1)

            tempPosition = cls.walk(position, action)

            # 到達終點
            if tempPosition == cls.goal:
                isArrive = True
                path.append(cls.goal)
                step += 1
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

        if not isArrive:
            availabel_direction=[direction for direction, isRoad in cls.mazeMap[path[-1]].items() if isRoad]
            # 死路
            if len(availabel_direction) == 1 \
                or all(cls.walk(path[-1],direction) in path for direction in availabel_direction):
                deadEnd = True

        # 到終點距離
        distanceToGoal = abs(path[-1][0] - cls.goal[0]) + \
            abs(path[-1][1] - cls.goal[1])

        return {"isArrive": isArrive, "step": step, "distanceToGoal": distanceToGoal, "deadEnd": deadEnd}, path, {"branch":branch, "step":step}

    def walk(position, action):
        if action == 'N':
            tempPosition = (position[0]-1, position[1])
        elif action == 'S':
            tempPosition = (position[0]+1, position[1])
        elif action == 'W':
            tempPosition = (position[0], position[1]-1)
        elif action == 'E':
            tempPosition = (position[0], position[1]+1)
        return tempPosition
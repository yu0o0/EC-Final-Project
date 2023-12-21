from pyamaze import maze
import yaml

m=maze(10,10)
m.CreateMaze(1,1,loopPercent=3)
# m.run()
print(m.maze_map)

with open("maze.yaml", "w") as yaml_file:
    yaml.dump(m.maze_map, yaml_file)
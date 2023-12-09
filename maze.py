from pyamaze import maze
import yaml

m=maze(50,50)
m.CreateMaze(10,10,loopPercent=6)
# m.run()
print(m.maze_map)

with open("maze.yaml", "w") as yaml_file:
    yaml.dump(m.maze_map, yaml_file)
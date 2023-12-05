import yaml
import matplotlib.pyplot as plt

# 自定義構建元組的方法
def tuple_constructor(loader, node):
    return tuple(loader.construct_sequence(node))

# 將自定義構建方法添加到 SafeLoader
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', lambda loader, node: tuple(loader.construct_sequence(node)))

# 載入 YAML 檔案
with open("maze.yaml", "r") as yaml_file:
    maze_map = yaml.safe_load(yaml_file)

# 現在 'data' 包含了 YAML 文件中的內容
print(maze_map)



# 設定繪圖大小
plt.figure(figsize=(11, 11))

# 繪製迷宮格子
for pos, walls in maze_map.items():
    y, x = pos
    # 畫出每個格子的四面牆壁
    if not walls['N']:
        plt.plot([x, x + 1], [y, y], 'k-')
    if not walls['S']:
        plt.plot([x, x + 1], [y+1, y+1], 'k-')
    if not walls['E']:
        plt.plot([x + 1, x + 1], [y, y + 1], 'k-')
    if not walls['W']:
        plt.plot([x, x], [y, y + 1], 'k-')

# 美化繪圖
plt.gca().invert_yaxis()
# plt.axis('off')

# 顯示繪圖
plt.show()
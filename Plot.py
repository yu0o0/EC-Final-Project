import matplotlib.pyplot as plt

class Plot:
    plot_handles = []

    def __init__(self, maze_size):
        plt.ion() #開啟interactive mode 成功的關鍵函式
        plt.figure(figsize=maze_size)
        
    @classmethod  
    def plotPath(cls, generation, pop=None, stay=False):    
        for handle in cls.plot_handles:
            handle.remove()
        cls.plot_handles = []

        plt.title(f'generation: {generation}')

        if pop:
            for i in range(len(pop)):
                # 將路徑畫在迷宮上
                # print(pop[i].path)
                path_x = [x + 0.5 for x, y in pop[i].path]
                path_y = [y + 0.5 for x, y in pop[i].path]
                handle, = plt.plot(path_y, path_x, marker='o', color='red', markersize=6)
                cls.plot_handles.append(handle)

        # 顯示繪圖
        if not stay:
            # plt.waitforbuttonpress()  # 等待用戶按下鍵盤或滑鼠按鈕
            plt.pause(0.001)     # 程式停止時間
            # plt.clf() 
        else:
            plt.ioff()
            plt.show()

    @classmethod  
    def plotMaze(cls, maze_map):
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




#
# Magic_World.py: 
#   An elitist (mu+mu) generational-with-overlap EA
#   Min-max MO problem with Pareto front
#
#
# To run: python MagicWorld.py --input magic_example.cfg
#         python MagicWorld.py --input my_params.cfg
#
#   - Supports self-adaptive mutation
#   - Uses MO-binary tournament selection for mating pool
#   - Uses MO-elitist truncation selection for survivors
#

import optparse
import sys
import yaml
import math
import time
from random import Random
import matplotlib.pyplot as plt
from Population import *
from Evaluator import *




#MagicWorld Config class 
class MagicWorld:
    """
    MagicWorld configuration class
    """
    # class variables
    sectionName='maze'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'crossoverFraction': (float,True),
             'evaluator': (str,True),
             'rounds': (int,True),
             'magicTypes': (int,True),
             'selfCost' : (list,True),
             'selfDamage': (list,True),
             'EnhanceDamage': (list,True),
             'map': (str,True),}
     
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get MagicWorld section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing {} section in cfg file'.format(self.sectionName))
         
        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval=eccfg[opt]
 
                #verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))
                 
                #create attributes on the fly
                setattr(self,opt,optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self,opt,None)
     
    #string representation for class data    
    def __str__(self):
        return str(yaml.dump(self.__dict__,default_flow_style=False))
         


#Print some useful stats to screen
def printStats(pop,gen):
    print('Generation:',gen)
    # avgDamage=0
    # avgCost=0
    # costval,maxval=pop[0].objectives
    # mutRate=pop[0].mutRate
    for ind in pop:
        # avgDamage+=ind.objectives[1]
        # avgCost+=ind.objectives[0]
        # if ind.objectives[1] > maxval:
        #     costval,maxval=ind.objectives
        #     mutRate=ind.mutRate
        print(f'{ind} {ind.objectives["isArrive"]} {ind.objectives["step"]}')

    # print('Max Damage',maxval)
    # print('Most powerful Spell Cost',costval)
    # print('Avg Damage',avgDamage/len(pop))
    # print('Avg Cost',avgCost/len(pop))
    # print('MutRate',mutRate)
    # print('')

#
# Helper function that allows us to init all cfg-related class
#  variables on our Pool worker processes
#
def initClassVars(cfg):
    MagicianIndividual.ObjFunc=MagicPower.ObjFuct
    MagicianIndividual.nRounds=cfg.rounds
    MagicianIndividual.nSpells=cfg.magicTypes
    MagicianIndividual.learningRate=1.0/math.sqrt(cfg.rounds)

    if len(cfg.selfDamage) != cfg.magicTypes: raise Exception('Inconsistent selfDamage vector length')
    if len(cfg.EnhanceDamage) != cfg.magicTypes: raise Exception('Inconsistent EnhanceDamage matrix size')
    Population.individualType=MagicianIndividual


def plotMaze(maze_map):
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


#EV3_MO:
#            
def EV3(cfg):
    # 將自定義構建方法添加到 SafeLoader
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', lambda loader, node: tuple(loader.construct_sequence(node)))
    # 載入 YAML 檔案
    with open(cfg.map, "r") as yaml_file:
        maze_map = yaml.safe_load(yaml_file)
    print(maze_map)
    # plotMaze(maze_map)

    #start random number generators
    uniprng=Random()
    uniprng.seed(cfg.randomSeed)
    normprng=Random()
    normprng.seed(cfg.randomSeed+101)

    #set static params on classes
    # (probably not the most elegant approach, but let's keep things simple...)
    Individual.uniprng=uniprng
    Individual.normprng=normprng
    Population.uniprng=uniprng
    Population.crossoverFraction=cfg.crossoverFraction
    MagicPower.mazeMap=maze_map
    initClassVars(cfg)

    #create initial Population (random initialization)
    population=Population(cfg.populationSize)
    population.sort()

    #print initial pop stats    
    printStats(population,0)
    # population.generatePlots(title=f'Generation 0')

    #evolution main loop
    for i in range(cfg.generationCount):
        #create initial offspring population by copying parent pop
        offspring=population.copy()
        
        #select mating pool
        #offspring.conductTournament()
        offspring.binaryTournament()
        
        #perform crossover
        
        offspring.crossover()
        
        #random mutation
        offspring.mutate()
        
        #Upadates obejectives
        offspring.evaluateObjectives()

            
        #survivor selection: elitist truncation using parents+offspring
        population.combinePops(offspring)

        #Obejectives are changed, so remeber to update the ranking before turcation occurs.
        # population.updateRanking()
        population.sort()

        #population.truncateSelect(cfg.populationSize)
        population.truncation(cfg.populationSize)
        
        #print population stats    
        printStats(population,i+1)
        #print the objective space with its frontRank
        # population.generatePlots(title=f'Generation {i+1}')


        
        
#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default="maze.cfg")
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=True)
        (options, args) = parser.parse_args(argv)
        
        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")
        
        #Get MagicWorld config params
        cfg=MagicWorld(options.inputFileName)
        
        #print config params
                    
        #run EV3_MO
        start_time=time.asctime()
        EV3(cfg)

        print('Start time: {}'.format(start_time))
        print('End time  : {}'.format(time.asctime()))
        
        if not options.quietMode:                    
            print('MagicWorld Completed!')    
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()
    

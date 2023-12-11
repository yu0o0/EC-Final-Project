#
# Population.py
#
#

import copy
import math
from operator import attrgetter
from Individual import *
# import matplotlib.pyplot as plt

class Population:
    """
    Population
    """
    uniprng=None
    crossoverFraction=None
    individualType=None
    
    def __init__(self, populationSize):
        """
        Population constructor
        """
        self.population=[]
        for i in range(populationSize):
            self.population.append(self.__class__.individualType())                                                                                                                                        

    def __len__(self):
        return len(self.population)
    
    def __getitem__(self,key):
        return self.population[key]
    
    def __setitem__(self,key,newValue):
        self.population[key]=newValue
        
    def copy(self):
        return copy.deepcopy(self)

    def evaluateObjectives(self):
        for individual in self.population: individual.evaluateObjectives()
            
    def mutate(self):     
        for individual in self.population:
            individual.mutate()
            
    def crossover(self):
        indexList1=list(range(len(self)))
        indexList2=list(range(len(self)))
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)
            
        if self.crossoverFraction == 1.0:             
            for index1,index2 in zip(indexList1,indexList2):
                self[index1].crossover(self[index2])
        else:
            for index1,index2 in zip(indexList1,indexList2):
                rn=self.uniprng.random()
                if rn < self.crossoverFraction:
                    self[index1].crossover(self[index2])        

    def combinePops(self,otherPop):
        self.population.extend(otherPop.population)

    def computeCrowding(self):
        """
        Compute crowding metric using k-th nearest-neighbor w/ normalized distance.
        """
        
        if len(self.population) == 0: return #nothing to do
        
        # if single objective, set all densities to zero then return
        if self.population[0].numObj == 1:
            for ind in self.population:
                ind.crowdDist=0.0
            return
                
        # compute k for knn density estimate
        kdist=int(math.sqrt(len(self.population)))
        
        # compute normalization vector
        maxObj=self.population[0].objectives.copy()
        minObj=self.population[0].objectives.copy()
        for ind in self.population:
            for i in range(ind.numObj):
                if ind.objectives[i] < minObj[i]: minObj[i]=ind.objectives[i]
                if ind.objectives[i] > maxObj[i]: maxObj[i]=ind.objectives[i]
        
        normVec=[]        
        for min,max in zip(minObj,maxObj):
            norm=math.fabs(max-min)
            if norm == 0: norm=1.0 #watch out for possible divide by zero problems
            normVec.append(norm)    
        
        # init distance matrix
        distanceMatrix=[]
        for i in range(len(self.population)):
            distanceMatrix.append([0.0]*len(self.population))
        
        # compute distance matrix
        # (matrix is diagonally symmetric so only need to compute half, then reflect)
        for i in range(len(self.population)):
            for j in range(i+1):
                distanceMatrix[i][j]=self.population[i].distance(self.population[j],normVec)
                distanceMatrix[j][i]=distanceMatrix[i][j]
                      
        # sort the rows by distance
        for row in distanceMatrix:
            row.sort()
        
        # find the crowding distance using knn index
        i=0
        for ind in self.population:
            ind.crowdDist=distanceMatrix[i][kdist]
            i+=1

    def computeFrontRanks(self):
        """
        Compute non-dominated front ranks using NSGA-II front-ranking scheme
        """
        tmpPop=self.population.copy()
        currentFrontRank=0
        while len(tmpPop) > 0:
            for ind1 in tmpPop:
                for ind2 in tmpPop:
                    if ind2.dominates(ind1) == 1:
                        ind1.frontRank=-1
                        break
                    else:
                        ind1.frontRank=currentFrontRank
            
            tmpTmpPop=tmpPop.copy() #be careful here since .remove is in for loop        
            for ind in tmpTmpPop:
                if ind.frontRank == currentFrontRank: tmpPop.remove(ind)
            
            #increment currentFrontRank to next level
            currentFrontRank+=1

    def binaryTournament(self):
        """
        Multi-objective binary tournament operator based on non-domination front-ranking scheme.
        
        Input Parameters:
          prng: Random number generator (i.e., random.Random object)
    
        Note: Similar to single-objective implementation, 
          - Tournament pairs should be randomly selected
          - All individuals from initial population should participate in exactly 2 tournaments   
        """

        # generate random binary tournament pairs
        popSize=len(self.population)
        indexList1=list(range(popSize))
        indexList2=list(range(popSize))
        
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)
        
        # do not allow self competition
        for i in range(popSize):
            if indexList1[i] == indexList2[i]:
                temp=indexList2[i]
                if i == 0:
                    indexList2[i]=indexList2[-1]
                    indexList2[-1]=temp
                else:
                    indexList2[i]=indexList2[i-1]
                    indexList2[i-1]=temp
        
        #compete
        newPop=[]        
        for index1,index2 in zip(indexList1,indexList2):
            if index1 < index2:
                newPop.append(copy.deepcopy(self.population[index1]))
            elif index1 > index2:
                newPop.append(copy.deepcopy(self.population[index2]))
            else:
                rn=self.uniprng.random()
                if rn > 0.5:
                    newPop.append(copy.deepcopy(self.population[index1]))
                else:
                    newPop.append(copy.deepcopy(self.population[index2]))
        
        # overwrite old pop with newPop (i.e., the selected pop)   
        self.population=newPop
    
    def truncation(self,newpopsize):
        self.population=self.population[:newpopsize]
        
    def updateRanking(self):
        """
        Update front-rank and crowding distance for entire population
        """
        self.computeFrontRanks()
        self.computeCrowding()
    
    def generatePlots(self,title=None,showPlot=True):
        #first, make sure state & objective space have at least 2 dimensions, pop size at least 1
        if len(self.population) < 1:
            raise Exception('showPlots error: Population size must be >= 1 !')
        if (len(self.population[0].state) < 2) or (len(self.population[0].objectives) < 2):
            raise Exception('showPlots error: State & objective spaces must have at least 2 dimensions!')

        #if front ranking has not been computed, then skip
        if self.population[0].frontRank is None: plotOrder=[111,000]
        else: plotOrder=[121,122]

        plt.subplots_adjust(wspace=0.75) #increase spacing between plots a bit
        plt.subplot(plotOrder[0])
        x=[ind.objectives[0] for ind in self.population]
        y=[ind.objectives[1] for ind in self.population]
        plt.scatter(x,y)
        plt.xlabel('Spell Cost')
        plt.ylabel('Total Damage')
        plt.title('Objective space of'+ title)

        if self.population[0].frontRank is not None:
            plt.subplot(plotOrder[1])
            maxRank=0
            for ind in self.population:
                if ind.frontRank > maxRank: maxRank=ind.frontRank
            
            rank=0
            while rank<= maxRank:
                xy=[ind.objectives for ind in self.population if ind.frontRank == rank]
                xy.sort(key=lambda obj: obj[0]) #need to sort in 1st dim to make connected line plots look sensible!
                x=[obj[0] for obj in xy]
                y=[obj[1] for obj in xy]
                plt.plot(x,y,marker='o',label=str(rank))
                rank+=1
            plt.xlabel('Mana Cost')
            plt.ylabel('Total Damage')
            plt.title('Ranked Fronts of' + title)

        if showPlot:
            plt.show()
        
    def sort(self):
        #self.population.sort(key=lambda ind: (-ind.objectives["step"]))
        #self.population.sort(key=lambda ind: (-ind.objectives["step"]))
        self.population.sort(key=lambda ind: (-ind.objectives["isArrive"], -ind.objectives["step"]))
                
    def __str__(self):
        s=''
        for ind in self:
            s+=str(ind) + '\n'
        return s


        
    

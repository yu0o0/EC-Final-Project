#
# Individual.py
#
#

import math

# Base class for all individual types
#


class Individual:
    """
    Individual
    """
    minMutRate = 1e-100
    maxMutRate = 1
    learningRate = None
    uniprng = None
    normprng = None
    ObjFunc = None

    def __init__(self):
        # self.objectives, self.path, self.branch=self.__class__.ObjFunc(self.state)
        self.objectives = None
        self.evaluateObjectives()
        self.mutRate = self.uniprng.uniform(0.9, 0.1)  # use "normalized" sigma
        self.numObj = len(self.objectives)

    def mutateMutRate(self):
        self.mutRate = self.mutRate * \
            math.exp(self.learningRate*self.normprng.normalvariate(0, 1))
        if self.mutRate < self.minMutRate:
            self.mutRate = self.minMutRate
        if self.mutRate > self.maxMutRate:
            self.mutRate = self.maxMutRate

    def evaluateObjectives(self):
        if self.objectives == None:
            self.objectives, self.path, self.info = self.__class__.ObjFunc(
                self.state)

    def dominates(self, other):
        dominatesCount = 0
        equalsCount = 0
        inferiorCount = 0

        i = 0
        while i < self.numObj:
            # minimize mana cost
            if i == 0:
                if self.objectives[i] < other.objectives[i]:
                    dominatesCount += 1
                elif self.objectives[i] > other.objectives[i]:
                    inferiorCount += 1
                else:
                    equalsCount += 1
                i += 1

            # maximize spell damage
            else:
                if self.objectives[i] > other.objectives[i]:
                    dominatesCount += 1
                elif self.objectives[i] < other.objectives[i]:
                    inferiorCount += 1
                else:
                    equalsCount += 1
                i += 1

        if equalsCount == self.numObj:
            return 0  # the two are non-dominating
        elif dominatesCount+equalsCount == self.numObj:
            return 1  # self dominates other
        elif inferiorCount+equalsCount == self.numObj:
            return -1  # other dominates self
        else:
            return 0  # the two are non-dominating

    def compareRankAndCrowding(self, other):
        if self is other:
            return 0

        if self.frontRank < other.frontRank:
            return 1
        elif self.frontRank > other.frontRank:
            return -1
        else:
            if self.crowdDist > other.crowdDist:
                return 1
            elif self.crowdDist < other.crowdDist:
                return -1
            else:
                return 0

    def distance(self, other, normalizationVec=[None]):
        """
        Compute distance between self & other in objective space
        """
        # check if self vs self
        if self is other:
            return 0.0

        # set default normalization to 1.0, if not specified
        if normalizationVec[0] == None:
            normalizationVec = [1.0]*self.numObj

        # compute normalized Euclidian distance
        distance = 0
        i = 0
        while i < self.numObj:
            tmp = (self.objectives[i]-other.objectives[i])/normalizationVec[i]
            distance += (tmp*tmp)
            i += 1

        distance = math.sqrt(distance)

        return distance


class MazeIndividual(Individual):
    """
    Magic World
    """
    nSpells = None
    nRounds = None

    def __init__(self):
        self.state = []
        for i in range(self.nRounds):
            self.state.append(self.uniprng.choice(['E', 'N', 'S', 'W']))

        super().__init__()

    def crossover(self, other):
        # perform crossover "in-place"
        # for i in range(self.nRounds):
        #     if self.uniprng.random() < 0.5:
        #         tmp = self.state[i]
        #         self.state[i] = other.state[i]
        #         other.state[i] = tmp

        # tmp = other.state.copy()
        # self.state[self.info["step"]:] = tmp[self.info["step"]:]
        # other.state[other.info["step"]:] = self.state[other.info["step"]:]

        end_steps = [branch[0] for branch in other.info["branch"] if branch[0] > self.info["step"]]
        end_steps.append(self.nRounds)
        end_step = self.uniprng.choice(end_steps)
        self.state[self.info["step"]:end_step] = other.state[self.info["step"]:end_step]
        # self.state[self.info["step"]:] = other.state[self.info["step"]:]

        self.objectives = None
        # other.objectives = None

    def mutate(self):
        self.mutateMutRate()  # update mutation rate

        # if self.branch:
        #     for i in range(self.branch[-1][0], self.nRounds):
        #         if self.uniprng.random() < self.mutRate:
        #             self.state[i]=self.uniprng.choice(['E', 'N', 'S', 'W'])
        # else:
        #     for i in range(self.nRounds):
        #         if self.uniprng.random() < self.mutRate:
        #             self.state[i]=self.uniprng.choice(['E', 'N', 'S', 'W'])
        
        # 有crossover就跳過
        if self.objectives == None:
            return

        
        prob = self.mutRate
        # prob = 0.7
        # 走錯路那步突變
        if self.uniprng.random() < prob or not self.info["branch"]:
            # for i in range(self.info['step'], self.nRounds):
            #     self.state[i] = self.uniprng.choice(['E', 'N', 'S', 'W'])
            self.state[self.info['step']] = self.uniprng.choice(['E', 'N', 'S', 'W'])
        else:
            # for i in range(self.branch[-1][0], self.nRounds):
            for i in range(self.uniprng.choice(self.info["branch"])[0], self.nRounds):
                self.state[i] = self.uniprng.choice(['E', 'N', 'S', 'W'])

        # else:
        #     for i in range(self.nRounds):
        #         self.state[i]=self.uniprng.choice(['E', 'N', 'S', 'W'])

        self.objectives = None

    def __str__(self):
        return str(self.state)+'\t'

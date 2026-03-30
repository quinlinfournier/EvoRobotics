import copy

from solution import SOLUTION
import constants as c

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()



    def Evolve(self):
        self.parent.Evluate("GUI")

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):

        self.Spawn()
        self.Mutate()
        self.child.Evluate("DIRECT")
        print("\nParent fitness:", self.parent.fitness, "Child fitness:", self.child.fitness)
        self.Select()

    def Spawn(self):
        # self.child = copy.deepcopy(self.parent)
        self.children = {}

        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        self.child.mutate()

    def Select(self):
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child

    def Show_Best(self):
        self.parent.Evluate("GUI")


    
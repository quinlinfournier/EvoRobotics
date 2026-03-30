import copy
import os
from solution import SOLUTION
import constants as c

class PARALLEL_HILL_CLIMBER:

    def __init__(self):

        os.system("del fitness*.txt")
        os.system("del brain*.nndf")

        self.parents = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):

        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):

        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].mutate()

    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()

    def Print(self):
        print("\n")
        for i in self.parents:
            print(f"Parent fitness: {self.parents[i].fitness}, Child fitness: {self.children[i].fitness}")
        print("\n")
    
    def Select(self):
        for i in self.children:
            if self.children[i].fitness < self.parents[i].fitness:
                self.parents[i] = self.children[i]

    def Show_Best(self):
        best_parent = self.parents[0]
        for i in self.parents:
            if self.parents[i].fitness < best_parent.fitness:
                best_parent = self.parents[i]
        best_parent.Start_Simulation("GUI")

    
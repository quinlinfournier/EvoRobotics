from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER


phc = PARALLEL_HILL_CLIMBER()

phc.Evolve()
phc.Save_Matrix()
phc.Show_Best()
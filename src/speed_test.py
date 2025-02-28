import cProfile
import pstats
#from utility import ensureCorrectPath

profiler = cProfile.Profile()
profiler.enable()

# Your slow function calls here
import pypenguin.database
#print(pypenguin.optimize)
print(pypenguin.database.opcodeDatabase)

#import pickle
#def load_opcodes():
##    with open(ensureCorrectPath("src/pypenguin/database/database.pkl", "PyPenguin"), "rb") as f:
#    with open("pypenguin/database/database.pkl", "rb") as f:
#        return pickle.load(f)
#OPCODES = load_opcodes()
#print(OPCODES)  # Example usage

profiler.disable()
stats = pstats.Stats(profiler)
stats.strip_dirs().sort_stats("cumulative").print_stats(20)  # Show top 20 slowest calls

import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your slow function calls here
import pypenguin.database

profiler.disable()
stats = pstats.Stats(profiler)
stats.strip_dirs().sort_stats("cumulative").print_stats(20)  # Show top 20 slowest calls

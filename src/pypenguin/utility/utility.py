from enum import Enum

# -----------------------------------
# Other Utility Classes and Functions
# -----------------------------------
class Platform(Enum):
    PENGUINMOD = 0
    SCRATCH    = 1


class BlockSelector:
    count = 0
    def __init__(self):
        self.id = BlockSelector.count
        BlockSelector.count += 1
    def __eq__(self, other):
        if isinstance(other, BlockSelector):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"tSn::{self.id}"
    
    def copy(self):
        new = BlockSelector()
        new.id = self.id
        return new

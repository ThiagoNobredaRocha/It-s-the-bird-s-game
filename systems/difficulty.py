import math

def get_difficulty(score, limit=1, slope=0.004, midpoint=2000):
    return limit / (1 + math.exp(-slope * (score - midpoint)))

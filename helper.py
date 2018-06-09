from itertools import tee, islice


def nwise(iterable, n=2):
    iters = tee(iterable, n)
    for i, it in enumerate(iters):
        next(islice(it, i, i), None)
    return zip(*iters)


def grouped(iterable, n):
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."""
    """https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list"""
    return zip(*[iter(iterable)]*n)


def bell_curve(value: float, opt_value: float, scaling_value: float) -> float:
    """MWinter Paper: Genetic Programming for Automated Quest Generation"""
    return 1 / (1 + scaling_value * pow(opt_value - value, 2))

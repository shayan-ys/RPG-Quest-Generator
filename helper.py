from itertools import tee, islice
import re


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


def camel_case_to_underscore(name):
    """ https://stackoverflow.com/a/1176023/4744051 """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def dict_pretty_str(dictionary: dict) -> str:
    pretty_str = '{'
    for key, value in dictionary.items():
        pretty_str += '\n\t' + str(key) + ': ' + str(value)
    return pretty_str + '\n}'


def sort_by_list(keys: list, sort_by: list) -> list:
    return [x for _, x in sorted(zip(sort_by, keys), key=lambda pair: pair[0])]

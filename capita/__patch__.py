# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import germania
import utilo


def authors(raw: str, verbose: bool = False) -> list:
    """\
    >>> authors('PEREIRA, M.G., VOLCHAN, E., SOUZA, G. G. DE, OLIVEIRA, L.,'
    ... 'CAMPAGNOLI, R. R., PINHEIRO, W. M., & PESSOA, L. ')
    ['PEREIRA, M.G.', 'VOLCHAN, E.', 'SOUZA, G. G. DE', 'OLIVEIRA, L.', 'CAMPAGNOLI, R. R.', 'PINHEIRO, W. M.', 'PESSOA, L.']
    """
    pattern = r"""
        [a-zA-Z]{4,}\,
        [ ]{0,2}
        ([a-zA-Z]\.[ ]{0,2}){1,3}
        [ ]{0,2}
        (DE)?
    """
    result = []
    for item in re.finditer(pattern, raw, re.VERBOSE):
        item = utilo.extract_match(item).strip()
        if verbose:
            item = (item, item)
        result.append(item)
    return result


germania.authors = authors


def a_minus_b(a: set | list, b: set | list) -> set | list:
    result = []
    for item in a:
        if item in b:
            continue
        result.append(item)
    if isinstance(a, set):
        result: set = set(result)
    return result


utilo.a_minus_b = a_minus_b


def union(*items: set | list):
    """\
    >>> union([1, 2, 3])
    [1, 2, 3]
    >>> union([1, 2, 3], [2, 2, 2])
    [1, 2, 3]
    """
    result = []
    for item in items:
        for it in item:
            result.append(it)
    result = utilo.make_unique(result)
    return result


utilo.union = union

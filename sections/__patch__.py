# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import german
import utila


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
        item = utila.extract_match(item).strip()
        if verbose:
            item = (item, item)
        result.append(item)
    return result


german.authors = authors

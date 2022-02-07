# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import utila


def valid_line(line: str) -> bool:
    line = line.strip()
    if line.count('. .') > 3:
        return True
    if line.count('..') > 3:
        return True
    if elements.level_numbered(line):
        return True
    if LINE_WITHPAGES.match(line):
        return True
    return False


# E. Abschließende Zusammenfassung      S. 85
LINE_WITHPAGES = utila.compiles(r'^.+S\.[ ]{0,3}\d{1,4}$')

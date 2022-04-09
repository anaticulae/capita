# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def huge_match(line: str, part: str) -> bool:
    """Ensure that matched `part` is long enough in detected line.

    >>> huge_match('20 Bilanz und Ausblick einer Wissenschaft', 'Ausblick')
    False
    """
    line = line.lower()
    if utila.iterable(part):
        return any(huge_match(line, item) for item in part)
    if part not in line:
        return False
    percent = len(part) / len(line)
    if percent < 0.5:
        # matched part is to small
        return False
    return True


def startswith(line: str, start: str) -> bool:
    """\
    >>> startswith('Methode3', '2 Methode3')
    True
    """
    percent = len(line) / len(start) if line else 0.0
    start = start[0:len(line)]
    maxdiff = 0.9 if len(start) > 10 else 0.7  # TODO: HOLY VALUE
    if percent < 0.5:
        # matched part is to small
        maxdiff = 0.9
    # TODO: REPLACE WITH UTILA CODe
    if utila.similar(start, line, maxdiff=maxdiff):
        return True
    return False

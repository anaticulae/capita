# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Workplan Runner
===============

Workplan
--------

.. code-block:: none

    [titlepage]
        char_margin = 10
        word_margin = 20

    [bibliography]
        char_margin = 100

    > titlepage

        > rawmaker -i abc.pdf -o extracted/titlepage --config titlepage.cfg
        > detector -i expected/titlepage -o detector_result --title --page=2

    > bibliography

        > rawmaker -i abc.pdf -o extracted/bibliography --config bibliography.cfg
        > detector -i expected/titlepage -o detector_result --bibliography --page=14:15

    > text ...
"""

import utila


def setup_plan(plan, config: dict) -> str:
    """Fill template strings with absolute paths and configuration.

    >>> setup_plan(['decider -i {RAWMAKER_INPUT} -o {OUTPUT}'],
    ... {'rawmaker_input' : 'source.txt', 'output' : 'output.txt'})
    'decider -i source.txt -o output.txt'

    Returns:
        fully replaced workplan template
    Raises:
        ValueError: if not every template string is replaced
    """
    result = utila.NEWLINE.join(plan)
    # replace templates
    for key, value in config.items():
        key = '{%s}' % key.upper()
        result = result.replace(key, value)
    if '{' in result or '}' in result:
        raise ValueError(f'template is not fully replaced:\n{result}')
    return result


def group_plan(plan: list, level=-1) -> str:
    result = []
    if isinstance(plan, list):
        for item in plan:
            result.append(group_plan(item, level + 1))
    else:
        level = '    ' * level
        return level + '>' + plan
    joined = utila.NEWLINE.join(result)
    return joined + utila.NEWLINE

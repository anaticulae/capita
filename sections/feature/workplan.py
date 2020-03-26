# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Schedule Workingplan
====================

Todo:

* Lookup to derivate todo from expected section
* How to handle low trusted areas?
* Check for text extraction and if not successful than ignore sections?

"""
import serializeraw

import sections.workplan.creator


def work(section_result: str, pages: tuple = None) -> str:
    loaded = serializeraw.load_sections(section_result, pages=pages)

    plan = sections.workplan.creator.create(loaded)
    grouped = sections.workplan.runner.group_plan(plan)

    return grouped

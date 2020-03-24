# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sections.feature.workplan
import sections.workplan.creator
import tests.example.sections
import tests.resources


def test_workplan_simplify_group():
    example = tests.example.sections.EXAMPLE
    merged_title = sections.workplan.creator.simplify_group(example[0])
    assert len(merged_title) == 1

    merged_toc = sections.workplan.creator.simplify_group(example[1])
    assert len(merged_toc) == 1

    merged_toc = merged_toc[0]
    assert merged_toc.start == 1
    assert merged_toc.end == 2


def test_workplan_create_plan():
    example = tests.example.sections.EXAMPLE
    plan = sections.workplan.creator.create(example)
    assert len(plan) == 4, str(plan)

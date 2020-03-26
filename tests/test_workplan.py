# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import sections.feature.section
import sections.feature.workplan
import sections.workplan.creator
import sections.workplan.runner
import tests.example.sections
import tests.resources


def test_workplan_simplify_group():
    example = tests.example.sections.EXAMPLE
    merged_title = sections.workplan.creator.simplify(example[0])
    assert len(merged_title) == 1

    merged_toc = sections.workplan.creator.simplify(example[1])
    assert len(merged_toc) == 1

    merged_toc = merged_toc[0]
    assert merged_toc.start == 1
    assert merged_toc.end == 2


def test_workplan_create_plan():
    example = tests.example.sections.EXAMPLE
    plan = sections.workplan.creator.create(example)
    assert len(plan) == 8, str(plan)


def master72():
    extracted = sections.feature.section.extract_sections_frompath(
        tests.resources.MASTER72)
    plan = sections.workplan.creator.create(extracted)
    return plan


def test_workplan_master72_create_plan():
    plan = master72()
    assert len(plan) == 8, str(plan)


EXPECTED = """\
>titlepage
    >rawmaker -i {SOURCE} -o {RAWMAKER_TITLE} -c {RAWMAKER_CFG_TITLE} --pages=0
    >detector --titlepage --pages=0 -i {RAWMAKER_TITLE} -o {DETECTOR_RESULT}

>toc
    >rawmaker -i {SOURCE} -o {RAWMAKER_TOC} -c {RAWMAKER_CFG_TOC} --pages=1:2
    >groupme --toc --pages=1:2 -i {RAWMAKER_TOC} -o {GROUPME_RESULT}

>text
    >rawmaker -i {SOURCE} -o {RAWMAKER_WORDS} -c {RAWMAKER_CFG_WORDS} --pages=3:9
    >words --pages=3:9 -i {RAWMAKER_WORDS} -o {WORDS_RESULT}

>bibliography
    >rawmaker -i {SOURCE} -o {RAWMAKER_BIBLIOGRAPHY} -c {RAWMAKER_CFG_BIBLIOGRAPHY} --pages=10:11
    >detector --bibliography --pages=10:11 -i {RAWMAKER_BIBLIOGRAPHY} -o {DETECTOR_RESULT}

"""


def test_workplan_simple_group_plan():
    example = tests.example.sections.EXAMPLE
    plan = sections.workplan.creator.create(example)
    result = sections.workplan.runner.group_plan(plan)
    assert result == EXPECTED


def test_workplan_runner_split():
    result = sections.workplan.runner.split(EXPECTED)
    assert len(result) == 4, result


PLAN = """\
>first
    >ls -a

>third
    >echo hi
    >echo hi
    >echo hi
"""


def test_workplan_runner_runtime(testdir, capsys):
    root = testdir.tmpdir
    returncode = sections.workplan.runner.runtime(PLAN, cwd=root)
    stdout = capsys.readouterr().out
    assert 'hi' in stdout, str(stdout)
    assert returncode == utila.SUCCESS


ERROR = """\
>first
    >this is just an error
"""


def test_workplan_runner_runtime_error():
    returncode = sections.workplan.runner.runtime(ERROR)
    assert returncode >= utila.FAILURE


def test_setuptestfolder_and_setupplan(testdir):
    root = testdir.tmpdir
    source = tests.resources.MASTER72_PDF
    config = sections.workplan.runner.setup_testfolder(
        root,
        source,
        config=root,
        dry=True,
    )
    replaced = sections.workplan.runner.setup_plan(EXPECTED, config)
    assert replaced

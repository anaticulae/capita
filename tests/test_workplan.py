# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import textwrap

import utila

import sections.feature.section
import sections.feature.workplan
import sections.workplan.serialize
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


def test_workplan_simple_dump_plan():
    example = tests.example.sections.EXAMPLE
    plan = sections.workplan.creator.create(example)
    result = sections.workplan.serialize.dump_cmds(plan)
    assert '>titlepage' in result
    assert '>toc' in result
    assert '>tex' in result
    assert '>rawmaker' in result


def test_workplan_runner_split():
    loaded = sections.workplan.serialize.load_plan(EXPECTED)
    assert len(loaded.cmds) == 4, loaded


def test_workplan_runner_runtime(testdir, capsys):
    plan = textwrap.dedent("""\
    >first
        >ls -a
    >third
        >echo hi
        >echo hi
        >echo hi
    """)
    root = testdir.tmpdir
    returncode = sections.workplan.runner.runtime(plan, cwd=root)
    stdout = capsys.readouterr().out
    assert 'hi' in stdout, str(stdout)
    assert returncode == utila.SUCCESS


def test_workplan_runner_runtime_error():
    error = textwrap.dedent("""
    >first
        >this is just an error
    """)
    returncode = sections.workplan.runner.runtime(error)
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


@utila.skip_longrun
def test_workplan_runner(testdir):
    root = testdir.tmpdir
    extracted = sections.feature.section.extract_sections_frompath(
        tests.resources.HOWTO_ARGPARSE)
    extracted_plan = sections.workplan.creator.create(extracted)
    grouped = sections.workplan.serialize.dump_cmds(extracted_plan)

    utila.file_create('rawmaker_cfg_title.ini')
    utila.file_create('rawmaker_cfg_title_oneline.ini')
    utila.file_create('rawmaker_cfg_toc.ini')
    utila.file_create('rawmaker_cfg_words.ini')
    utila.file_create('rawmaker_cfg_bibliography.ini')
    utila.file_create('rawmaker_cfg_bibliography_oneline.ini')
    config = sections.workplan.runner.setup_testfolder(
        path=root,
        source=tests.resources.HOWTO_ARGPARSE_PDF,
        config=root,
    )
    raw = sections.workplan.runner.setup_plan(grouped, config)

    completed = sections.workplan.runner.runtime(raw, cwd=root)
    assert completed == utila.SUCCESS, str(completed)


def example_raw_plan() -> str:
    example = tests.example.sections.EXAMPLE
    plan = sections.workplan.creator.create(example)
    executionplan = sections.workplan.serialize.ExecutionPlan(cmds=plan)
    assert len(executionplan.cmds) == 8, str(executionplan)
    tailer = sections.workplan.serialize.dump_plan(executionplan)

    config = {
        'rawmaker_cfg_title': {
            'char_margin': 10
        },
        'rawmaker_cfg_title_oneline': {},
        'rawmaker_cfg_toc': {
            'raw': 10.5
        },
    }
    header = sections.workplan.serialize.dump_config(config)
    result = f'{header}\n{tailer}'
    assert 'char_margin = 10' in result, result
    assert 'raw = 10.5' in result, result
    return result


def test_workplan_create_plan_with_config():
    example = example_raw_plan()
    assert '{RAWMAKER_CFG_BIBLIOGRAPHY}' in example, example
    config = {
        'rawmaker_cfg_bibliography': '/c/config.ini',
    }
    plan = sections.workplan.runner.setup_plan(
        example,
        config=config,
        validate=False,
    )
    # check that template ...
    assert '{RAWMAKER_CFG_BIBLIOGRAPHY}' not in plan, plan
    # ... was replaced
    assert '/c/config.ini' in plan, plan

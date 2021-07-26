# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import power
import serializeraw
import utilatest

import sections
import sections.cli

#pylint:disable=C0103
run_sections = functools.partial(
    utilatest.run_command,
    main=sections.cli.main,
    process=sections.PROCESS,
    success=True,
)

run_sections_failure = functools.partial(
    utilatest.run_command,
    main=sections.cli.main,
    process=sections.PROCESS,
    success=False,
)

utilatest.register_marker('huge')


def sections_from_dir(pdf: str, path, monkeypatch) -> iamraw.SectionList:
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    cmd = f'--pdf={pdf} -i {source} -o {path} -j8'
    run_sections(cmd, monkeypatch=monkeypatch)
    result = serializeraw.load_sections(str(path))
    return result

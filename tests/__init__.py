# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utilatest

import sections

run, fail = utilatest.create_cli_runner(sections)

utilatest.register_marker('huge')


def sections_from_dir(
    pdf: str,
    path,
    mp,
    pages: str = ':',
) -> iamraw.SectionList:
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    cmd = f'--pdf={pdf} -i {source} -o {path} -j8 --pages={pages} -VVV --profile'
    run(cmd, mp=mp)
    result = serializeraw.load_sections(str(path))
    return result

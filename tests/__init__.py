# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita
import hoverpower
import iamraw
import serializeraw
import utilotest

run, fail = utilotest.create_cli_runner(capita)

utilotest.register_marker('huge')


def sections_from_dir(
    pdf: str,
    path,
    mp,
    pages: str = ':',
) -> iamraw.SectionList:
    utilotest.fixture_requires(pdf)
    source = hoverpower.link(pdf)
    cmd = f'--pdf={pdf} -i {source} -o {path} -j8 --pages={pages} -VVV --profile'
    run(cmd, mp=mp)
    result = serializeraw.load_sections(str(path))
    return result

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilotest

import tests


@utilotest.nightly
def test_docinfo_lang(td, mp):
    pdf = hoverpower.DISS406_PDF
    utilotest.fixture_requires(pdf)
    source = hoverpower.link(pdf)
    cmd = f'-i {source} -o {td.tmpdir} --pages=0:10'
    tests.run(cmd, mp=mp)
    docinfo = serializeraw.load_docinfo(td.tmpdir)
    assert docinfo.lang == iamraw.Language.GERMAN

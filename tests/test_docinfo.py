# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utilatest

import tests


@utilatest.nightly
def test_docinfo_lang(testdir, monkeypatch):
    pdf = power.DISS406_PDF
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    command = f'-i {source} -o {testdir.tmpdir} --pages=0:10'
    tests.run_sections(command, monkeypatch=monkeypatch)
    docinfo = serializeraw.load_docinfo(testdir.tmpdir)
    assert docinfo.lang == iamraw.Language.GERMAN

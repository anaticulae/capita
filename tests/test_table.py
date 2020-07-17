# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import sections.path
import tests


def test_table_table_master98_page95(testdir, monkeypatch):
    source = power.link(power.MASTER098_PDF)
    tests.run_sections(
        f'-i {source} --tabletable --pages=95',
        monkeypatch=monkeypatch,
    )
    path = sections.path.tabletable(testdir.tmpdir)
    likelihood = serializeraw.load_likelihood(path)

    non_zero = [item.page for item in likelihood if item.content.value > 0.0]
    assert non_zero == [95]

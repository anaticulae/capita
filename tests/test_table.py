# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import sections
import tests


@utilotest.longrun
def test_table_table_master98_page95(td, mp):
    utilotest.fixture_requires(hoverpower.MASTER098_PDF)
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    tests.run(
        f'-i {source} --tabletable --pages=95',
        mp=mp,
    )
    path = sections.path.tabletable(td.tmpdir)
    likelihood = serializeraw.load_likelihood(path)

    non_zero = [item.page for item in likelihood if item.content.value > 0.0]
    assert non_zero == [95]

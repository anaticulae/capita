# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import sections
import tests


@utilatest.longrun
def test_table_table_master98_page95(td, mp):
    utilatest.fixture_requires(power.MASTER098_PDF)
    source = power.link(power.MASTER098_PDF)
    tests.run(
        f'-i {source} --tabletable --pages=95',
        mp=mp,
    )
    path = sections.path.tabletable(td.tmpdir)
    likelihood = serializeraw.load_likelihood(path)

    non_zero = [item.page for item in likelihood if item.content.value > 0.0]
    assert non_zero == [95]

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

import sections.geometry.column


def test_extract_columns_bachelor37_page33():
    source = power.link(power.BACHELOR037_PDF)
    ptn = serializeraw.create_pagetextnavigators_frompath(source, pages=(33,))
    ptn = ptn[0]
    parsed = sections.geometry.column.parse(ptn)

    # parse two columns
    assert len(parsed) == 2


def test_extract_columns_bachelor37_complete():
    source = power.link(power.BACHELOR037_PDF)
    ptns = serializeraw.create_pagetextnavigators_frompath(source)

    doubled = [
        page.page for page in ptns if sections.geometry.column.parse(page)
    ]

    # it is possible that more than required pages can be inside
    inside = [item in doubled for item in [33, 34, 35, 36]]
    assert all(inside), str(inside)

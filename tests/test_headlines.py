# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import sections.utils.headline

BACHELOR90 = power.link(power.BACHELOR090_PDF)


@pytest.mark.parametrize('source, page, expected', [
    (BACHELOR90, 2, 'Eidesstattliche Erklärung'),
    (BACHELOR90, 3, ['Kurzfassung', 'Abstract']),
    (BACHELOR90, 4, 'Inhaltsverzeichnis'),
])
def test_detect_page_headlines(source, page, expected):
    navigator = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=(page,),
    )
    extracted = sections.utils.headline.headlines(navigator[0])
    assert extracted == expected

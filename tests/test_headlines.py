# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import sections.utils.headline


# yapf:disable
@pytest.mark.parametrize('source, page, expected', [
    pytest.param(power.BACHELOR090_PDF, 2, 'Eidesstattliche Erklärung', id='eides'),
    pytest.param(power.BACHELOR090_PDF, 3, ['Kurzfassung', 'Abstract'], id='abstract'),
    pytest.param(power.BACHELOR090_PDF, 4, 'Inhaltsverzeichnis', id='toc'),
    pytest.param(power.MASTER148_PDF, 109, 'Literaturverzeichnis', id='bib'),
])
# yapf:enable
def test_detect_page_headlines(source, page, expected):
    utilatest.fixture_requires(source)
    source = power.link(source)
    navigator = serializeraw.ptn_frompath(
        source,
        pages=(page,),
    )
    extracted = sections.utils.headline.headlines(navigator[0])
    assert extracted == expected

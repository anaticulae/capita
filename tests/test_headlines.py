# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest

import capita.utils.headline


# yapf:disable
@pytest.mark.parametrize('source, page, expected', [
    pytest.param(hoverpower.BACHELOR090_PDF, 2, 'Eidesstattliche Erklärung', id='eides'),
    pytest.param(hoverpower.BACHELOR090_PDF, 3, ['Kurzfassung', 'Abstract'], id='abstract'),
    pytest.param(hoverpower.BACHELOR090_PDF, 4, 'Inhaltsverzeichnis', id='toc'),
    pytest.param(hoverpower.MASTER148_PDF, 109, 'Literaturverzeichnis', id='bib'),
])
# yapf:enable
def test_detect_page_headlines(source, page, expected):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    navigator = serializeraw.ptn_frompath(
        source,
        pages=(page,),
    )
    extracted = capita.utils.headline.headlines(navigator[0])
    assert extracted == expected

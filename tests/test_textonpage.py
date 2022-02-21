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
import utila
import utilatest

import sections.utils.text


def example(pages: tuple = None):
    utilatest.fixture_requires(power.BACHELOR037_PDF)
    loaded = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR037_PDF),
        pages=pages,
    )
    if len(loaded) == 1:
        return loaded[0]
    return loaded


@utilatest.longrun
def test_textonpage_page1():
    page1 = example((1,))
    result = sections.utils.text.textonpage(page1)
    assert len(result.words) >= 1
    assert len(result.signs) >= 1


def test_textonpage_descriptor_operation():
    data = sections.utils.text.TextOnPage()
    data.append_word('Hello')
    data.append_word('My')
    data.append_word('Friend')
    mean = data.words_mean
    assert utila.roundme(mean) == 4.33, mean
    assert data.words_max == 6
    assert data.words_min == 2


def test_textonpage_descriptor_key_error():
    data = sections.utils.text.TextOnPage()
    with pytest.raises(AttributeError):
        _ = data.mean_not_existing

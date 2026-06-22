# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita.feature.title
import capita.utils
import hoverpower
import iamraw
import iamraw.path
import pytest
import serializeraw
import utilo
import utilotest


def test_load_font_lookup(docu027_fontstore):
    first_font = docu027_fontstore.font(
        number=0,
        container=0,
        line=2,
        char=0,
    )
    assert first_font
    assert isinstance(first_font, iamraw.Font)


# qualitygate for further alogrithm improvements
TITLE_LIKELIHOOD_MIN = 0.70


# yapf:disable
@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.DOCU027_PDF, id='docu027'),
    pytest.param(hoverpower.DOCU007_PDF, id='docu007', marks=pytest.mark.xfail(reason='improve algo')),
])
# yapf:enable
def test_extract_title_likelihood(source):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    document = iamraw.path.text(source)
    fontheader = iamraw.path.fontheader(source)
    fontcontent = iamraw.path.fontcontent(source)

    document = serializeraw.load_document(document)
    fontstore = serializeraw.create_fontstore(fontheader, fontcontent)

    result = capita.feature.title.extract_title_likelihood(
        document,
        fontstore,
    )
    assert result[0].content.value >= TITLE_LIKELIHOOD_MIN
    # as a result of rounding the sum of the likelihoods is not one, but thats
    # not a big problem, hitting the region one is enough.
    result = [item.content.value for item in result]
    assert sum(result) == pytest.approx(1.0, abs=0.05)


def test_dump_and_load_likelhood(
    docu027_text,
    docu027_fontstore,
):
    result = capita.feature.title.extract_title_likelihood(
        docu027_text,
        docu027_fontstore,
    )
    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)

    assert loaded == result


def titlepage_likelihood(document: str) -> tuple:
    utilotest.fixture_requires(document)
    title = capita.feature.title.extract_titlelikelihood_frompath(
        hoverpower.link(document),
        pages=tuple(range(10)),
    )
    extracted = capita.utils.simple_content(title)
    return extracted


def test_extract_title_likelihood_master72():
    extracted = titlepage_likelihood(hoverpower.MASTER072_PDF)
    assert extracted[0] >= 0.95


def test_title_likelihood_master049():
    extracted = titlepage_likelihood(hoverpower.MASTER049_PDF)
    assert extracted[2] >= 0.80


@utilotest.longrun
def test_extract_title_likelihood_order107():
    extracted = titlepage_likelihood(
        hoverpower.ORDER107_PDF)  # TODO: CHANGE 107
    # assert extracted[0] >= 0.95
    assert utilo.iszero(extracted[2])

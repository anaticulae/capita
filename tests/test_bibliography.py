# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import sections.feature.bibliography
import sections.path
import tests


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_bibliography_work():
    source = power.link(power.MASTER072_PDF)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    expected = (
        (65, 0.5),
        (66, 0.5),
        (67, 0.5),
        (68, 0.5),
        (69, 0.5),
        (70, 0.5),
    )
    pages = [page for page, _ in expected]
    extracted = sections.feature.bibliography.work(
        text,
        textposition,
        pages=pages,
    )
    assert len(extracted) > 50, str(extracted)
    loaded = serializeraw.load_likelihood(extracted)
    # validate result
    for page, value in expected:
        selected = utila.select_page(loaded, page=page)
        current = selected.content.value
        assert current >= value, str(selected)


def extract_bibliography(source, testdir, monkeypatch):
    source = power.link(source)
    utilatest.fixture_requires(source)
    tests.run_sections(f'-i {source} --bibliography', monkeypatch=monkeypatch)
    # verify result
    path = sections.path.bibliography(testdir.tmpdir)
    likelihood = serializeraw.load_likelihood(path)
    pages = [item.page for item in likelihood if item.content.value > 0.0]
    return pages


@utilatest.longrun
def test_bibliography_ensure_connected_pages(testdir, monkeypatch):
    non_zero = extract_bibliography(power.MASTER098_PDF, testdir, monkeypatch)
    diff = utila.diffs(non_zero)
    # ensure to have only one ascending group with holes
    assert utila.isascending(diff, strict=False)
    assert max(diff) == 1, diff


# yapf:disable
@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR037_PDF, [33, 34, 35, 36], id='bachelor37'),
    pytest.param(power.BACHELOR128_PDF, [96, 97, 98, 99, 100, 101, 102, 103], id='bachelor128'),
    pytest.param(power.HOME018_PDF, [17], id='home18'),
    pytest.param(power.PAPER18_PDF, [15, 16, 17], id='paper18'),
    pytest.param(power.MASTER110_PDF, [104, 105, 106, 107, 108], id='master110'),
    pytest.param(power.BACHELOR090_PDF, [84, 85, 86, 87, 88], id='bachelor90'),
    pytest.param(power.DISS266_PDF, utila.ranged_list(214, 246), id='diss266'),
    pytest.param(power.DISS406_PDF, [], id='diss406'),
    # pytest.param(power.DISS406_PDF, utila.ranged_list(343, 406), id='diss406'),
])
# yapf:enable
@utilatest.longrun
def test_bibliography_x(source, expected, testdir, monkeypatch):
    pages = extract_bibliography(source, testdir, monkeypatch)
    assert pages == expected

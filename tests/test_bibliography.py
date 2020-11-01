# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw
import utila
import utilatest

import sections.path
import tests


@utilatest.skip_longrun
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

    for page, value in expected:
        selected = utila.select_page(loaded, page=page)
        current = selected.content.value
        assert current >= value, str(selected)


def extract_bibliography(source, testdir, monkeypatch):
    source = power.link(source)
    tests.run_sections(f'-i {source} --bibliography', monkeypatch=monkeypatch)

    path = sections.path.bibliography(testdir.tmpdir)
    likelihood = serializeraw.load_likelihood(path)
    pages = [item.page for item in likelihood if item.content.value > 0.0]
    return pages


@utilatest.skip_longrun
def test_bibliography_ensure_connected_pages(testdir, monkeypatch):
    non_zero = extract_bibliography(power.MASTER098_PDF, testdir, monkeypatch)
    diff = utila.diffs(non_zero)

    # ensure to have only one ascending group with holes
    assert utila.isascending(diff, strict=False)
    assert max(diff) == 1, diff


@utilatest.skip_longrun
def test_bibliography_bachelor37(testdir, monkeypatch):
    pages = extract_bibliography(power.BACHELOR037_PDF, testdir, monkeypatch)
    expected = [33, 34, 35, 36]
    assert pages == expected


def test_bibliography_paper18(testdir, monkeypatch):
    pages = extract_bibliography(power.PAPER18_PDF, testdir, monkeypatch)
    expected = [15, 16, 17]
    assert pages == expected


def test_bibliography_bachelor128(testdir, monkeypatch):
    pages = extract_bibliography(power.BACHELOR128_PDF, testdir, monkeypatch)
    expected = [96, 97, 98, 99, 100, 101, 102, 103]
    assert pages == expected


def test_bibliography_home018(testdir, monkeypatch):
    pages = extract_bibliography(power.HOME018_PDF, testdir, monkeypatch)
    expected = [
        17,
    ]
    assert pages == expected

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import serializeraw
import utila

import sections.feature.abbreviation
import sections.path
import tests
import tests.resources


def test_bibliography_work():
    source = tests.resources.MASTER72
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


def test_bibliography_ensure_connected_pages(testdir, monkeypatch):
    source = tests.resources.MASTER98
    tests.run_sections(f'-i {source} --bibliography', monkeypatch=monkeypatch)

    path = sections.path.bibliography(testdir.tmpdir)
    likelihood = serializeraw.load_likelihood(path)

    non_zero = [item.page for item in likelihood if item.content.value > 0.0]

    diff = utila.diffs(non_zero)

    # ensure to have only one ascending group with holes
    assert utila.isascending(diff), diff
    assert max(diff) == 1, diff

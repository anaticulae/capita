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
import tests.test_validate

ARCHIVE = utila.join(sections.ROOT, 'tests/expected/bibliography', exist=True)


@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_bibliography_work():
    source = power.link(power.MASTER072_PDF)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    footer = iamraw.path.groupme_headerfooters(source)
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
        footer=footer,
        pages=pages,
    )
    assert len(extracted) > 50, str(extracted)
    loaded = serializeraw.load_likelihood(extracted)
    # validate result
    for page, value in expected:
        selected = utila.select_page(loaded, page=page)
        current = selected.content.value
        assert current >= value, str(selected)


def extract_bibliography(source, pages, td, mp):
    source = power.link(source)
    utilatest.fixture_requires(source)
    tests.run_sections(
        f'-i {source} --bibliography --pages={pages} -VVV',
        mp=mp,
    )
    # verify result
    path = sections.path.bibliography(td.tmpdir)
    likelihood = serializeraw.load_likelihood(path)
    pages = [item.page for item in likelihood if item.content.value > 0.0]
    return pages


@utilatest.nightly
def test_bibliography_ensure_connected_pages(td, mp):
    non_zero = extract_bibliography(
        power.MASTER098_PDF,
        ':',
        td,
        mp,
    )
    diff = utila.diffs(non_zero)
    # ensure to have only one ascending group with holes
    assert utila.isascending(diff, strict=False)
    assert max(diff) == 1, diff


# pytest.param(power.DISS406_PDF, utila.rlist(343, 406), id='diss406'),
@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR037_PDF, [33, 34, 35, 36], id='bachelor037'),
    pytest.param(power.BACHELOR090_PDF, [84, 85, 86, 87, 88], id='bachelor090'),
    pytest.param(power.BACHELOR128_PDF, utila.rlist(96, 103), id='bachelor128'),
    pytest.param(power.BOOK173_PDF, [], id='book173', marks=pytest.mark.xfail),
    pytest.param(power.DISS266_PDF, utila.rlist(214, 246), id='diss266'),
    pytest.param(power.DISS406_PDF, [], id='diss406'),
    pytest.param(power.HOME018_PDF, [17], id='home018'),
    pytest.param(power.MASTER110_PDF, utila.rlist(104, 109), id='master110'),
    pytest.param(power.MASTER148_PDF, [109, 110, 111, 112], id='master148'),
    pytest.param(power.MASTER193_PDF, [188, 189, 190], id='master193'),
    pytest.param(power.PAPER018_PDF, [15, 16, 17], id='paper018'),
])
@utilatest.nightly
def test_bibliography_x(source, expected, td, mp):
    pages = extract_bibliography(source, ':', td, mp)
    assert pages == expected


@utilatest.nightly
@pytest.mark.parametrize('source, pages', [
    pytest.param(power.MASTER193_PDF, '124:130', id='master193'),
])
def test_nobib_x(source, pages, td, mp):
    detected = extract_bibliography(source, pages, td, mp)
    assert not detected


@utilatest.nightly
@pytest.mark.parametrize(
    'source',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
def test_validate_bibliography(source, td, mp):
    BibliographyValidate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class BibliographyValidate(tests.test_validate.Evaluate):

    def __init__(self, source, workdir, mp):
        super().__init__(
            step='bibliography',
            pages=':',
            source=source,
            mp=mp,
            workdir=workdir,
        )
        self.archive = ARCHIVE

    def load_sections(self, _):  # pylint:disable=W0613
        path = utila.join(
            self.workdir,
            'sections__bibliography_likelihood.yaml',
        )
        loaded = serializeraw.load_likelihood(path)
        return loaded

    def raw(self, value) -> str:
        pages = []
        for line in value:
            raw = f'{line.page}'.zfill(3) + ' ' + str(line.content.value)
            pages.append(raw)
        result = utila.NEWLINE.join(pages)
        return result

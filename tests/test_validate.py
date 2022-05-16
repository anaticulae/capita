# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import sections
import tests
import tests.conftest

ARCHIVE = utila.join(sections.ROOT, 'tests/expected', exist=True)

TODO = [
    item[0] if isinstance(item, tuple) else item
    for item in tests.conftest.RESOURCES
]
TODO = [pytest.param(item, id=utila.file_name(item)) for item in TODO]


@utilatest.nightly
@pytest.mark.parametrize('source', TODO)
def test_validate(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        expected=utila.file_name(source),
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            # step=f'pdf {source}',
            step='',
            program=functools.partial(
                tests.run_sections,
                monkeypatch=monkeypatch,
            ),
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_sections,
            convert_source=False,
            index=expected,
        )

    def load_sections(self, _):  # pylint:disable=W0613
        loaded = serializeraw.load_sections(self.workdir)
        return loaded

    def raw(self, value) -> str:
        result = []
        for section in value:
            line = rawline(section)
            result.append(line)
            for item in section:
                line = rawline(item)
                result.append('    ' + line)
        raw = utila.NEWLINE.join(result)
        return raw


def rawline(item) -> str:
    start = str(item.start).zfill(3)
    end = str(item.end).zfill(3)
    line = f'{start} {end} {item.__class__.__name__}'
    return line

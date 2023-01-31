# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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

ARCHIVE = utila.join(sections.ROOT, 'tests/expected/result', exist=True)


@utilatest.nightly
@pytest.mark.parametrize(
    'source',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
def test_validate(source, td, mp):
    utilatest.fixture_requires(source)
    Evaluate(
        step='',
        source=source,
        pages=':',
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, step, source, pages, workdir, mp):
        super().__init__(
            # step=f'pdf {source}',
            step=step,
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_sections,
            convert_source=False,
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

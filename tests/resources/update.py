# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import os

import detector.feature.titlepage
import utila

import sections
import tests.resources

WORKER = 12


def install_requirements():
    utila.clean_install(sections.ROOT, sections.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    if os.path.exists(tests.resources.GENERATED):
        return
    extract()


# yapf:disable
PACKAGE = [
    (tests.resources.BACHELOR37_PDF, tests.resources.BACHELOR37, '0:30'),
    (tests.resources.BACHELOR63_PDF, tests.resources.BACHELOR63, '0,1,2,3,4,5,6,7,8,59,60,61'),
    (tests.resources.HOWTO_ARGPARSE_PDF, tests.resources.HOWTO_ARGPARSE, None),
    (tests.resources.HOWTO_PYPORTING_PDF, tests.resources.HOWTO_PYPORTING, None),
    (tests.resources.MASTER72_PDF, tests.resources.MASTER72, None),
    (tests.resources.PYPORTING_PDF, tests.resources.PYPORTING, None),
    (tests.resources.RESTRUCT_PDF, tests.resources.RESTRUCT, None),
]
SINGLE = [
    (tests.resources.BACHELOR56_PDF, tests.resources.BACHELOR56, '0:55'),
    (tests.resources.MASTER116_PDF, tests.resources.MASTER116, '0,1,2,3,4,96,97,98,99,100'),
]
# yapf:enable


def run_package(pdf, outpath, pages=None, rungroupme: bool = True):
    utila.log(f'run: {pdf}')
    todo = [
        rawmaker(pdf, outpath, pages),
        oneline(pdf, outpath, pages),
    ]
    utila.run_parallel(todo)
    if rungroupme:
        utila.run(groupme(outpath, pages=pages))
    utila.log(f'completed: {pdf}')
    return pdf


def extract():
    for pdf, _, __ in PACKAGE:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), pdf

    # ensure that generation directory exists
    os.makedirs(tests.resources.GENERATED)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures_standard = {
            executor.submit(
                run_package,
                pdf,
                out,
                pages=pages,
            ): pdf for pdf, out, pages in PACKAGE
        }
        futures_singles = {
            executor.submit(
                run_package,
                pdf,
                out,
                pages=pages,
                rungroupme=False,
            ): pdf for pdf, out, pages in SINGLE
        }
        futures = {}
        futures.update(futures_standard)
        futures.update(futures_singles)
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.log(comment)
            except Exception:
                utila.error(f'{future} failed.')
                raise


def rawmaker(inpath: str, outpath: str, pages: tuple = None) -> str:
    pages = f' --pages {pages} ' if pages is not None else ' '
    config = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '
    cmd = f'rawmaker -i {inpath} -o {outpath} {pages} {config} -j8'
    cmd += f' && linero -i {outpath} -o {outpath}'
    return cmd


def oneline(inpath: str, outpath: str, pages: tuple = None) -> str:
    pages = f' --pages {pages} ' if pages is not None else ' '
    config = detector.feature.titlepage.RAWMAKER_CONFIGURATION
    cmd = f'rawmaker -i {inpath} -o {outpath} {pages} {config} -j8'
    return cmd


def groupme(inpath: str, pages: tuple = None) -> str:
    pages = f' --pages {pages} ' if pages is not None else ' '
    cmd = f'groupme -i {inpath} -o {inpath} {pages} -j8'
    return cmd

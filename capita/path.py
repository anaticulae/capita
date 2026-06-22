# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita
import utilo


def result(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'section_result',
        prefix,
    )


# TODO: REMOVE LATER
sections_ = result  # pylint:disable=C0103


def abbreviation(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'abbreviation_likelihood',
        prefix,
    )


def abstract(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'abstract_likelihood',
        prefix,
    )


def acknowledge(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'acknowledge_likelihood',
        prefix,
    )


def appendix(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'appendix_likelihood',
        prefix,
    )


def bibliography(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        'sections_ref',
        'bibliography_likelihood',
        prefix,
    )


def chapter(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'chapter_likelihood',
        prefix,
    )


def index(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'index_likelihood',
        prefix,
    )


def legal(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'legal_likelihood',
        prefix,
    )


def title(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'title_likelihood',
        prefix,
    )


def toc(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'toc_likelihood',
        prefix,
    )


def tabletable(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'tabletable_likelihood',
        prefix,
    )


def symboltable(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'symboltable_likelihood',
        prefix,
    )


def figuretable(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'figuretable_likelihood',
        prefix,
    )


def whitepage(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'whitepage_likelihood',
        prefix,
    )


def paper(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        capita.PROCESS,
        'paper_likelihood',
        prefix,
    )

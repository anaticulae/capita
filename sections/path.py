# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import sections


def result(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'section_result',
        prefix,
    )


# TODO: REMOVE LATER
sections_ = result  # pylint:disable=C0103


def abbreviation(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'abbreviation_likelihood',
        prefix,
    )


def abstract(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'abstract_likelihood',
        prefix,
    )


def appendix(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'appendix_likelihood',
        prefix,
    )


def bibliography(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'bibliography_likelihood',
        prefix,
    )


def chapter(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'chapter_likelihood',
        prefix,
    )


def index(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'index_likelihood',
        prefix,
    )


def legal(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'legal_likelihood',
        prefix,
    )


def title(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'title_likelihood',
        prefix,
    )


def toc(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'toc_likelihood',
        prefix,
    )


def tabletable(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'tabletable_likelihood',
        prefix,
    )


def symboltable(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'symboltable_likelihood',
        prefix,
    )


def figuretable(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'figuretable_likelihood',
        prefix,
    )


def whitepage(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'whitepage_likelihood',
        prefix,
    )

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila


def create(sections: iamraw.Sections):
    result = []
    for group in sections:
        result.append(create_group(group))
    return result


def simplify_group(group):
    result = [group.content[0]]
    for item in group.content[1:]:
        if not isinstance(item, result[-1].__class__):
            result.append(item)
        else:
            result[-1].end = item.end
    return result


def create_group(group):
    result = []
    merged = simplify_group(group)
    for item in merged:
        try:
            mapper = MAPPING[item.__class__]
        except KeyError:
            utila.error(f'could not group {item.__class__}')
            continue
        result.append(mapper(item))
    return result


def create_toc(item):
    result = []
    page = pages(item.start, item.end)
    inout = '-i {RAWMAKER_TOC} -o {GROUPME_RESULT}'
    result.append(f'groupme --toc {page} {inout}')
    return result


def create_titlepage(item):
    result = []
    page = pages(item.start, item.end)
    inout = '-i {RAWMAKER_TITLE} -o {DETECTOR_RESULT}'
    result.append(f'detector --titlepage {page} {inout}')
    return result


def create_bibliography(bibliography):
    result = []
    page = pages(bibliography.start, bibliography.end)
    inout = '-i {RAWMAKER_BIBLIOGRAPHY} -o {DETECTOR_RESULT}'
    result.append(f'detector --bibliography {page} {inout}')
    return result


def pages(start: int, end: int):
    assert 0 <= start <= end, f'{start} <= {end}'
    if start == end:
        return f'--pages={start}'
    return f'--pages={start}:{end}'


MAPPING = {
    iamraw.sections.TitlePage: create_titlepage,
    iamraw.sections.Bibliography: create_bibliography,
    iamraw.sections.TableOfContent: create_toc,
}

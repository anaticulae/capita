# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import copy

import iamraw
import utila


def create(sections: iamraw.Sections):
    result = []
    for group in sections:
        result.extend(create_group(group))
    return result


def create_group(group):
    result = []
    merged = simplify(group)
    for item in merged:
        try:
            mapper = MAPPING[item.__class__]
        except KeyError:
            utila.error(f'could not group: {item.__class__}')
            continue
        groupname = mapper.__name__.split('_', maxsplit=1)[1]
        result.append(groupname)
        mapped = mapper(item)
        result.append(mapped)
    return result


def simplify(group):
    result = [copy.deepcopy(group.content[0])]
    for item in group.content[1:]:
        merge = should_merge(result[-1], item)
        if merge:
            result[-1].end = item.end
        elif not isinstance(item, result[-1].__class__):
            result.append(copy.deepcopy(item))
        else:
            result[-1].end = item.end
    return result


def should_merge(parent, current):
    merger = {
        iamraw.sections.Text: (iamraw.sections.Chapter,),
        iamraw.sections.Chapter: (iamraw.sections.Text,),
    }
    with contextlib.suppress(KeyError):
        if current.__class__ in merger[parent.__class__]:
            return True
    return False


def rawmaker(name, page):
    cmd = 'rawmaker -i {SOURCE} -o {RAWMAKER_%s} -c {RAWMAKER_CFG_%s} %s'
    cmd = cmd % (name.upper(), name.upper(), page)
    return cmd


def create_toc(item):
    result = []
    page = pages(item.start, item.end)
    result.append(rawmaker('toc', page))
    inout = '-i {RAWMAKER_TOC} -o {GROUPME_RESULT}'
    result.append(f'groupme --toc {page} {inout}')
    return result


def create_titlepage(item):
    result = []
    page = pages(item.start, item.end)
    result.append(rawmaker('title', page))
    inout = '-i {RAWMAKER_TITLE} -o {DETECTOR_RESULT}'
    result.append(f'detector --titlepage {page} {inout}')
    return result


def create_bibliography(bibliography):
    result = []
    page = pages(bibliography.start, bibliography.end)
    result.append(rawmaker('bibliography', page))
    inout = '-i {RAWMAKER_BIBLIOGRAPHY} -o {DETECTOR_RESULT}'
    result.append(f'detector --bibliography {page} {inout}')
    return result


def create_text(text):
    """Chapter and Text."""
    result = []
    page = pages(text.start, text.end)
    result.append(rawmaker('words', page))
    inout = '-i {RAWMAKER_WORDS} -o {WORDS_RESULT}'
    result.append(f'words {page} {inout}')
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
    iamraw.sections.Text: create_text,
    iamraw.sections.Chapter: create_text,
}

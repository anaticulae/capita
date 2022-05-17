# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import copy
import typing

import configo
import iamraw
import iamraw.sections
import utila

import sections.section.after
import sections.section.ctor

# features with lower trust are not expected as detected feature
FEATURE_TRUST_MIN = configo.HV_PERCENT_PLUS(default=40)

# more than one feature have this trust, accept all of them
MULTIPLE_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=75)


def extract_sections(loaded: 'SectionsRequiredResources') -> iamraw.Sections:
    """Decide which `DocumentSection` is selected of the different
    feature extractor.

    If more than one feature suits very well, split page in different
    regions.

    Args:
        loaded: result of different `sections` steps
    Returns:
        `Sections` definition for given pages
    """
    collected = {}
    for pagenumber, content in loaded.sync():
        trusted = most_trusted_items(content)
        if not trusted:
            # if trust is to low, the feature is not charactaristical enough,
            # therefore the page is treated as a normal text page
            collected[pagenumber] = iamraw.sections.Text(
                start=pagenumber,
                end=pagenumber,
                trust=1.0,
            )
            continue
        if morethan_one(trusted):
            multiple = create_multisection(trusted, pagenumber, content)
            collected[pagenumber] = multiple
        else:
            item = trusted[0]
            new = sections.section.ctor.create(
                start=pagenumber,
                end=pagenumber,
                trust=item.content.value,
                typ=content.index(item),
            )
            collected[pagenumber] = new
    collected = clean_collection(collected)
    grouped = group_sections(collected)
    result = verify_sections(grouped)
    return result


def morethan_one(trusted) -> bool:
    if not trusted or len(trusted) == 1:
        return False
    if len(trusted) == 2:
        names = [item.content.name for item in trusted]
        # in the current state, we are not able to distinguish between
        # symbol table and abbr table. This is not necessary for our job
        # here.
        if 'abbreviation_table' in names and 'symboltable' in names:
            # TODO: REMOVE LATER
            return False
    return True


def create_multisection(trusted, pagenumber, content):
    multiple = iamraw.MultipleSection(
        start=pagenumber,
        end=pagenumber,
        trust=1.0,
    )
    for index, item in enumerate(trusted):
        # TODO: Preseve order on page
        start = pagenumber + index * 1 / len(trusted)
        end = pagenumber + (index + 1) * 1 / len(trusted)
        start, end = utila.roundme(start, end)
        new = sections.section.ctor.create(
            start=start,
            end=end,
            trust=item.content.value,
            typ=content.index(item),
        )
        multiple.content.append(new)  # pylint:disable=E1101
    return multiple


def most_trusted_items(items: iamraw.PageContentLikelihoods) -> list:
    """Extract most trusted items on a page.

    There are multiple items possible.

    Accepted features must have a higher trust than `FEATURE_TRUST_MIN `.
    Multiple features on a page require a much higher trust
    `MULTIPLE_FEATURE_TRUST`.

    Args:
        items: detected items on a page
    Returns:
        sorted list of accepted features, max trust stands on the top
    """
    items = sorted(
        items,
        key=lambda x: x.content.value if x and x.content else 0.0,
        reverse=True,
    )
    # remove features with to low trust
    items = [
        item for item in items
        if item and item.content and item.content.value >= FEATURE_TRUST_MIN
    ]
    # more than one feature on a page
    if len(items) > 1:
        for item in items:
            # do not return MultiplePart, use Paper instead
            if item.content.name == 'paper':
                return [item]
        # filter multiple sections result
        multiple = [
            item for item in items if item and item.content and
            item.content.value >= MULTIPLE_FEATURE_TRUST
        ]
        # TODO: SEARCH FOR A BETTER APROACH, NEED MORE INFORMATION
        # THIS ASSERT SEAMS NOT TO BE USEFUL
        # assert len(multiple) >= 1, str(items)
        if multiple:
            items = multiple
    return items


def verify_sections(sectionx: iamraw.Sections) -> iamraw.Sections:
    """Merge sections to improve DocumentSection detection."""
    result = iamraw.Sections()
    # avoid side effects
    todo = [copy.deepcopy(item) for item in sectionx.content]
    if not todo:
        return result
    length = todo[-1].end
    result.append(todo[0])
    # STEP 1: MERGE INVALID SECTION TO SECTION BEFORE
    for current in todo[1:]:
        if valid_section(current, document_length=length):
            result.append(current)
            continue
        # merge content to section before
        before = result[-1]
        before.end = current.end
        before.content.extend(current.content)
    # STEP 2: UNITE EQUAL SECTIONS
    todo = list(result.content[1:])
    result.content = [result.content[0]]
    for current in todo:
        before = result[-1]
        if current.__class__ != before.__class__:
            result.append(current)
            continue
        # merge equal classes to section before
        before.end = current.end
        before.content.extend(current.content)
    return result


def clean_collection(collected: dict) -> dict:
    """Do not detect MainPart before Toc."""
    tocrange = type_range(collected.items(), iamraw.sections.TableOfContent)
    if not tocrange:
        return collected
    for page, content in collected.items():
        if isinstance(content, iamraw.sections.Chapter):
            if page < tocrange[0][0]:
                # Chapter starts before TOC, ignore chapter detection to
                # have MainPart after TOC.
                collected[page] = iamraw.sections.Text(
                    start=page,
                    end=page,
                    trust=1.0,
                )
    return collected


def valid_section(
    section: iamraw.DocumentSection,
    document_length: int,
) -> bool:
    if document_length < 20:
        # disable check for small documents
        return True
    if isinstance(section, iamraw.MainPart):
        # TODO: IMPROVE THIS CHECK
        if len(section) < 10:
            return False
    return True


def is_new_area(current, next_):
    current_class = current.__class__
    next_class = next_ if callable(next_) else next_.__class__
    return current_class != next_class


AreaItems = typing.List[iamraw.sections.AreaItem]


def group_sections(items: AreaItems) -> iamraw.Sections:
    """Extend ranges of `AreaItems` to avoid empty regions between `AreaItems`.

    A empty region can be created if you have the titlepage and after
    this a blank page before continuing with table of content.
    """
    result = iamraw.Sections()
    current = None
    chapter = 1
    for page, item in items.items():
        next_ = sections.section.after.determine_document_section(
            current,
            item,
        )
        if not current and isinstance(item, iamraw.MultipleSection):
            # Multiple section on the start of the document
            # TODO: HOW TO HANDLE MULTIPLE SECTION IN THE MIDDLE OF THE DOCUMENT?
            current = item
            result.content.append(item)  # pylint:disable=E1101
            continue
        if is_new_area(current, next_):
            # `page + 1` cause of python style index pattern
            current = next_(start=page, end=page + 1, trust=1.0)
            result.content.append(current)  # pylint:disable=E1101
        else:
            # increase section end
            # `page + 1` cause of python style index pattern
            current.end = page + 1
        if isinstance(item, iamraw.sections.Chapter):
            # set chapter level
            item.number = chapter
            chapter += 1
        current.content.append(item)
    return result


def glossary_path(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'glossary_likelihood',
        prefix,
    )


def type_range(sectionx, typ):
    pages = []
    for section in sectionx:
        if isinstance(section, typ):
            pages.append(section.start)
            pages.append(section.end)
            continue
        for page in section:
            if isinstance(page, typ):
                pages.append(page.start)
    if not pages:
        return None
    pages = sorted(pages)
    grouped = utila.groupby_diff(pages)
    grouped = [(group[0], group[-1]) for group in grouped]
    return grouped

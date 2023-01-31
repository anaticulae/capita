# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import iamraw.sections
import utila

import sections.section.ctor
import sections.section.improve

# features with lower trust are not expected as detected feature
FEATURE_TRUST_MIN = configo.HV_PERCENT_PLUS(default=40)

# more than one feature have this trust, accept all of them
MULTIPLE_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=75)


def run(loaded: 'SectionsRequiredResources') -> iamraw.Sections:
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
            # if trust is too low, the feature is not characteristic
            # enough, therefore the page is treated as a normal text page
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
    result = sections.section.improve.improve(collected)
    return result


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
            # TODO: WHAT IF NOTHING IS LEFT IN MULTIPLE?
    return items


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

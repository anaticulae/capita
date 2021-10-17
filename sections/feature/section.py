# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import copy
import dataclasses
import functools
import inspect
import typing

import configo
import iamraw
import iamraw.likelihood
import iamraw.sections
import serializeraw
import utila

import sections.path

# features with lower trust are not expected as detected feature
FEATURE_TRUST_MIN = configo.HV_PERCENT_PLUS(default=40).value

# more than one feature have this trust, accept all of them
MULTIPLE_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=75).value


@utila.checkdatatype
def work(  # pylint:disable=R0913,R0914,W0613
    abbreviation: str,
    abstract: str,
    acknowledge: str,
    appendix: str,
    bibliography: str,
    chapter: str,
    figuretable: str,
    index: str,
    legal: str,
    paper: str,
    symboltable: str,
    tabletable: str,
    title: str,
    toc: str,
    whitepage: str,
    glossary: str,
    pages: tuple = None,
) -> str:
    """Combine different featuretypes to determine the page type with
    most confidence. Returns dumped `Section`."""
    loaded = load_features(**locals())
    # work
    extracted = extract_sections(loaded)
    # save
    dumped = serializeraw.dump_sections(extracted)
    return dumped


@dataclasses.dataclass
class SectionsRequiredResources:
    abbreviation: iamraw.PageContentLikelihoods
    abstract: iamraw.PageContentLikelihoods
    acknowledge: iamraw.PageContentLikelihoods
    appendix: iamraw.PageContentLikelihoods
    bibliography: iamraw.PageContentLikelihoods
    chapter: iamraw.PageContentLikelihoods
    figuretable: iamraw.PageContentLikelihoods
    index: iamraw.PageContentLikelihoods
    legal: iamraw.PageContentLikelihoods
    paper: iamraw.PageContentLikelihoods
    symboltable: iamraw.PageContentLikelihoods
    tabletable: iamraw.PageContentLikelihoods
    title: iamraw.PageContentLikelihoods
    toc: iamraw.PageContentLikelihoods
    whitepage: typing.List[iamraw.sections.WhitePage]
    glossary: iamraw.PageContentLikelihoods


def extract_sections(loaded: SectionsRequiredResources) -> iamraw.Sections:
    """Decide which `DocumentSection` is selected of the different
    feature extractor. If more than one feature suits very well, split
    page in different regions.

    Args:
        loaded: result of different `sections` steps
    Returns:
        `Sections` definition for given pages
    """
    collected = {}
    for pagenumber, content in utila.sync_pages([
            loaded.abbreviation,
            loaded.abstract,
            loaded.acknowledge,
            loaded.appendix,
            loaded.bibliography,
            loaded.chapter,
            loaded.figuretable,
            loaded.index,
            loaded.legal,
            loaded.paper,
            loaded.symboltable,
            loaded.tabletable,
            loaded.title,
            loaded.toc,
            loaded.whitepage,
            loaded.glossary,
    ]):
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
        if len(trusted) > 1:
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
                new = create(
                    start=start,
                    end=end,
                    trust=item.content.value,
                    typ=content.index(item),
                )
                multiple.content.append(new)  # pylint:disable=E1101
            collected[pagenumber] = multiple
        else:
            item = trusted[0]
            new = create(
                start=pagenumber,
                end=pagenumber,
                trust=item.content.value,
                typ=content.index(item),
            )
            collected[pagenumber] = new
    grouped = group_sections(collected)
    result = verify_sections(grouped)
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
    """Extend ranges of `AreaItems` to avoid empty regions between
    `AreaItems`. A empty region can be created if you have the titlepage
    and after this a blank page before continuing with table of content.
    """
    result = iamraw.Sections()
    current = None
    chapter = 1
    for page, item in items.items():
        next_ = determine_document_section(current, item)
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


# THE ORDER IS IMPORTANT!
BUILDER = [
    iamraw.sections.AbbreviationTable,
    iamraw.sections.Abstract,
    iamraw.sections.Acknowledgments,
    iamraw.sections.Appendix,
    iamraw.sections.Bibliography,
    iamraw.sections.Chapter,
    iamraw.sections.FigureTable,
    iamraw.sections.Index,
    iamraw.sections.LegalInformation,
    iamraw.sections.CiteContent,
    iamraw.sections.SymbolTable,
    iamraw.sections.TableTable,
    iamraw.sections.TitlePage,
    iamraw.sections.TableOfContent,
    iamraw.sections.WhitePage,
    iamraw.sections.Glossary,
]
assert BUILDER.index(iamraw.sections.TableOfContent) > BUILDER.index(
    iamraw.sections.TitlePage), 'do not sort BUILDER'


def create(start, end, trust, typ):
    ctor = BUILDER[typ]
    new = ctor(start=start, end=end, trust=trust)
    return new


def multiplesection_next(multiple):
    if utila.select_type(multiple.content, iamraw.sections.Bibliography):
        return iamraw.sections.Appendix
    return iamraw.MultipleSection


# do not change DocumentSection
# iamraw.sections.DocumentSection
#       iamraw.sections.Text
#       iamraw.sections.WhitePage:
# yapf:disable
MATCHING = {
    iamraw.sections.Abstract: [  # pylint:disable=E1101
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Acknowledgments: [
        iamraw.sections.Introduction,
        iamraw.sections.Appendix,
    ],
    iamraw.sections.Appendix: iamraw.sections.Appendix,
    iamraw.MultipleSection: multiplesection_next,
    iamraw.sections.AbbreviationTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Bibliography: iamraw.sections.Appendix,
    iamraw.sections.Chapter: iamraw.MainPart,
    iamraw.sections.FigureTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Index: iamraw.sections.Table,
    iamraw.sections.LegalInformation: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.TableOfContent: [
        iamraw.sections.Introduction,
        iamraw.sections.Table,
    ],
    iamraw.sections.SymbolTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.TableTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Glossary: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.CiteContent: iamraw.sections.CitePart,
    iamraw.sections.CitePart: iamraw.sections.CitePart,
    iamraw.sections.Text: iamraw.sections.DocumentSection,
    iamraw.sections.TitlePage: iamraw.sections.Introduction,
    iamraw.sections.WhitePage: iamraw.sections.DocumentSection,
}
# yapf:enable


def determine_document_section(
    current: iamraw.sections.DocumentSection,
    after: iamraw.sections.AreaItem,
):
    """It is not always required to change the `current`
    DocumentSection. We require only few DocumentSection, therefore in
    some cases more than one possible parent is defined."""
    nextclass = MATCHING[type(after)]
    if inspect.isfunction(nextclass):
        # dynamic next section determiner
        nextclass = nextclass(after)
        return nextclass

    if isinstance(current, iamraw.sections.MainPart):
        changer = (
            iamraw.sections.AbbreviationTable,
            iamraw.sections.FigureTable,
            iamraw.sections.Glossary,
            iamraw.sections.SymbolTable,
            iamraw.sections.TableTable,
        )
        if isinstance(after, changer):
            # TODO: HACK?
            return iamraw.sections.Appendix

    new_section = nextclass == iamraw.sections.DocumentSection
    use_current = (isinstance(nextclass, list) and
                   not any(item == current for item in nextclass))

    if new_section or use_current:
        if not current:
            return iamraw.sections.Unknown
        return current
    return nextclass


@functools.lru_cache(configo.CACHE_SMALL)
def load_features(  # pylint:disable=R0913,R0914
    abbreviation: str,
    abstract: str,
    acknowledge: str,
    appendix: str,
    bibliography: str,
    chapter: str,
    figuretable: str,
    index: str,
    legal: str,
    paper: str,
    symboltable: str,
    tabletable: str,
    title: str,
    toc: str,
    whitepage: str,
    glossary: str,
    pages: tuple = None,
) -> SectionsRequiredResources:
    abbreviation = serializeraw.load_likelihood(abbreviation, pages=pages)
    abstract = serializeraw.load_likelihood(abstract, pages=pages)
    appendix = serializeraw.load_likelihood(appendix, pages=pages)
    acknowledge = serializeraw.load_likelihood(acknowledge, pages=pages)
    bibliography = serializeraw.load_likelihood(bibliography, pages=pages)
    chapter = serializeraw.load_likelihood(chapter, pages=pages)
    figuretable = serializeraw.load_likelihood(figuretable, pages=pages)
    index = serializeraw.load_likelihood(index, pages=pages)
    legal = serializeraw.load_likelihood(legal, pages=pages)
    paper = serializeraw.load_likelihood(paper, pages=pages)
    symboltable = serializeraw.load_likelihood(symboltable, pages=pages)
    tabletable = serializeraw.load_likelihood(tabletable, pages=pages)
    title = serializeraw.load_likelihood(title, pages=pages)
    toc = serializeraw.load_likelihood(toc, pages=pages)
    white = serializeraw.load_whitepages(whitepage, pages=pages)
    glossary = serializeraw.load_likelihood(glossary, pages=pages)
    # prepare result
    result = SectionsRequiredResources(
        abbreviation=abbreviation,
        abstract=abstract,
        acknowledge=acknowledge,
        appendix=appendix,
        bibliography=bibliography,
        chapter=chapter,
        figuretable=figuretable,
        index=index,
        legal=legal,
        paper=paper,
        symboltable=symboltable,
        tabletable=tabletable,
        title=title,
        toc=toc,
        whitepage=white,
        glossary=glossary,
    )
    return result


def chapters(root: iamraw.Sections):
    content = [item for item in root if isinstance(item, iamraw.MainPart)]
    if not content:
        # no content in document
        return []
    result = []
    for area in content:
        for chapter in area:
            result.append((chapter.start, chapter.end))
    return result


def load_section_likelihood_frompath(path: str, pages: tuple = None):
    # TODO: we need to improve this
    loaded = load_features(
        sections.path.abbreviation(path),
        sections.path.abstract(path),
        sections.path.appendix(path),
        sections.path.acknowledge(path),
        sections.path.bibliography(path),
        sections.path.chapter(path),
        sections.path.figuretable(path),
        sections.path.index(path),
        sections.path.legal(path),
        sections.path.paper(path),
        sections.path.symboltable(path),
        sections.path.tabletable(path),
        sections.path.title(path),
        sections.path.toc(path),
        sections.path.whitepage(path),
        glossary_path(path),
        pages=pages,
    )
    result = extract_sections(loaded)
    return result


def glossary_path(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        sections.PROCESS,
        'glossary_likelihood',
        prefix,
    )

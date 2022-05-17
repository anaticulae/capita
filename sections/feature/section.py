# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import sections.section.load
import sections.section.run


@utila.checkdatatype
def work(  # pylint:disable=R0913,R0914,W0613
    xabbreviation: str,
    xabstract: str,
    xacknowledge: str,
    xappendix: str,
    xbibliography: str,
    xchapter: str,
    xfiguretable: str,
    xindex: str,
    xlegal: str,
    xpaper: str,
    xsymboltable: str,
    xtabletable: str,
    xtitle: str,
    xtoc: str,
    xwhitepage: str,
    xglossary: str,
    pages: tuple = None,
) -> str:
    """Combine different featuretypes to determine the page type with
    most confidence.

    Returns dumped `Section`.
    """
    loaded = sections.section.load.load_features(**locals())
    # work
    extracted = sections.section.run.run(loaded)
    # save
    dumped = serializeraw.dump_sections(extracted)
    return dumped

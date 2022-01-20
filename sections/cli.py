#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from sections import PROCESS
from sections import ROOT
from sections import __version__

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

ResultFile = lambda producer, name: RF(producer=producer, name=name)  # pylint:disable=C0103

WORKPLAN = [
    step(
        'abbreviation',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'abstract',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('groupme', 'footer_footerheader'),
            utila.File(name='pdfinfo', optional=True),
        ],
        output=('likelihood',),
    ),
    step(
        'acknowledge',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'appendix',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'bibliography',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'figuretable',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    step(
        'glossary',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'index',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood',),
    ),
    step(
        'legal',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'symboltable',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    step(
        'tabletable',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    step(
        'title',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
        ],
        output=('likelihood',),
    ),
    step(
        'toc',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    step(
        'whitepage',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('groupme', 'footer_footerheader'),
            utila.Directory('rawmaker__images_images'),
            utila.Directory('rawmaker__figures_figures'),
        ],
        output=('likelihood',),
    ),
    step(
        'chapter',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('groupme', 'footer_footerheader'),
            ResultFile('rawmaker', 'outlines_outlines'),
        ],
        output=('likelihood',),
    ),
    step(
        'paper',
        inputs=[
            utila.Value('pdf', typ=None, defaultvar=None),
        ],
        output=('likelihood',),
    ),
    step(
        'section',
        inputs=[
            ResultFile('sections', 'abbreviation_likelihood'),
            ResultFile('sections', 'abstract_likelihood'),
            ResultFile('sections', 'acknowledge_likelihood'),
            ResultFile('sections', 'appendix_likelihood'),
            ResultFile('sections', 'bibliography_likelihood'),
            ResultFile('sections', 'chapter_likelihood'),
            ResultFile('sections', 'figuretable_likelihood'),
            ResultFile('sections', 'index_likelihood'),
            ResultFile('sections', 'legal_likelihood'),
            ResultFile('sections', 'paper_likelihood'),
            ResultFile('sections', 'symboltable_likelihood'),
            ResultFile('sections', 'tabletable_likelihood'),
            ResultFile('sections', 'title_likelihood'),
            ResultFile('sections', 'toc_likelihood'),
            ResultFile('sections', 'whitepage_likelihood'),
            ResultFile('sections', 'glossary_likelihood'),
        ],
        output=('result',),
    ),
    step(
        'docinfo',
        inputs=[
            ResultFile('sections', 'section_result'),
            ResultFile('rawmaker', 'text_text'),
            utila.File(name='pdfinfo', optional=True),
        ],
        output=('docinfo',),
    ),
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='sections.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            profileflag=True,
            version=__version__,
        ),
    )

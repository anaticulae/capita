#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import sections

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

WORKPLAN = [
    utila.create_step(
        'abbreviation',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'abstract',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.File(name='pdfinfo', optional=True),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'acknowledge',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'appendix',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'bibliography',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'figuretable',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'glossary',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.File(name='pdfinfo', optional=True),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'index',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'legal',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'symboltable',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'tabletable',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'title',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'toc',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'whitepage',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.Directory('rawmaker__images_images'),
            utila.Directory('rawmaker__figures_figures'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'chapter',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'outlines_outlines'),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'paper',
        inputs=[
            utila.Value('pdf', typ=None, defaultvar=None),
        ],
        output=('likelihood',),
    ),
    utila.create_step(
        'section',
        inputs=[
            utila.ResultFile('sections', 'abbreviation_likelihood'),
            utila.ResultFile('sections', 'abstract_likelihood'),
            utila.ResultFile('sections', 'acknowledge_likelihood'),
            utila.ResultFile('sections', 'appendix_likelihood'),
            utila.ResultFile('sections', 'bibliography_likelihood'),
            utila.ResultFile('sections', 'chapter_likelihood'),
            utila.ResultFile('sections', 'figuretable_likelihood'),
            utila.ResultFile('sections', 'index_likelihood'),
            utila.ResultFile('sections', 'legal_likelihood'),
            utila.ResultFile('sections', 'paper_likelihood'),
            utila.ResultFile('sections', 'symboltable_likelihood'),
            utila.ResultFile('sections', 'tabletable_likelihood'),
            utila.ResultFile('sections', 'title_likelihood'),
            utila.ResultFile('sections', 'toc_likelihood'),
            utila.ResultFile('sections', 'whitepage_likelihood'),
            utila.ResultFile('sections', 'glossary_likelihood'),
        ],
        output=('result',),
    ),
    utila.create_step(
        'docinfo',
        inputs=[
            utila.ResultFile('sections', 'section_result'),
            utila.ResultFile('rawmaker', 'text_text'),
            utila.File(name='pdfinfo', optional=True),
        ],
        output=('docinfo',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=sections.ROOT,
        featurepackage='sections.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=sections.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            profileflag=True,
            version=sections.__version__,
        ),
    )

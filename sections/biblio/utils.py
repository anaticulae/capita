# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def ascending_page_groups(items):
    # TODO: MOVE TO UTILA
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        if item.page - result[-1][-1].page == 1:
            result[-1].append(item)
        else:
            result.append([item])
    return result


def cluster_bibpages(items):
    """Select hugest(max sum likelihood value) group."""
    grouped = ascending_page_groups(items)
    if not grouped:
        return []
    hugest = sorted(
        grouped, key=lambda x: sum(item.content.value for item in x))
    hugest = hugest[-1]

    avg = sum([item.content.value for item in hugest]) / len(hugest)
    for item in hugest:
        # every item of the group should have the same likelihood
        item.content.value = utila.roundme(avg)
    return hugest

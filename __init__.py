import anki.stats
from anki.hooks import wrap

from .graph import progress_graphs

anki.stats.CollectionStats.easeGraph = \
    wrap(anki.stats.CollectionStats.easeGraph, progress_graphs, pos="")

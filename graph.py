from collections import Counter

from . import flot_tickrotor
from .stats import get_stats

colYoung = "#7c7"
colMature = "#070"
colLearn = "#00F"
colUnseen = "#000"
colSusp = "#ff0"


def progress_graphs(self, _old):
    result = _old(self)

    model = self.col.models.byName('Bible Verse')
    model_id = model['id'] if model else None

    if model_id is None:
        return result

    ot_book_stats, nt_book_stats = get_stats(self.col.db, model_id, self._limit())
    ot_stats = sum((s[1] for s in ot_book_stats), Counter())
    nt_stats = sum((s[1] for s in nt_book_stats), Counter())

    stats = list(filter(lambda book_stats: (book_stats[1] is None or
                                            book_stats[1].get('mature_count', 0) > 0 or
                                            book_stats[1].get('young_count', 0) > 0),
                        ot_book_stats + [('', None)] + nt_book_stats))

    def get_data(key):
        return [(i, s[1].get(key, 0)) for i, s in enumerate(stats) if s[1] is not None]

    txt = self._title("Books of the Bible")
    txt += flot_tickrotor.txt
    txt += self._graph(
        id="bible-stats",
        ylabel="Verses",
        data=[
            dict(data=get_data('mature_count'), color=colMature, label="Mature"),
            dict(data=get_data('young_count'), color=colYoung, label="Young+Learn")
        ],
        conf=dict(xaxis=dict(ticks=list(enumerate(s[0] for s in stats)), rotateTicks=90),
                  yaxis=dict(min=0))
    )

    i = []
    self._line(
        i, "Old Testament", "{} mature / {} young".format(ot_stats.get('mature_count'),
                                                          ot_stats.get('young_count'))
    )
    self._line(
        i, "New Testament", "{} mature / {} young".format(nt_stats.get('mature_count'),
                                                          nt_stats.get('young_count'))
    )
    self._line(
        i, "Total", "{} mature / {} young".format(ot_stats.get('mature_count') + nt_stats.get('mature_count'),
                                                  ot_stats.get('young_count') + nt_stats.get('young_count'))
    )
    txt += self._lineTbl(i)

    result += self._section(txt)

    return result

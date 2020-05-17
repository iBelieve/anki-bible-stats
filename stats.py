from collections import Counter

from anki.consts import *

OT_BOOKS = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    ["Psalms", "Psalm"],
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
]

NT_BOOKS = [
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation"
]


def get_stats(db, model_id, limit):
    stats = []
    for testament in [OT_BOOKS, NT_BOOKS]:
        testament_stats = []
        for book_names in testament:
            if isinstance(book_names, str):
                book_names = [book_names]
            book_stats = sum((get_stats_for_book(db, model_id, limit, book_name)
                              for book_name in book_names), Counter())
            testament_stats.append((book_names[0], book_stats))
        stats.append(testament_stats)
    return stats


def get_stats_for_book(db, model_id, limit, book_name):
    stats = db.first(f'''
    select
        sum(case when queue={QUEUE_TYPE_REV} and ivl >= 21 then 1 else 0 end) as mature_count,
        sum(case when queue in ({QUEUE_TYPE_LRN},{QUEUE_TYPE_DAY_LEARN_RELEARN}) or 
                               (queue={QUEUE_TYPE_REV} and ivl < 21) then 1 else 0 end) as young_count,
        sum(case when queue={QUEUE_TYPE_NEW} then 1 else 0 end) as unseen_count,
        sum(case when queue<{QUEUE_TYPE_NEW} then 1 else 0 end) as suspended_count
    from cards 
    join notes on notes.id = cards.nid
    where ord = 0 and mid = {model_id} and did in {limit} and sfld like "{book_name}%"
    ''')
    return Counter({
        'mature_count': stats[0] or 0,
        'young_count': stats[1] or 0,
        'new_count': stats[2] or 0,
        'suspended_count': stats[3] or 0
    })
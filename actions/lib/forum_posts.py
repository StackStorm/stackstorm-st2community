import time

from datetime import datetime
from datetime import timedelta

import feedparser

__all__ = [
    'get_forum_posts'
]


def get_forum_posts(feed_url, delta=timedelta(days=1, minutes=10)):
    """
    Retrieve forum posts which are been created between now - delta.
    """
    feed = feedparser.parse(feed_url)

    filter_date = (datetime.utcnow() - delta)

    result = []
    for item in feed['items']:
        published_parsed = item.get('published_parsed', None)

        if published_parsed:
            published_dt = datetime.fromtimestamp(time.mktime(published_parsed))
        else:
            published_dt = None

        if published_dt and (published_dt > filter_date):
            item['published_dt'] = published_dt
            result.append(item)

    # Items are sorted in the oldest to newest order
    result = sorted(result, key=lambda x: x['published_dt'])
    return result

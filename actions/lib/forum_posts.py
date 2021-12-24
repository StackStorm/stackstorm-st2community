import time

from datetime import datetime
from datetime import timedelta

import feedparser

__all__ = ["get_forum_posts"]


def get_forum_posts(feed_url, delta=timedelta(days=1, minutes=10)):
    """
    Retrieve forum posts which are been created between now - delta.
    """
    feed = feedparser.parse(feed_url)

    filter_date = datetime.utcnow() - delta

    result = []
    for item in feed["items"]:
        published_parsed = item.get("published_parsed", None)

        if published_parsed:
            published_dt = datetime.fromtimestamp(time.mktime(published_parsed))
        else:
            published_dt = None

        if published_dt and (published_dt > filter_date):
            item["published_dt"] = published_dt
            result.append(item)

    # Items are sorted in the oldest to newest order
    result = sorted(result, key=lambda x: x["published_dt"])

    # Remove complex types (datetime, etc)
    # TODO: Add escape Jinja filter which is available to Orquesta workflows
    keys_to_remove = ["published_dt", "published_parsed", "summary", "summary_detail"]
    for item in result:
        for key in keys_to_remove:
            if key in item:
                del item[key]

    # Serialzie it to json and back to end up only with simple types
    return result

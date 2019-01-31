#!/usr/bin/env python
"""Community Update Action
"""
from datetime import timedelta
from st2common.runners.base_action import Action

from lib import community


class BuildText(Action):
    """Community Update Action
    """
    def __init__(self, config):
        super(BuildText, self).__init__(config)
        self._token = config.get('token')
        self._forum_feed_url = config.get('forum_feed_url')

    def run(self, body=None, user=None, delta=None):
        """Build and return rendered text
        """
        time_delta = timedelta(
            days=delta.get('days', 0),
            hours=delta.get('hours', 0),
            minutes=delta.get('minutes', 0),
            seconds=delta.get('seconds', 0)
        )

        # TODO: Combine 2 rules and only retrieve forum posts once, not once per rule
        return {
            'body': community.build_text(
                token=self._token,
                forum_feed_url=self._forum_feed_url,
                body=body,
                user=user,
                delta=time_delta
            )
        }

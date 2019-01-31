#!/usr/bin/env python
"""
Community Update Action
"""

from datetime import timedelta
from st2common.runners.base_action import Action

from lib import community

__all__ = [
    'BuildTextAction'
]


class BuildTextAction(Action):
    """Community Update Action
    """
    def __init__(self, config):
        super(BuildTextAction, self).__init__(config)
        self._token = config.get('token')
        self._forum_feed_url = config.get('forum_feed_url')

    def run(self, github_users, template_path, delta):
        """
        Build and return rendered text
        """
        time_delta = timedelta(
            days=delta.get('days', 0),
            hours=delta.get('hours', 0),
            minutes=delta.get('minutes', 0),
            seconds=delta.get('seconds', 0)
        )

        return {
            'body': community.build_text(
                logger=self.logger,
                token=self._token,
                forum_feed_url=self._forum_feed_url,
                github_users=github_users,
                delta=time_delta,
                template_path=template_path,
            )
        }

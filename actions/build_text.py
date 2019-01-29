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

    def run(self, body=None, user=None, delta=None):
        """Build and return rendered text
        """
        time_delta = timedelta(
            days=delta.get('days', 0),
            hours=delta.get('hours', 0),
            minutes=delta.get('minutes', 0),
            seconds=delta.get('seconds', 0)
        )

        return {
            'body': community.build_text(
                self._token,
                body=body,
                user=user,
                delta=time_delta
            )
        }

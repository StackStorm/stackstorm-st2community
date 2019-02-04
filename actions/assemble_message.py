#!/usr/bin/env python
# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import codecs


from jinja2 import Environment

from st2common.runners.base_action import Action


__all__ = [
    'AssembleMessageAction'
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class AssembleMessageAction(Action):
    def run(self, forum_posts, github_data, template_path):
        """
        Build and return rendered text.
        """

        template_path = os.path.join(BASE_DIR, '../', template_path)
        template_path = os.path.abspath(template_path)

        with codecs.open(template_path, encoding='utf-8') as fp:
            template_data = fp.read()

        template_context = {
            'github_data': github_data,
            'forum_posts': forum_posts
        }

        # Add all information to the template context and render the template
        env = Environment(trim_blocks=True, lstrip_blocks=True)
        rendered = env.from_string(template_data).render(template_context)
        return rendered

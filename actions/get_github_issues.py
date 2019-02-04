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

from github import Github

from st2common.runners.base_action import Action

from lib.utils import get_timedelta_object_from_delta_arg
from lib.github_issues import get_issues_and_prs_for_user

__all__ = [
    'GetGithubIssuesAction'
]


class GetGithubIssuesAction(Action):
    def run(self, token, user, delta):
        time_delta = get_timedelta_object_from_delta_arg(delta)
        github = Github(token)
        github_user = github.get_user(user)
        result = get_issues_and_prs_for_user(github_user=github_user, user=user,
                                             time_delta=time_delta)
        return result

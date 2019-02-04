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

from datetime import datetime

__all__ = [
    'get_issues_and_prs_for_repo',
    'get_issues_and_prs_for_user'
]


def get_issues_and_prs_for_repo(repo, time_delta):
    """
    Retrieve new issues and PRs for the provided user and time period.
    """
    result = {
        'issues': [],
        'prs': []
    }

    since_dt = (datetime.now() - time_delta)
    issues = list(repo.get_issues(since=since_dt))

    for issue in issues:
        if issue.pull_request:
            result['prs'].append(issue)
        else:
            result['issues'].append(issue)

    return result


def get_issues_and_prs_for_user(github_user, time_delta):
    """
    Retrieve issues and PRs for all the Github repos for the provided user.
    """
    result = {
        'issues': [],
        'prs': []
    }

    for repo in github_user.get_repos():
        result = get_issues_and_prs_for_repo(repo=repo, time_delta=time_delta)
        result['issues'].extend(result['issues'])
        result['prs'].extend(result['prs'])

    return result

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

__all__ = ["get_issues_and_prs_for_repo", "get_issues_and_prs_for_user"]


def get_issues_and_prs_for_repo(repo, time_delta):
    """
    Retrieve new issues and PRs for the provided user and time period.
    """
    result = {"issues": [], "pulls": []}

    since_dt = datetime.now() - time_delta
    issues = list(repo.get_issues(since=since_dt))

    for issue in issues:
        # Convert Python object in a native Python type (dict)
        issue_dict = issue.raw_data
        issue_dict["repository"] = issue.repository.raw_data

        if issue.pull_request:
            result["pulls"].append(issue_dict)
        else:
            result["issues"].append(issue_dict)

        # Remove fields which we don't need to spin things up
        if "body" in issue_dict:
            del issue_dict["body"]

    return result


def get_issues_and_prs_for_user(github_user, time_delta, repo_type="all"):
    """
    Retrieve issues and PRs for all the Github repos for the provided user.

    :param repo_type: Type of repos to query for the isssues (all, public, private, forks,
                      sources, member).
    :type repo_type: ``str``
    """
    result = {
        "username": github_user.login.replace("-", "_").lower(),
        "username_friendly": github_user.login,
        "issues": [],
        "pulls": [],
    }

    for repo in github_user.get_repos(type=repo_type):
        repo_result = get_issues_and_prs_for_repo(repo=repo, time_delta=time_delta)
        result["issues"].extend(repo_result["issues"])
        result["pulls"].extend(repo_result["pulls"])

    return result

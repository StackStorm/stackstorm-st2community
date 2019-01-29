#!/usr/bin/env python
"""Daily update from Github
"""
from datetime import datetime, timedelta

from github import Github
from jinja2 import Template


def _iterate_repos(user, func, **kwargs):
    new_items = []
    for repo in user.get_repos():
        new_items += func(repo, **kwargs)

    return new_items


def _filter_by_date(items, date_attribute, delta):
    filter_date = datetime.utcnow() - delta
    filtered_items = []

    for item in items:
        if getattr(item, date_attribute) > filter_date:
            filtered_items.append(item)

    return filtered_items


def _filter_prs(repo, delta=timedelta(days=1, minutes=10)):
    return _filter_by_date(repo.get_pulls(), 'created_at', delta)


def _get_new_prs(user, delta):
    return _iterate_repos(user, _filter_prs, delta=delta)


def _filter_issues(repo, delta=timedelta(days=1, minutes=10)):
    issues = _filter_by_date(repo.get_issues(), 'created_at', delta)
    for index, issue in enumerate(issues):
        if issue.pull_request:
            issues.pop(index)
    return issues


def _get_new_issues(user, delta):
    return _iterate_repos(user, _filter_issues, delta=delta)


def build_text(
        token,
        body=None,
        user='StackStorm-Exchange',
        delta=timedelta(days=1, minutes=10)
):
    """build_text processes the new issues and PRs for a given time period and
    returns slack message text to be sent.
    """
    body = Template(body) if body is not None else Template(
        "Good morning, @oncall. Here's your community update. Yesterday there "
        "were **{{ new_issue_count }}** new issue(s), and "
        "**{{ new_pull_count }}** new pull request(s).\n"
        "{% if pulls %}\n*Pull Requests*\n"
        "{% for pull in pulls %}* <{{ pull.base.repo.html_url }}|{{ pull.base."
        "repo.name }}>: <{{ pull.html_url }}|{{ pull.title }}> by <{{ pull.use"
        "r.html_url }}|{{ pull.user.name }}>\n"
        "{% endfor %}{% endif %}{% if issues %}\n*Issues:*\n"
        "{% for issue in issues %}* <{{ issue.repository.html_url }}|{{ issue."
        "repository.name }}>: <{{ issue.html_url }}|{{ issue.title }}> by <{{ "
        "issue.user.html_url }}|{{ issue.user.name }}>{% endfor %}{% endif %}"
    )
    github = Github(token)
    exchange = github.get_user(user)
    pulls = _get_new_prs(exchange, delta=delta)
    issues = _get_new_issues(exchange, delta=delta)

    return body.render(
        new_issue_count=len(issues),
        new_pull_count=len(pulls),
        pulls=pulls,
        issues=issues,
    )

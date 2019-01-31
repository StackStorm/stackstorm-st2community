#!/usr/bin/env python
"""Daily update from Github
"""

import os

from datetime import datetime, timedelta

from github import Github
from jinja2 import Template

from lib.forum_posts import get_forum_posts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE_PATH = os.path.join(BASE_DIR, '../../etc/message_template.j2')


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
        forum_feed_url,
        body=None,
        user='StackStorm-Exchange',
        delta=timedelta(days=1, minutes=10)
):
    """build_text processes the new issues and PRs for a given time period and
    returns slack message text to be sent.
    """
    if body:
        body = body.replace('[', '{')
        body = body.replace(']', '}')

    if not body:
        # Read default template from file
        with open(DEFAULT_TEMPLATE_PATH, 'r') as fp:
            body = fp.read()

    template = Template(body)

    # 1. Retrieve Github stats for Github organization
    github = Github(token)
    exchange = github.get_user(user)
    pulls = _get_new_prs(exchange, delta=delta)
    issues = _get_new_issues(exchange, delta=delta)

    # 2. Retrieve forum posts from forum.stackstorm.com
    forum_posts = get_forum_posts(feed_url=forum_feed_url, delta=delta)

    return template.render(
        new_issue_count=len(issues),
        new_pull_count=len(pulls),
        pulls=pulls,
        issues=issues,
        new_forum_post_count=len(forum_posts),
        forum_posts=forum_posts,
    )

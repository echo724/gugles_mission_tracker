import os, sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gugles_mission_tracker import env, graphql
import json
import pytest

LEN_ALL_DISCUSSIONS = 236
LEN_DISCUSSIONS_AFTER_PERIOD = 40
LEN_DISCUSSIONS_IN_CATEGORY = 39
LEN_AUTHORS = 33
START_DATE = datetime.strptime(env.START_DATE, "%Y-%m-%d").date()
END_DATE = START_DATE + timedelta(days=6)


def read_discussions_from_file(filename):
    with open(filename, "r") as f:
        discussions = json.load(f)
    return discussions


DISCUSSIONS = read_discussions_from_file("tests/test_discussions.json")
AUTHOR_DISCUSSION_COUNT = read_discussions_from_file("tests/test_author_count.json")


# change Class test to function test
def test_get_discussions_after_period():
    discussions = graphql.get_discussions_after_period(
        DISCUSSIONS, START_DATE, END_DATE
    )
    assert len(discussions) == LEN_DISCUSSIONS_AFTER_PERIOD


def test_get_discussions_in_category():
    discussions = graphql.get_discussions_after_period(
        DISCUSSIONS, START_DATE, END_DATE
    )
    discussions = graphql.get_discussions_by_category(discussions, env.CATEGORIES)
    assert len(discussions) == LEN_DISCUSSIONS_IN_CATEGORY


def test_get_discussions_by_author():
    author_count = {}
    discussions = graphql.get_discussions_after_period(
        DISCUSSIONS, START_DATE, END_DATE
    )
    discussions = graphql.get_discussions_by_category(discussions, env.CATEGORIES)
    for discussion in discussions:
        author = discussion["node"]["author"]["login"]
        if author in author_count:
            author_count[author] += 1
        else:
            author_count[author] = 1
    assert len(author_count) == LEN_AUTHORS
    assert author_count == AUTHOR_DISCUSSION_COUNT


def test_get_discussions_number_by_author_after_date():
    for author, count in AUTHOR_DISCUSSION_COUNT.items():
        discussions = graphql.get_discussions_number_by_author_after_date(
            author, START_DATE, END_DATE
        )
        assert discussions == count

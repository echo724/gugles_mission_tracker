import os
from os import path

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REQUEST_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

GSPREAD_URL = "https://docs.google.com/spreadsheets/d/1mSuoPCjmRDDZ5ouNucHRO5eZmderAjGxc_LU81cPb3c/edit#gid=0"

JSON_KEY_PATH = path.join(path.dirname(path.dirname(__file__)), "credentials.json")

CREW_NUM = 38

START_DATE = "2023-02-20"

DATE_COLUMN = 3

SPREAD_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

ANNOUNCEMENT_CATEGORY_ID = "DIC_kwDOJAfDqs4CUWOk"

GUGLES_REPO_ID = "R_kgDOJAfDqg"

CATEGORIES = ["2 백엔드 글모음", "3 프론트엔드 글모음", "4 안드로이드 글모음", "5 회고 글모음"]

MUTATION_QUERY = """
mutation {
    createDiscussion(input: {
        repositoryId: {put_repository_id},
        categoryId: {put_category_id},
        body: {put_body},
        title: {put_title}
    }) {
        discussion {
            id
        }
    }
}
"""

QUERY = """
{
    repository(owner: "woowacourse-study", name: "Gugles") {
        discussions(first:100 {put_cursor}) {
            totalCount
            pageInfo {
                endCursor
                hasNextPage
            }
            edges{
                cursor
                node {
                    id
                    title
                    createdAt
                    category{
                        name
                    }
                    author {
                        login
                    }
                }
            }
        }
    }
}
"""

import os
import json
from dotenv import load_dotenv

# Injection of environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GSPREAD_CREDENTIAL_KEY = json.loads(os.environ["GSPREAD_CREDENTIAL_KEY"])
CREW_NUM = os.environ["CREW_NUM"]
CATEGORIES = json.loads(os.environ["CATEGORIES"])
ANNOUNCEMENT_CATEGORY_ID = os.environ["ANNOUNCEMENT_CATEGORY_ID"]

# Other constants
REQUEST_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

GSPREAD_URL = "https://docs.google.com/spreadsheets/d/1mSuoPCjmRDDZ5ouNucHRO5eZmderAjGxc_LU81cPb3c/edit#gid=0"

START_DATE = "2023-02-20"

DATE_COLUMN = 3

SPREAD_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


GUGLES_REPO_ID = "R_kgDOJAfDqg"

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

owner_name = "woowacourse-study"
repo_name = "Gugles"

QUERY = "{"
QUERY += f'repository(owner: "{owner_name}", name: "{repo_name}")'
QUERY += """
{
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

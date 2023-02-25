import datetime
import requests
import env



CACHED_DISCUSSIONS = []

def build_query(cursor=None):
    if cursor is None:
        return env.QUERY.replace("{put_cursor}", "")
    return env.QUERY.replace("{put_cursor}", f', after: "{cursor}"')

def get_discussions(cursor=None):
    query = build_query(cursor)
    response = requests.post(env.REQUEST_URL, json={"query": query}, headers=env.HEADERS)
    if response.status_code == 200:
        return response.json()['data']['repository']['discussions']

def get_all_discussions():
    if not CACHED_DISCUSSIONS:
        discussions = []
        cursor = None
        while True:
            response = get_discussions(cursor)
            discussions.extend(response['edges'])
            if response['pageInfo']['hasNextPage']:
                cursor = response['pageInfo']['endCursor']
            else:
                break
        CACHED_DISCUSSIONS.append(discussions)
    return CACHED_DISCUSSIONS[0]

def get_discussions_after_period(start,end):
    discussions = get_all_discussions()
    return [discussion for discussion in discussions \
            if datetime.datetime.strptime(discussion['node']['createdAt'], "%Y-%m-%dT%H:%M:%SZ").date() >= start \
            and datetime.datetime.strptime(discussion['node']['createdAt'], "%Y-%m-%dT%H:%M:%SZ").date() < end]

def get_discussions_number_by_author_after_date(author, start,end):
    return len([discussion for discussion in get_discussions_after_period(start,end) if discussion['node']['author']['login'] == author])



def build_mutation_query(repository_id, category_id, body, title):
    return env.MUTATION_QUERY.replace("{put_repository_id}", f'"{repository_id}"') \
                .replace("{put_category_id}", f'"{category_id}"') \
                .replace("{put_body}", f'"{body}"') \
                .replace("{put_title}", f'"{title}"')

def make_discussion(repository_id, category_id, body, title):
    query = build_mutation_query(repository_id, category_id, body, title)
    response = requests.post(env.REQUEST_URL, json={"query": query}, headers=env.HEADERS)
    if response.status_code == 200:
        return response.json()

def make_announcement(title, body):
    return make_discussion(env.GUGLES_REPO_ID, env.ANNOUNCEMENT_CATEGORY_ID, body, title)
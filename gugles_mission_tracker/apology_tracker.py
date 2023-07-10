import datetime
import sheets
import graphql
import status_maker
import env

github_ids = sheets.get_github_ids()
nicknames = sheets.get_nicknames()


def get_nicknames_has_no_discussion(nicknames, status):
    nicknames = sheets.get_nicknames()
    nicknames_has_no_discussion = []
    for nickname in nicknames:
        if status[nickname] == 0:
            nicknames_has_no_discussion.append(nickname)
    return nicknames_has_no_discussion


def get_last_week_apology_status():
    status = {}
    for i, github_id in enumerate(github_ids):
        status[nicknames[i]] = graphql.get_discussions_number_by_author_after_date(
            github_id,
            status_maker.last_week_start_date,
            status_maker.last_week_end_date,
            env.APOLOGY_CATEGORY,
        )
    return status


def get_last_last_week_status():
    status = {}
    last_last_week_start_date = status_maker.last_week_start_date - datetime.timedelta(
        days=7
    )
    last_last_week_end_date = status_maker.last_week_end_date - datetime.timedelta(
        days=7
    )
    for i, github_id in enumerate(github_ids):
        status[nicknames[i]] = graphql.get_discussions_number_by_author_after_date(
            github_id,
            last_last_week_start_date,
            last_last_week_end_date,
        )
    return status


def check_crew_wrote_apology():
    # 지난 지난주 글이 없는 사람들
    last_last_week_status = get_last_last_week_status()
    last_last_week_nicknames_has_no_discussion = get_nicknames_has_no_discussion(
        nicknames, last_last_week_status
    )
    # 지난주 반성문이 없는 사람들
    last_week_apology_status = get_last_week_apology_status()
    last_week_nicknames_has_no_apology = get_nicknames_has_no_discussion(
        nicknames, last_week_apology_status
    )
    nicknames_did_not_write_apology = []
    for nickname in last_last_week_nicknames_has_no_discussion:
        if nickname in last_week_nicknames_has_no_apology:
            nicknames_did_not_write_apology.append(nickname)
    return nicknames_did_not_write_apology

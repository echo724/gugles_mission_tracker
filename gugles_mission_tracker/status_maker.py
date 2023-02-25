import datetime
import sheets,graphql

last_week_end_date = sheets.get_week_start_date()
last_week_start_date = last_week_end_date - datetime.timedelta(days=7)
this_week_start_date = sheets.get_week_start_date()
this_week_end_date = this_week_start_date + datetime.timedelta(days=7)

github_ids = sheets.get_github_ids()
nicknames = sheets.get_nicknames()

STATUS = {}

def get_this_week_status():
    if not STATUS:
        for i,github_id in enumerate(github_ids):
            STATUS[nicknames[i]] = graphql.get_discussions_number_by_author_after_date(github_id, this_week_start_date, this_week_end_date)
    return STATUS

def get_last_week_status():
    if not STATUS:
        for i,github_id in enumerate(github_ids):
            STATUS[nicknames[i]] = graphql.get_discussions_number_by_author_after_date(github_id, last_week_start_date, last_week_end_date)
    return STATUS
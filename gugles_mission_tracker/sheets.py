import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import env


SHEET = []
NICKNAME = []
GITHUB_IDS = []

def get_sheet():
    if not SHEET:
        credential = ServiceAccountCredentials.from_json_keyfile_name(env.JSON_KEY_PATH, env.SPREAD_SCOPE)
        gc = gspread.authorize(credential)
        SHEET.append(gc.open_by_url(env.GSPREAD_URL).worksheet("주차별미션현황"))
    return SHEET[0]

def get_nicknames():
    if not NICKNAME:
        sheet = get_sheet()
        NICKNAME.append(sheet.col_values(1)[1:env.CREW_NUM+1])
    return NICKNAME[0]

def get_github_ids():
    if not GITHUB_IDS:
        sheet = get_sheet()
        GITHUB_IDS.append(sheet.col_values(2)[1:env.CREW_NUM+1])
    return GITHUB_IDS[0]

def get_week_num():
    week_num = (datetime.date.today() - datetime.datetime.strptime(env.START_DATE, "%Y-%m-%d").date()).days//7
    return week_num

def get_col_number_from_week_number():
    return env.DATE_COLUMN + get_week_num()

def get_week_start_date():
    sheet = get_sheet()
    date = sheet.col_values(get_col_number_from_week_number())[0]
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()

def update_cell_from_github_id(github_id,value):
    sheet = get_sheet()
    github_ids = get_github_ids()
    row_number = github_ids.index(github_id) + 2
    col_number = get_col_number_from_week_number()
    sheet.update_cell(row_number, col_number, value)
    
def update_cell_from_nickname(nickname,value,period):
    sheet = get_sheet()
    nicknames = get_nicknames()
    row_number = nicknames.index(nickname) + 2
    if period == "this_week":
        col_number = get_col_number_from_week_number()
    elif period == "last_week":
        col_number = get_col_number_from_week_number() - 1
    sheet.update_cell(row_number, col_number, value)
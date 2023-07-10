import pytz
import datetime
from google.oauth2.service_account import Credentials
import env
import gspread
from gspread import Cell


SHEET = []
NICKNAME = []
GITHUB_IDS = []


def get_cred():
    cred = Credentials.from_service_account_info(env.GSPREAD_CREDENTIAL_KEY)
    scoped = cred.with_scopes(env.SPREAD_SCOPE)
    return scoped


async def get_asyncio_sheet(sheet_name, agcm):
    gc = await agcm.authorize()
    sheet = await gc.open_by_url(env.GSPREAD_URL)
    ws = await sheet.worksheet(sheet_name)
    return ws


def get_sheet(sheet_name="주차별미션현황"):
    if not SHEET:
        cred = get_cred()
        gc = gspread.authorize(cred)
        sheet = gc.open_by_url(env.GSPREAD_URL)
        ws = sheet.worksheet(sheet_name)
        SHEET.append(ws)
    return SHEET[0]


def get_nicknames():
    if not NICKNAME:
        sheet = get_sheet()
        NICKNAME.append(sheet.col_values(1)[1 : env.CREW_NUM + 1])
    return NICKNAME[0]


def get_github_ids():
    if not GITHUB_IDS:
        sheet = get_sheet()
        GITHUB_IDS.append(sheet.col_values(2)[1 : env.CREW_NUM + 1])
    return GITHUB_IDS[0]


def get_week_num():
    week_num = (
        datetime.datetime.now(pytz.timezone("Asia/Seoul")).date()
        - datetime.datetime.strptime(env.START_DATE, "%Y-%m-%d").date()
    ).days // 7
    return week_num


def get_col_number_from_week_number():
    return env.DATE_COLUMN + get_week_num()


def get_week_start_date():
    sheet = get_sheet()
    date = sheet.col_values(get_col_number_from_week_number())[0]
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def update_cell(status, period):
    sheet = get_sheet()
    nicknames = get_nicknames()
    cells = []
    for nickname in status.keys():
        row_number = nicknames.index(nickname) + 2
        col_number = get_col_number(period)
        cells.append(Cell(row_number, col_number, status[nickname]))
    sheet.update_cells(cells)


def get_col_number(period):
    if period == "this_week":
        col_number = get_col_number_from_week_number()
    elif period == "last_week":
        col_number = get_col_number_from_week_number() - 1
    return col_number

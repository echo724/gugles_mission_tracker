import datetime
import graphql
import status_maker
import sheets

def make_notification_title():
    week_num = sheets.get_week_num()
    start = sheets.get_week_start_date() - datetime.timedelta(days = 7)
    end = sheets.get_week_start_date() - datetime.timedelta(days = 1)
    return f"꾸글쓰 미션 결과 - {week_num}주차 ({start.strftime('%-m월 %-d일')} ~ {end.strftime('%-m월 %-d일')})"

def make_status_body(period):
    if period == "this_week":
        status = status_maker.get_this_week_status()
    elif period == "last_week":
        status = status_maker.get_last_week_status()
    else:
        raise Exception("Invalid period")
    
    body = "## 🥳 지난 주 미션 수행 결과: "
    body += f"총 {sum(status.values())}개 글 작성 \n\n"
    body += "### ✍️ 크루별 작성한 글 수:\n\n"
    nicknames = sheets.get_nicknames()
    has_no_discussion = []
    body += "|닉네임|게시물 수|\n|---|---|\n"
    for nickname in nicknames:
        if status[nickname] == 0:
            has_no_discussion.append(nickname)
        body += f"|{nickname}|{status[nickname]}|\n"
    body += f"|{len(nicknames)}명|{sum(status.values())}개|\n"
    
    exceptions = parse_exception_list(has_no_discussion)
    if not exceptions:
        has_no_discussion = list(filter(lambda x: x not in exceptions, has_no_discussion))
    
    body += "\n"
    body += f"### 🥲 미션을 수행하지 않은 크루: {len(has_no_discussion)}명\n\n"
    if has_no_discussion:
        body += ", ".join(has_no_discussion)
        body += "\n\n"
        next_week = sheets.get_week_start_date() + datetime.timedelta(days=14)
        body += f"### 💪 {next_week.strftime('%-m월 %-d일')}까지 반성문을 작성해 슬랙에 올려주세요\n\n"
    else:
        body += "모두 수행하셨네요! 꾸글쓰 크루들 최고 👏👏👏\n\n"
    return body

def parse_exception_list(has_no_discussion):
    while True:
        exception_list = list(map(lambda x: x.strip(),input("예외자 입력:(크루는 ,로 구분) ").split(",")))
        if exception_list == [""]:
            return []
        if all(map(lambda x: x in has_no_discussion, exception_list)):
            print(f"예외자: {', '.join(exception_list)}")
            return exception_list
        print("예외자가 잘못 입력되었습니다. 다시 입력해주세요.")

def make_body(period):
    body = make_status_body(period)
    return body

def make_notification(period):
    title = make_notification_title()
    body = make_body(period)
    return graphql.make_announcement(title, body)
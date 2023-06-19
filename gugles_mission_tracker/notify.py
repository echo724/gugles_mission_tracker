import datetime
import graphql
import status_maker
import sheets
import apology_tracker


def make_notification_title():
    week_period = generate_week_period_message()
    return f"꾸글쓰 미션 결과 - {week_period}"


def generate_week_period_message():
    week_num = sheets.get_week_num()
    start = sheets.get_week_start_date() - datetime.timedelta(days=7)
    end = sheets.get_week_start_date() - datetime.timedelta(days=1)
    week_period = (
        f"{week_num}주차 ({start.strftime('%-m월 %-d일')} ~ {end.strftime('%-m월 %-d일')})"
    )

    return week_period


def make_status_body(period):
    status = status_maker.get_status(period)

    body = "## 🥳 지난 주 미션 수행 결과: "
    body += f"총 {sum(status.values())}개 글 작성 \n\n"
    body += "### ✍️ 크루별 작성한 글 수:\n\n"
    body += "|닉네임|게시물 수|\n|---|---|\n"

    nicknames = sheets.get_nicknames()

    for nickname in nicknames:
        body += f"|{nickname}|{status[nickname]}|\n"
    body += f"|{len(nicknames)}명|{sum(status.values())}개|\n"

    has_no_discussion = apology_tracker.get_nicknames_has_no_discussion(
        nicknames, status
    )

    body += "\n"
    body += f"### 🥲 미션을 수행하지 않은 크루: {len(has_no_discussion)}명\n\n"
    if has_no_discussion:
        body += ", ".join(has_no_discussion)
        body += "\n\n"
        next_week = sheets.get_week_start_date() + datetime.timedelta(days=7)
        body += f"### 💪 {next_week.strftime('%-m월 %-d일')}까지 반성문을 작성해 슬랙에 올려주세요\n\n"
    else:
        body += "모두 수행하셨네요! 꾸글쓰 크루들 최고 👏👏👏\n\n"
    return body


def make_apology_tracker_body():
    body = "# 지난주 반성문을 작성하지 않은 크루들입니다.🥲\n\n"
    nicknames = apology_tracker.check_crew_wrote_apology()
    if nicknames:
        body += ", ".join(nicknames)
        body += "\n\n"
        body += "### 꼭 다음주까지 반성문을 작성해주세요!\n"
        body += "> ⚠️ 다음주에도 반성문을 작성하지 않으면, 꾸글쓰 크루에서 제외될 수 있습니다.\n\n"
    else:
        body += "모두 반성문을 작성하셨네요! 꾸글쓰 크루들 최고 👏👏👏\n\n"
    return body


def make_body(period):
    body = make_status_body(period)
    return body


def make_notification(period):
    title = make_notification_title()
    body = make_body(period)
    return graphql.make_announcement(title, body)


def make_apology_notification():
    title = "반성문 작성 안한 크루 - " + generate_week_period_message()
    body = make_apology_tracker_body()
    return graphql.make_announcement(title, body)

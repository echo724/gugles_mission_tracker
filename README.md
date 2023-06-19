# 꾸글쓰 미션 트래커

우아한테크코스 5기 [꾸준히 글쓰는 크루들](https://github.com/woowacourse-study/Gugles)에서 사용되는 미션 트래커

- Dicussions 활동 기록으로 gspread 업데이트 및 discussion에 결과 업로드

## 자동화 및 작동 순서
- Github Actions을 사용해 월요일 00:01분에 gugles_mission_tracker 실행
- Github Discussions graphql api를 사용해 
    - 1주일 단위의 글들을 조회
    - 글쓴 유저 파악
    - 디스커션에 미션 진행상황 작성
- 스프레드시트에 업데이트
- Slack Github bot을 통해 채널트 notify

## 준비물

- github personal token
- 미션 트래커에 연동된 service account credentials

## 사용법

```bash
$mission_tracker check #미션 결과를 미션 트래커 스프레드시트에 업데이트

$mission_tracker report #미션 결과를 스프레드시트에 업데이트하고 꾸글쓰 디스커션에 업로드
```

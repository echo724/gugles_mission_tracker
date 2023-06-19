import notify, update, arg_parser


def run():
    args = arg_parser.parse_args()
    if args.action == "check":
        try:
            update.update_cells("this_week")
            print("미션 수행 결과를 업데이트했습니다.")
        except Exception as e:
            print("미션 수행 결과를 업데이트하는데 실패했습니다.")
            print(e)
    elif args.action == "check_last":
        try:
            update.update_cells("last_week")
            print("지난주  미션 수행 결과를 업데이트했습니다.")
        except Exception as e:
            print("미션 수행 결과를 업데이트하는데 실패했습니다.")
            print(e)
    elif args.action == "report":
        try:
            update.update_cells("last_week")
            print("미션 수행 결과를 업데이트했습니다.")
            notify.make_notification("last_week")
            print("미션 수행 결과 알림을 보냈습니다.")
            notify.make_apology_notification()
            print("반성문 작성하지 않은 크루 알림을 보냈습니다.")
        except Exception as e:
            print("미션 수행 결과를 업데이트하거나 알림을 보내는데 실패했습니다.")
            print(e)


if __name__ == "__main__":
    run()

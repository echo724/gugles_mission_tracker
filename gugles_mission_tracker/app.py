import notify,update,arg_parser

def run():
    args = arg_parser.parse_args()
    if args.action == "check":
        try:
            update.update_cells("this_week")
            print("미션 수행 결과를 업데이트했습니다.")
        except Exception as e:
            print("미션 수행 결과를 업데이트하는데 실패했습니다.")
            print(e)
    
    elif args.action == "report":
        try:
            update.update_cells("last_week")
            notify.make_notification("last_week")
            print("미션 수행 결과를 업데이트하고 알림을 보냈습니다.")
        except Exception as e:
            print("미션 수행 결과를 업데이트하거나 알림을 보내는데 실패했습니다.")
    

if __name__ == "__main__":
    run()
import notify,update,arg_parser

def run():
    args = arg_parser.parse_args()
    if args.action == "check":
        update.update_cells("this_week")
    else:
        update.update_cells("last_week")
        notify.make_notification("last_week")
    

if __name__ == "__main__":
    run()
import sheets
import status_maker

def update_cells(period):
    if period == "this_week":
        status = status_maker.get_this_week_status()
    elif period == "last_week":
        status = status_maker.get_last_week_status()
    else:
        raise Exception("Invalid period")
    for nickname in status.keys():
            sheets.update_cell_from_nickname(nickname, status[nickname],period)
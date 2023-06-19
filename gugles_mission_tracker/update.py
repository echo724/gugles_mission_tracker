import sheets
import status_maker


def update_cells(period):
    status = status_maker.get_status(period)
    for nickname in status.keys():
        print(f"Updating {nickname}'s status")
        sheets.update_cell_from_nickname(nickname, status[nickname], period)

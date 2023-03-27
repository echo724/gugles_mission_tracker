import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Gugles Mission Tracker')

    parser.add_argument('action',choices=['check','report','check_last'] ,help="미션 트래커 동작을 선택합니다.", default="check")
    
    return parser.parse_args()
import json
import pandas as pd
from datetime import datetime

from slacker import Slacker
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config


def connect_gspread(jsonf, key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_url(config.url).get_worksheet(0)
    return worksheet


def extract_df(worksheet):
    df = pd.DataFrame(worksheet.get_all_records(empty2zero=False, head=1, default_blank=''))
    return df

# def get_message():
#     return msg

def main(API_TOKEN, key):
    wc = connect_gspread(config.jsonf, key)
    df = extract_df(wc)

    today = datetime.now()
    today = today.strftime('%m/%d')
    target = df[df['日付'] == today].reset_index(drop=True)

    for i in range(target.shape[0]):
        msg = f"今日の {target.loc[i]['仕事内容']} は <@{config.mem_dict[target.loc[i]['担当']]}> !!!!!"
        slack = Slacker(API_TOKEN)
        slack.chat.post_message("生活_全般", msg, as_user=True)


if __name__ == "__main__":
    main(config.API_TOKEN, config.spread_sheet_key)
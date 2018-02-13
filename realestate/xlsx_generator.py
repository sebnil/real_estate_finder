import pandas as pd
import sqlite3
from realestate.database import database_path
from realestate.constants import output_xlsx_path
from datetime import datetime

def generate():

    conn = sqlite3.connect(database_path)
    query = "SELECT * FROM realestate;"
    df = pd.read_sql_query(query, conn)

    df['link'] = df['link'].apply(lambda x: make_hyperlink(x))

    df['price_per_month_in_sek'] = pd.to_numeric((pd.to_numeric(df['price_per_week']).fillna(0) * 52 / 12) * 6.3862813, downcast='integer')

    now = datetime.now()
    now_timestring = now.__str__().replace(' ', '_')
    writer = pd.ExcelWriter('{}/realestate_{}.xlsx'.format(output_xlsx_path, now_timestring))
    pd.DataFrame.to_excel(df, writer, index=False)
    writer.save()


def make_hyperlink(value):
    return '=HYPERLINK("{}")'.format(value)


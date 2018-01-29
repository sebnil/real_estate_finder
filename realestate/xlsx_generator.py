import pandas as pd
import sqlite3
from database import database_path


def generate():

    conn = sqlite3.connect(database_path)
    query = "SELECT * FROM realestate;"
    df = pd.read_sql_query(query, conn)

    df['link'] = df['link'].apply(lambda x: make_hyperlink(x))

    df['price_per_month_in_sek'] = pd.to_numeric((pd.to_numeric(df['price_per_week']).fillna(0) * 52 / 12) * 6.3862813, downcast='integer')

    writer = pd.ExcelWriter('realestate.xlsx')
    pd.DataFrame.to_excel(df, writer, index=False)
    writer.save()


def make_hyperlink(value):
    return '=HYPERLINK("{}")'.format(value)


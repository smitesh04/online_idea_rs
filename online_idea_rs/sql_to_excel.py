from db_config import DbConfig
import pandas as pd
import datetime

obj = DbConfig()

qr = f'SELECT * FROM {obj.data_table}'
obj.cur.execute(qr)
results = obj.cur.fetchall()

df = pd.read_sql(qr, obj.con)
date_today = datetime.datetime.today()
date_today_strf = date_today.strftime("%d_%m_%Y")
country = 'Serbia'
excel_file_path = f'online_idea_rs_{date_today_strf}_{country}.xlsx'
df.to_excel(excel_file_path, index=False)
print("Data exported to Excel file successfully.")


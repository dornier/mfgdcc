from flask import Flask
import pandas as pd
import os


app = Flask(__name__)
app.secret_key = 'hf\x04\x1a\x18\x80\x833\xef/N\xea\x92\xe3\x96\xf5K<N\x0c\xb7\xa8\xf3'

column_names = [
    'Name',
    'Market Cap',
    'Price',
    'Supply',
    'Status'
]

base_dir = os.path.abspath(os.path.dirname(__file__))
coins_df = pd.read_fwf(os.path.join(base_dir, '..',  'coins.txt'), header=0, names=column_names)
nan_replacements = {
    'Name': '',
    'Market Cap': 0,
    'Price': 0,
    'Supply': 0,
    'Status': 'N/A'
}
coins_df.fillna(value=nan_replacements, inplace=True)
coins_df_names = sorted(coins_df.Name.unique().tolist(), key=str.lower)
coins_df_statuses = coins_df.Status.unique().tolist()


import mfgdcc.views

#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

survey1a = pd.read_csv('survey1a.csv')
#survey1b = pd.read_csv('survey1b.csv')
#survey2a = pd.read_csv('survey2a.csv')
survey2b = pd.read_csv('survey2b.csv')
# %%

def data_cleaner(df):
    df.drop(columns=["Response ID", "Date submitted", "Start language", "Seed"], inplace=True)
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.lower()
    df = df[df['do_you_agree_to_participate?'] == 'Yes']
    df.drop(columns='do_you_agree_to_participate?', inplace=True)
    return df

survey1a = data_cleaner(survey1a)
survey2b = data_cleaner(survey2b)
# %%

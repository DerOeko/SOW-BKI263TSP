#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import re
raw_survey1a = pd.read_csv('survey1a.csv')
#raw_survey1b = pd.read_csv('survey1b.csv')
#raw_survey2a = pd.read_csv('survey2a.csv')
raw_survey2b = pd.read_csv('survey2b.csv')
# %%
def clean_column_name(col):
    col_clean = col.strip()  # Remove extra whitespace
    if col_clean.lower() in [
        'how trustworthy do you believe this content is?',
        'how credible do you believe this piece of content is?',
        'would you feel confident using this as a reference in an essay?'
    ]:
        return col_clean.replace(" ", "_").replace("?", "_0").lower()
    else:
        # Use a more flexible regex pattern here.
        col = re.sub(r'(.*?)[\?\s\.]+(\d+)$', r'\1_\2', col_clean)
        return col.replace(" ", "_").lower()

def data_cleaner(raw_df):
    df = raw_df.copy()
    df.drop(columns=["Date submitted", "Start language", "Seed"], inplace=True)
    df.rename(columns={'Response ID': 'participant_id'}, inplace=True)
    df.columns = [clean_column_name(col) for col in df.columns]
    print(df.columns)
    df = df[df['do_you_agree_to_participate'] == 'Yes']
    df.drop(columns='do_you_agree_to_participate', inplace=True)
    df.drop_duplicates(inplace=True)
    return df

clean_survey1a = data_cleaner(raw_survey1a)
clean_survey2b = data_cleaner(raw_survey2b)
# %%

survey1_text_origins = {
    1: 'traditional',
    2: 'traditional',
    3: 'ai',
    4: 'traditional',
    5: 'ai',
    6: 'ai',
    7: 'traditional',
    8: 'traditional',
    9: 'traditional',
    10: 'ai',
    11: 'ai',
    12: 'ai'
}

survey2_text_origins = {
    1: 'traditional',
    2: 'traditional',
    3: 'traditional',
    4: 'traditional',
    5: 'traditional',
    6: 'traditional',
    7: 'ai',
    8: 'ai',
    9: 'ai',
    10: 'ai',
    11: 'ai',
    12: 'ai'
}

trust_cols1 = [col for col in clean_survey1a.columns if 'trustworthy' in col]
credible_cols1 = [col for col in clean_survey1a.columns if 'credible' in col]
usage_cols1 = [col for col in clean_survey1a.columns if 'confident' in col]
belief_cols1 = [col for col in clean_survey1a.columns if 'believe' in col]
background_cols1 = [col for col in clean_survey1a.columns if col not in trust_cols1 + credible_cols1 + usage_cols1 + belief_cols1]


df_long = pd.wide_to_long(clean_survey1a,
                          stubnames=['trustworthy', 'credible', 'confident', 'Do you believe this content is AI generated?'],
                          i = 'participant_id',
                          j = 'text_number',
                          sep = "_").reset_index()
# %%

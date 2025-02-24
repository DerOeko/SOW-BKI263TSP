#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest
import seaborn as sns
import re
raw_survey1a = pd.read_csv('survey1a.csv')
#raw_survey1b = pd.read_csv('survey1b.csv')
#raw_survey2a = pd.read_csv('survey2a.csv')
raw_survey2b = pd.read_csv('survey2b.csv')
# %%

survey1_text_origins = {
    1: False,
    2: False,
    3: True,
    4: False,
    5: True,
    6: True,
    7: False,
    8: False,
    9: False,
    10: True,
    11: True,
    12: True
}

survey2_text_origins = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False,
    7: True,
    8: True,
    9: True,
    10: True,
    11: True,
    12: True
}

def clean_column(col):
    if "trustworthy" in col:
        return "trustworthy"
    elif "credible" in col:
        return "credible"
    elif "confident" in col:
        return "confident"
    elif "Do you believe this content is AI generated? " in col:
        return "belief"
    else:
        return col.strip().lower().replace(" ", "_").replace("?", "")

def dedup_columns(columns):
    seen = {}
    new_cols = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            if col in ["trustworthy", "credible", "confident", "belief"]:
                seen[col] = 0
                new_cols.append(f"{col}_{seen[col]}")
            else:
                seen[col]=0
                new_cols.append(col)
    return new_cols


def data_cleaner(raw_df, survey_number=1, background_first=False):
    df = raw_df.copy()
    df.drop(columns=["Date submitted", "Start language", "Seed"], inplace=True)
    df.rename(columns={'Response ID': 'participant_id'}, inplace=True)
    df['participant_id'] = df['participant_id'].astype(str) + f"_{survey_number}" + ("a" if background_first else "b")
    df['background_first'] = background_first
    df['survey_number'] = survey_number
    cleaned_cols = [clean_column(col) for col in df.columns]
    df.columns = dedup_columns(cleaned_cols)
    df = df[df['do_you_agree_to_participate'] == 'Yes']
    df.drop(columns='do_you_agree_to_participate', inplace=True)

    return df

def convert_wide_to_long(wide_df, mapping, survey_number, background_first):
    # Transform the wide dataframe to long format
    df_long = pd.wide_to_long(wide_df,
                stubnames=['trustworthy', 'credible', 'confident', 'belief'],
                i='participant_id',
                j='text_number',
                sep="_").reset_index()

    # Adjust numbering and map text origins
    df_long["text_number"] += 1
    df_long["ai_generated"] = df_long["text_number"].map(mapping).astype(bool)
    df_long['text_number'] = df_long['text_number'].astype(str) + f"_{survey_number}" + ("a" if background_first else "b")
    df_long['belief'] = df_long['belief'].apply(lambda x: True if "Yes" else False)
    df_long['belief'] = df_long['belief'].astype(bool)
    return df_long


clean_survey1a = data_cleaner(raw_survey1a, survey_number=1, background_first=True)
#clean_survey1b = data_cleaner(raw_survey1b, survey_number=1, background_first=False)
#clean_survey2a = data_cleaner(raw_survey2a, survey_number=2, background_first=True)
clean_survey2b = data_cleaner(raw_survey2b, survey_number=2, background_first=False)

survey1a_long = convert_wide_to_long(clean_survey1a, survey1_text_origins, survey_number=1, background_first=True)
#survey1b_long = convert_wide_to_long(clean_survey1b, survey1_text_origins, survey_number=1, background_first=False)
#survey2a_long = convert_wide_to_long(clean_survey2a, survey2_text_origins, survey_number=2, background_first=True)
survey2b_long = convert_wide_to_long(clean_survey2b, survey2_text_origins, survey_number=2, background_first=False)
# %% ==========================================================================
# ========== Combine subject datasets together to form a long dataframe =======
# =============================================================================
trust_cols1 = [col for col in clean_survey1a.columns if 'trustworthy' in col]
credible_cols1 = [col for col in clean_survey1a.columns if 'credible' in col]
usage_cols1 = [col for col in clean_survey1a.columns if 'confident' in col]
belief_cols1 = [col for col in clean_survey1a.columns if 'believe' in col]
background_cols1 = [col for col in clean_survey1a.columns if col not in trust_cols1 + credible_cols1 + usage_cols1 + belief_cols1]

# Combine the long-form dataframes
combined_df = pd.concat([survey1a_long, survey2b_long], ignore_index=True)

df = combined_df.dropna(subset=['trustworthy', 'credible', 'confident', 'belief'])

# %% ==========================================================================
# ========== Do participants perform significantly above chance level? ========
# =============================================================================
df['correct_belief'] = df['ai_generated'] == df['belief']

k = sum(df['correct_belief'])
n = len(df)

print(k)
print(n)

result = binomtest(k, n, p=0.5, alternative='greater')
print("p-value:", result.pvalue)

# %% ==========================================================================
# ========== Participant-wise analysis ========================================
# =============================================================================
unique_participants = df['participant_id'].unique()

for participant in unique_participants:
    participant_df = df[df['participant_id'] == participant]
    k = sum(participant_df['correct_belief'])
    n = len(participant_df)
    print(n)
    result = binomtest(k, n, p=0.5, alternative='greater')
    print(f"Participant {participant}: p-value = {result.pvalue}")

# %%

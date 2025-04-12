# %% ==========================================================================
# ========== imports ==========================================================
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest
import seaborn as sns
import re

# %% ==========================================================================
# ========== read in raw surveys (must be in the same folder as this script) ==
# =============================================================================


raw_Survey1a = pd.read_csv('Survey1a.csv')
raw_Survey2a = pd.read_csv('Survey2a.csv')

# raw_Survey1b = pd.read_csv('Survey1b.csv')
# raw_Survey2b = pd.read_csv('Survey2b.csv')

# %% ==========================================================================
# ========== define mappings, data cleaner and processing function ============
# =============================================================================


# for survey 1:

# text 1, 2, 4, 7, 8, 9 are traditional 
# text 3, 5, 6, 10, 11, 12 are ai
# for survey 2:
# trad texts are 1,2,3,4,5,6
# ai texts are 7,8,9,10,11,12
# so surveyX_text_origins= ture means AI generated, false means traditional


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

#rename survey1a columns
survey1a_col_mapping = {


        "id. Response_ID": "id",
        "submitdate. Date_submitted": "submitdate",
        "lastpage. Last_page": "lastpage",
        "startlanguage. Start_language": "startlanguage",
        "seed. Seed": "seed",
        "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
        
          # Standard demographic/background questions for Survey 1a
            "G02Q02_SQ001. What_is_your_fa..__[Faculty_of_Phil.._]": "G02Q02_SQ001",
            "G02Q02_SQ002. What_is_your_fa..__[Faculty_of_Arts]": "G02Q02_SQ002",
            "G02Q02_SQ003. What_is_your_fa..__[School_of_Manag.._]": "G02Q02_SQ003",
            "G02Q02_SQ004. What_is_your_fa..__[Faculty_of_Medi.._]": "G02Q02_SQ004",
            "G02Q02_SQ005. What_is_your_fa..__[Faculty_of_Science]": "G02Q02_SQ005",
            "G02Q02_SQ006. What_is_your_fa..[Faculty_of_Law]": "G02Q02_SQ006",
            "G02Q02_SQ007. What_is_your_fa..__[Faculty_of_Soci.._]": "G02Q02_SQ007",
            "G02Q03. How_familiar_ar.._": "G02Q03",
            "G01Q04. How_often_do_yo.._": "G01Q04",
            "G01Q05. How_often_do_yo.._": "G01Q05",
            "G02Q06. How_much_do_you.._": "G02Q06",
            "G02Q07. How_much_do_you.._": "G02Q07",
            "G01Q08. How_often_do_yo.._": "G01Q08",
            "G02Q09.  __How_accurate.._": "G02Q09",
            "G02Q10. Have_you_ever_e.._": "G02Q10",
            "G01Q11. Regarding_the_q.._": "G01Q11",
            "G01Q12. Have_you_ever_e.._": "G01Q12",
            "G01Q13. Regarding_the_q.._": "G01Q13",
            "G02Q14. Is_there_anythi.._": "G02Q14",
        
        # Survey 1a Text mappings
        # Text 1
        "G03Q32. How_trustworthy.._": "Sv1a_T1_trustworthy",
        "G03Q15. How_credible_do.._": "Sv1a_T1_credible",
        "G03Q31. Would_you_feel_.._": "Sv1a_T1_confident",
        
        # Text 2
        "G03Q32Copy. How_trustworthy.._": "Sv1a_T2_trustworthy",
        "G03Q17. How_credible_do.._": "Sv1a_T2_credible",
        "G03Q31Copy. Would_you_feel_.._": "Sv1a_T2_confident",
        
        # Text 3
        "G03Q32CCopyCopy. How_trustworthy.._": "Sv1a_T3_trustworthy",
        "G03Q19. How_credible_do.._": "Sv1a_T3_credible",
        "G03Q20. Would_you_feel_.._": "Sv1a_T3_confident",
        
        # Text 4
        "G03Q32CopyCopy. How_trustworthy.._": "Sv1a_T4_trustworthy",
        "G03Q21. How_credible_do.._": "Sv1a_T4_credible",
        "G03Q31CC. Would_you_feel_.._": "Sv1a_T4_confident",
        
        # Text 5
        "G03Q32CC. How_trustworthy.._": "Sv1a_T5_trustworthy",
        "G03Q23. How_credible_do.._": "Sv1a_T5_credible",
        "G03Q24. Would_you_feel_.._": "Sv1a_T5_confident",
        
        # Text 6
        "G03Q32CCCopy. How_trustworthy.._": "Sv1a_T6_trustworthy",
        "G03Q25. How_credible_do.._": "Sv1a_T6_credible",
        "G03Q24Copy. Would_you_feel_.._": "Sv1a_T6_confident",
        
        # Text 7
        "G03Q32CopyCopyCopy. How_trustworthy.._": "Sv1a_T7_trustworthy",
        "G03Q27. How_credible_do.._": "Sv1a_T7_credible",
        "G03Q28. Would_you_feel_.._": "Sv1a_T7_confident",
        
        # Text 8
        "G03Q32C. How_trustworthy.._": "Sv1a_T8_trustworthy",
        "G03Q29. How_credible_do.._": "Sv1a_T8_credible",
        "G03Q30. Would_you_feel_.._": "Sv1a_T8_confident",
        
        # Text 9
        "G03Q32CCopy. How_trustworthy.._": "Sv1a_T9_trustworthy",
        "G03Qcopy. How_credible_do.._": "Sv1a_T9_credible",
        "G03Q30Copy. Would_you_feel_.._": "Sv1a_T9_confident",
        
        # Text 10
        "G03Q32CCC. How_trustworthy.._": "Sv1a_T10_trustworthy",
        "G03Q25Copy. How_credible_do.._": "Sv1a_T10_credible",
        "G03Q24CopyCopy. Would_you_feel_.._": "Sv1a_T10_confident",
        
        # Text 11
        "G03Q32CCCCopy. How_trustworthy.._": "Sv1a_T11_trustworthy",
        "G03Q25CopyCopy. How_credible_do.._": "Sv1a_T11_credible",
        "G03Q24C. Would_you_feel_.._": "Sv1a_T11_confident",
        
        # Text 12
        "G03Q32CCCC. How_trustworthy.._": "Sv1a_T12_trustworthy",
        "G03Q26CopyCopyCopy. How_credible_do.._": "Sv1a_T12_credible",
        "G03Q31CopyCopy. Would_you_feel_.._": "Sv1a_T12_confident",
        
        # Belief columns - mapping based on Round 2 text numbering
        "G03Q16. Do_you_believe_.._": "Sv1a_T1_belief",
        "G03Q16C. Do_you_believe_.._": "Sv1a_T7_belief",
        "G03Q18. Do_you_believe_.._": "Sv1a_T3_belief",
        "G03Q16Copy. Do_you_believe_.._": "Sv1a_T2_belief",
        "G03Q16CopyCopy. Do_you_believe_.._": "Sv1a_T4_belief",
        "G03Q26CopyCopy. Do_you_believe_.._": "Sv1a_T12_belief",
        "G03Q22. Do_you_believe_.._": "Sv1a_T10_belief",
        "G03Q16CCopy. Do_you_believe_.._": "Sv1a_T8_belief",
        "G03Q16CCopyCopy. Do_you_believe_.._": "Sv1a_T9_belief",
        "G03Q25CopyCopyCopy. Do_you_believe_.._": "Sv1a_T5_belief",
        "G03Q26. Do_you_believe_.._": "Sv1a_T6_belief",
        "G03Q26Copy. Do_you_believe_.._": "Sv1a_T11_belief"

}

survey2a_col_mapping= {
            "id. Response_ID": "id",
            "submitdate. Date_submitted": "submitdate",
            "lastpage. Last_page": "lastpage",
            "startlanguage. Start_language": "startlanguage",
            "seed. Seed": "seed",
            "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
            
            # Standard demographic/background questions for Survey 2a
            "G02Q02_SQ001. What_is_your_fa..__[Faculty_of_Phil.._]": "G02Q02_SQ001",
            "G02Q02_SQ002. What_is_your_fa..__[Faculty_of_Arts]": "G02Q02_SQ002",
            "G02Q02_SQ003. What_is_your_fa..__[School_of_Manag.._]": "G02Q02_SQ003",
            "G02Q02_SQ004. What_is_your_fa..__[Faculty_of_Medi.._]": "G02Q02_SQ004",
            "G02Q02_SQ005. What_is_your_fa..__[Faculty_of_Science]": "G02Q02_SQ005",
            "G02Q02_SQ006. What_is_your_fa..__[Faculty_of_Law]": "G02Q02_SQ006",
            "G02Q02_SQ007. What_is_your_fa..__[Faculty_of_Soci.._]": "G02Q02_SQ007",
            "G02Q03. How_familiar_ar.._": "G02Q03",
            "G01Q04. How_often_do_yo.._": "G01Q04",
            "G01Q05. How_often_do_yo.._": "G01Q05",
            "G02Q06. How_much_do_you.._": "G02Q06",
            "G02Q07. How_much_do_you.._": "G02Q07",
            "G01Q08. How_often_do_yo.._": "G01Q08",
            "G02Q09.  __How_accurate.._": "G02Q09",
            "G02Q10. Have_you_ever_e.._": "G02Q10",
            "G01Q11. Regarding_the_q.._": "G01Q11",
            "G01Q12. Have_you_ever_e.._": "G01Q12",
            "G01Q13. Regarding_the_q.._": "G01Q13",
            "G02Q14. Is_there_anythi.._": "G02Q14",
            
            # Survey 2a Text mappings
            # Text 1
            "G03Q32. How_trustworthy.._": "Sv2a_T1_trustworthy",
            "G03Q15. How_credible_do.._": "Sv2a_T1_credible",
            "G03Q31. Would_you_feel_.._": "Sv2a_T1_confident",
            
            # Text 2
            "G03Q32Copy. How_trustworthy.._": "Sv2a_T2_trustworthy",
            "G03Q17. How_credible_do.._": "Sv2a_T2_credible",
            "G03Q31Copy. Would_you_feel_.._": "Sv2a_T2_confident",
            
            # Text 3
            "G03Q19. How_credible_do.._": "Sv2a_T3_credible",
            "G03Q32CCopyCopy. How_trustworthy.._": "Sv2a_T3_trustworthy",
            "G03Q20. Would_you_feel_.._": "Sv2a_T3_confident",
            
            # Text 4
            "G03Q32CopyCopy. How_trustworthy.._": "Sv2a_T4_trustworthy",
            "G03Q21. How_credible_do.._": "Sv2a_T4_credible",
            "G03Q31CC. Would_you_feel_.._": "Sv2a_T4_confident",
            
            # Text 5
            "G03Q32CC. How_trustworthy.._": "Sv2a_T5_trustworthy",
            "G03Q23. How_credible_do.._": "Sv2a_T5_credible",
            "G03Q24. Would_you_feel_.._": "Sv2a_T5_confident",
            
            # Text 6
            "G03Q25CopyCopy. How_credible_do.._": "Sv2a_T6_credible",
            "G03Q32CCCCopy. How_trustworthy.._": "Sv2a_T6_trustworthy",
            "G03Q24C. Would_you_feel_.._": "Sv2a_T6_confident",
            
            # Text 7
            "G03Q32CopyCopyCopy. How_trustworthy.._": "Sv2a_T7_trustworthy",
            "G03Q27. How_credible_do.._": "Sv2a_T7_credible",
            "G03Q28. Would_you_feel_.._": "Sv2a_T7_confident",
            
            # Text 8
            "G03Q32C. How_trustworthy.._": "Sv2a_T8_trustworthy",
            "G03Q29. How_credible_do.._": "Sv2a_T8_credible",
            "G03Q30. Would_you_feel_.._": "Sv2a_T8_confident",
            
            # Text 9
            "G03Q32CCopy. How_trustworthy.._": "Sv2a_T9_trustworthy",
            "G03Qcopy. How_credible_do.._": "Sv2a_T9_credible",
            "G03Q30Copy. Would_you_feel_.._": "Sv2a_T9_confident",
            
            # Text 10
            "r154q0. How_credible_do.._": "Sv2a_T10_credible",
            "r563q0. How_trustworthy.._": "Sv2a_T10_trustworthy",
            "r693q0. Would_you_feel_.._": "Sv2a_T10_confident",
            
            # Text 11
            "r479q0. How_credible_do.._": "Sv2a_T11_credible",
            "r733q0. How_trustworthy.._": "Sv2a_T11_trustworthy",
            "r328q0. Would_you_feel_.._": "Sv2a_T11_confident",
            
            # Text 12
            "r938q0. How_credible_do.._": "Sv2a_T12_credible",
            "r259q0. How_trustworthy.._": "Sv2a_T12_trustworthy",
            "r882q0. Would_you_feel_.._": "Sv2a_T12_confident",
            
            # Belief columns for Survey 2a
            "G03Q16. Do_you_believe_.._": "Sv2a_T1_belief",
            "r895q0. Do_you_believe_.._": "Sv2a_T2_belief",
            "r781q0. Do_you_believe_.._": "Sv2a_T3_belief",
            "r198q0. Do_you_believe_.._": "Sv2a_T4_belief",
            "r857q0. Do_you_believe_.._": "Sv2a_T5_belief",
            "r572q0. Do_you_believe_.._": "Sv2a_T6_belief",
            "r928q0. Do_you_believe_.._": "Sv2a_T7_belief",
            "r778q0. Do_you_believe_.._": "Sv2a_T8_belief",
            "r877q0. Do_you_believe_.._": "Sv2a_T9_belief",
            "r213q0. Do_you_believe_.._": "Sv2a_T10_belief",
            "r78q0. Do_you_believe_.._": "Sv2a_T11_belief",
            "r91q0. Do_you_believe_.._": "Sv2a_T12_belief"
        }

survey1b_col_mapping= {}

survey2b_col_mapping= {}




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
# def dedup_columns(columns): the ideas is to add a number to the end of the column name if it is not unique


def data_cleaner(raw_df, column_mapping, survey_number=1, background_first=False):
    df = raw_df.copy()
    # rename columns according to the provided mapping
    
    
    df.rename(columns=column_mapping, inplace=True)
    df.drop(columns=["submitdate", "startlanguage", "seed"], inplace=True)
    df.rename(columns={'id': 'participant_id'}, inplace=True)
    df['participant_id'] = df['participant_id'].astype(str) + f"_{survey_number}" + ("a" if background_first else "b")
    df['background_first'] = background_first
    df['survey_number'] = survey_number
    cleaned_cols = [clean_column(col) for col in df.columns]
    df.columns = dedup_columns(cleaned_cols)
    df = df[df['do_you_agree_to_participate'] == 'Yes']
    df.drop(columns='do_you_agree_to_participate', inplace=True)

    return df

#here we print all the col names that are the samme in Survay1a and Survay2a


def convert_wide_to_long(wide_df, mapping, survey_number, background_first):
    # transform the wide dataframe to long format
    df_long = pd.wide_to_long(wide_df,
                stubnames=['trustworthy', 'credible', 'confident', 'belief'],
                i='participant_id',
                j='text_number',
                sep="_").reset_index()

    # adjust numbering and map text origins
    df_long["text_number"] += 1
    df_long["ai_generated"] = df_long["text_number"].map(mapping).astype(bool)
    df_long['text_number'] = df_long['text_number'].astype(str) + f"_{survey_number}" + ("a" if background_first else "b")
    df_long['belief'] = df_long['belief'].apply(lambda x: True if "Yes" else False)
    df_long['belief'] = df_long['belief'].astype(bool)
    return df_long


# clean_survey1a = data_cleaner(raw_survey1a, survey_number=1, background_first=True)       
# clean_survey1b = data_cleaner(raw_survey1b, survey_number=1, background_first=False)
# clean_survey2a = data_cleaner(raw_survey2a, survey_number=2, background_first=True)
# clean_survey2b = data_cleaner(raw_survey2b, survey_number=2, background_first=False)

clean_Survey1a = data_cleaner(raw_Survey1a, survey1a_col_mapping, survey_number=1, background_first=True)
clean_Survey2a = data_cleaner(raw_Survey2a, survey2a_col_mapping, survey_number=2, background_first=False)

Survey1a_long = convert_wide_to_long(clean_Survey1a, survey1_text_origins, survey_number=1, background_first=True)
Survey2a_long = convert_wide_to_long(clean_Survey2a, survey2_text_origins, survey_number=2, background_first=False)


# survey1a_long = convert_wide_to_long(clean_survey1a, survey1_text_origins, survey_number=1, background_first=True)
# survey1b_long = convert_wide_to_long(clean_survey1b, survey1_text_origins, survey_number=1, background_first=False)
# survey2a_long = convert_wide_to_long(clean_survey2a, survey2_text_origins, survey_number=2, background_first=True)
# survey2b_long = convert_wide_to_long(clean_survey2b, survey2_text_origins, survey_number=2, background_first=False) 

# %% ==========================================================================
# ========== combine subject datasets together to form a long dataframe =======
# =============================================================================

trust_cols1 = [col for col in clean_Survey1a.columns if 'trustworthy' in col]
credible_cols1 = [col for col in clean_Survey1a.columns if 'credible' in col]
usage_cols1 = [col for col in clean_Survey1a.columns if 'confident' in col]
belief_cols1 = [col for col in clean_Survey1a.columns if 'believe' in col]
background_cols1 = [col for col in clean_Survey1a.columns if col not in trust_cols1 + credible_cols1 + usage_cols1 + belief_cols1]

# combine the long-form dataframes
combined_df = pd.concat([Survey1a_long, Survey2a_long], ignore_index=True)  

df = combined_df.dropna(subset=['trustworthy', 'credible', 'confident', 'belief'])
print(f"Number of valid data observations: {len(df)}")
# %% ==========================================================================
# ========== do participants perform significantly above chance level? ========
# =============================================================================

df['correct_belief'] = df['ai_generated'] == df['belief']

k = sum(df['correct_belief'])
n = len(df)

print(k)
print(n)

result = binomtest(k, n, p=0.5, alternative='greater')
print("p-value:", result.pvalue)

# %% ==========================================================================
# ========== participant-wise analysis ========================================
# =============================================================================

unique_participants = df['participant_id'].unique()

for participant in unique_participants:
    participant_df = df[df['participant_id'] == participant]
    k = sum(participant_df['correct_belief'])
    n = len(participant_df)
    print(n)
    result = binomtest(k, n, p=0.5, alternative='greater')
    print(f"Participant {participant}: p-value = {result.pvalue}")

# %% ==========================================================================
# ========== compare trust-related metrics =====================================
# =============================================================================

# combine data from both surveys
all_data = pd.concat([Survey1a_long, Survey2a_long], ignore_index=True)

# debug information to understand the data
# print("Total rows in combined data:", len(all_data))
# print("Column names:", all_data.columns.tolist())
# print("Sample data:")
print(all_data[['participant_id', 'text_number', 'ai_generated', 'trustworthy', 'credible', 'confident', 'belief']].head())

# check data types and null values
print("\nData types:")
print(all_data.dtypes)
print("\nNull values per column:")
print(all_data.isnull().sum())

# this line is important to remove any rows with NaN values in the trust metrics
all_data = all_data.dropna(subset=['trustworthy', 'credible', 'confident', 'belief'])

print("\nAnalyzing trust metrics for all texts:")
print(f"Number of observations after dropping NaNs: {len(all_data)}")

# ensure trust metrics are numeric
all_data['trustworthy'] = pd.to_numeric(all_data['trustworthy'], errors='coerce')
all_data['credible'] = pd.to_numeric(all_data['credible'], errors='coerce')
all_data['confident'] = pd.to_numeric(all_data['confident'], errors='coerce')

# verify data ranges to ensure proper plotting
print("\nData ranges:")
print("Trustworthy:", all_data['trustworthy'].min(), "to", all_data['trustworthy'].max())
print("Credible:", all_data['credible'].min(), "to", all_data['credible'].max())
print("Confident:", all_data['confident'].min(), "to", all_data['confident'].max())

# create a long format dataframe for the trust metrics
trust_metrics = all_data.melt(
    id_vars=['participant_id', 'text_number', 'ai_generated'],
    value_vars=['trustworthy', 'credible', 'confident'],
    var_name='metric',
    value_name='rating'
)

# convert ratings to numeric (ensuring consistent data type)
trust_metrics['rating'] = pd.to_numeric(trust_metrics['rating'], errors='coerce')

# check the distribution of metrics in the melted dataframe
print("\nCount of each metric in long format:")
print(trust_metrics['metric'].value_counts())

# compare means across different trust metrics
print("\n--- Comparing different trust metrics ---")
for metric in ['trustworthy', 'credible', 'confident']:
    mean_value = all_data[metric].mean()
    print(f"Mean {metric} score: {mean_value:.2f}")

# paired t-tests between trust metrics
print("\n--- T-tests between trust metrics ---")
print("Trustworthy vs Credible:")
t_stat, p_val = scipy.stats.ttest_rel(all_data['trustworthy'], all_data['credible'])
print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")

print("\nTrustworthy vs Confident:")
t_stat, p_val = scipy.stats.ttest_rel(all_data['trustworthy'], all_data['confident'])
print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")

print("\nCredible vs Confident:")
t_stat, p_val = scipy.stats.ttest_rel(all_data['credible'], all_data['confident'])
print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")

# compare AI-generated vs real texts for each trust metric
print("\n--- Comparing AI-generated vs Real texts ---")
for metric in ['trustworthy', 'credible', 'confident']:
    ai_mean = all_data[all_data['ai_generated'] == True][metric].mean()
    real_mean = all_data[all_data['ai_generated'] == False][metric].mean()
    
    print(f"\nMetric: {metric}")
    print(f"AI-generated texts mean: {ai_mean:.2f}")
    print(f"Real texts mean: {real_mean:.2f}")
    
    t_stat, p_val = scipy.stats.ttest_ind(
        all_data[all_data['ai_generated'] == True][metric],
        all_data[all_data['ai_generated'] == False][metric]
    )
    print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")

# create visualizations with improved formatting
plt.figure(figsize=(14, 10))

# plot 1: compare means of trust metrics with error bars
plt.subplot(2, 2, 1)
sns.barplot(x='metric', y='rating', data=trust_metrics, errorbar=('ci', 95))
plt.title('Comparison of Trust Metrics', fontsize=12)
plt.ylim(0, 5)
plt.xlabel('Metric', fontsize=10)
plt.ylabel('Rating', fontsize=10)

# plot 2: compare AI vs Real texts for each metric with error bars
plt.subplot(2, 2, 2)
sns.barplot(x='metric', y='rating', hue='ai_generated', data=trust_metrics, errorbar=('ci', 95))
plt.title('Trust Metrics: AI vs Real Texts', fontsize=12)
plt.ylim(0, 5)
plt.legend(title='AI Generated', labels=['Real', 'AI'])
plt.xlabel('Metric', fontsize=10)
plt.ylabel('Rating', fontsize=10)

# plot 3: distribution of trust metrics
plt.subplot(2, 2, 3)
sns.boxplot(x='metric', y='rating', data=trust_metrics)
plt.title('Distribution of Trust Ratings', fontsize=12)
plt.xlabel('Metric', fontsize=10)
plt.ylabel('Rating', fontsize=10)

# plot 4: relationship between belief in AI generation and trust ratings
plt.subplot(2, 2, 4)
plt.title('Trust vs Belief in AI Generation', fontsize=12)

trust_with_belief = all_data.groupby(['participant_id', 'belief']).agg({
    'trustworthy': 'mean',
    'credible': 'mean',
    'confident': 'mean'
}).reset_index()

trust_belief_long = trust_with_belief.melt(
    id_vars=['participant_id', 'belief'],
    value_vars=['trustworthy', 'credible', 'confident'],
    var_name='metric',
    value_name='rating'
)
sns.boxplot(x='metric', y='rating', hue='belief', data=trust_belief_long)
plt.legend(title='Believed to be AI', labels=['No', 'Yes'])

plt.tight_layout()
plt.savefig('trust_analysis.png', dpi=300)
plt.show()

# save the processed data for further analysis
trust_metrics.to_csv('trust_metrics_processed.csv', index=False)
all_data.to_csv('all_trust_data_processed.csv', index=False)

# %%

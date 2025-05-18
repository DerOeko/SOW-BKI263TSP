# %% ==========================================================================
# ========== imports ==========================================================
# =============================================================================

# CHECK THIS AND THEN ANALYSIS https://docs.google.com/document/d/1oOQNnOSSosASuEkfXeORtZspPcvTdH6ULDFgknAPReo/edit?tab=t.0

# Survey 2a: Background questions in the back !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# https://tsp-c6.limesurvey.net/273257?lang=en

# Survey 1a: Backgorund questions in the front !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# https://tsp-c6.limesurvey.net/474256?lang=en

# Survey 2b: Backgorund questions in the front !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# https://levi11.limesurvey.net/353824?lang=en

# Survey 1b: Backgorund questions in the back !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# https://levi11.limesurvey.net/445568?lang=en



# for survey 1 :
# text 1, 2, 4, 7, 8, 9 are traditional 
# text 3, 5, 6, 10, 11, 12 are ai
# for survey 2 :
# trad texts are 1,2,3,4,5,6
# ai texts are 7,8,9,10,11,12
# so surveyX_text_origins= ture means AI generated, false means traditional


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# configure pandas pretty printing
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
import scipy
from scipy.stats import binomtest
import seaborn as sns
import re
import scipy.stats as stats
from scipy.stats import levene
import statsmodels.api as sm
import statsmodels.formula.api as smf


# %% ==========================================================================
# ========== read in raw surveys (must be in the same folder as this script) ==
# =============================================================================

raw_Survey1a = pd.read_csv('Survey1a.csv')
raw_Survey2a = pd.read_csv('Survey2a.csv')

raw_Survey1b = pd.read_csv('Survey1b.csv')
raw_Survey2b = pd.read_csv('Survey2b.csv')

# %% ==========================================================================
# ========== define mappings, data cleaner and processing function ============
# =============================================================================

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


        "id. Response_ID": "participant_id",
        "submitdate. Date_submitted": "submitdate",
        "lastpage. Last_page": "lastpage",
        "startlanguage. Start_language": "startlanguage",
        "seed. Seed": "seed",
        "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
        
          # Standard demographic/background questions for Survey 1a
            "G02Q02_SQ001. What_is_your_fa..__[Faculty_of_Phil.._]": "Faculty_of_Philosophy",
            "G02Q02_SQ002. What_is_your_fa..__[Faculty_of_Arts]": "Faculty_of_Arts",
            "G02Q02_SQ003. What_is_your_fa..__[School_of_Manag.._]": "School_of_Management",
            "G02Q02_SQ004. What_is_your_fa..__[Faculty_of_Medi.._]": "Faculty_of_Medicine",
            "G02Q02_SQ005. What_is_your_fa..__[Faculty_of_Science]": "Faculty_of_Science",
            "G02Q02_SQ006. What_is_your_fa..[Faculty_of_Law]": "Faculty_of_Law",
            "G02Q02_SQ007. What_is_your_fa..__[Faculty_of_Soci.._]": "Faculty_of_Social_Science",
            "G02Q03. How_familiar_ar.._": "Familiar_with_AI",
            "G01Q04. How_often_do_yo.._": "Tratditional_usage",
            "G01Q05. How_often_do_yo.._": "ChatGPT_usage_amount",
            "G02Q06. How_much_do_you.._": "trust_traditional",
            "G02Q07. How_much_do_you.._": "trust_ChatGPT",
            "G01Q08. How_often_do_yo.._": "doublechecking_ChatGPT",
            "G02Q09.  __How_accurate.._": "accuracy_ChatGPT_study",
            "G02Q10. Have_you_ever_e.._": "was_traditionaly_wrong",
            "G01Q11. Regarding_the_q.._": "G01Q11",
            "G01Q12. Have_you_ever_e.._": "was_ChatGPT_wrong",
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
            "id. Response_ID": "participant_id",
            "submitdate. Date_submitted": "submitdate",
            "lastpage. Last_page": "lastpage",
            "startlanguage. Start_language": "startlanguage",
            "seed. Seed": "seed",
            "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
            
            # Standard demographic/background questions for Survey 2a
            "G02Q02_SQ001. What_is_your_fa..__[Faculty_of_Phil.._]": "Faculty_of_Philosophy",
            "G02Q02_SQ002. What_is_your_fa..__[Faculty_of_Arts]": "Faculty_of_Arts",
            "G02Q02_SQ003. What_is_your_fa..__[School_of_Manag.._]": "School_of_Management",
            "G02Q02_SQ004. What_is_your_fa..__[Faculty_of_Medi.._]": "Faculty_of_Medicine",
            "G02Q02_SQ005. What_is_your_fa..__[Faculty_of_Science]": "Faculty_of_Science",
            "G02Q02_SQ006. What_is_your_fa..[Faculty_of_Law]": "Faculty_of_Law",
            "G02Q02_SQ007. What_is_your_fa..__[Faculty_of_Soci.._]": "Faculty_of_Social_Science",
            "G02Q03. How_familiar_ar.._": "Familiar_with_AI",
            "G01Q04. How_often_do_yo.._": "Tratditional_usage",
            "G01Q05. How_often_do_yo.._": "ChatGPT_usage_amount",
            "G02Q06. How_much_do_you.._": "trust_traditional",
            "G02Q07. How_much_do_you.._": "trust_ChatGPT",
            "G01Q08. How_often_do_yo.._": "doublechecking_ChatGPT",
            "G02Q09.  __How_accurate.._": "accuracy_ChatGPT_study",
            "G02Q10. Have_you_ever_e.._": "was_traditionaly_wrong",
            "G01Q11. Regarding_the_q.._": "G01Q11",
            "G01Q12. Have_you_ever_e.._": "was_ChatGPT_wrong",
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

survey1b_col_mapping= {
        "id. Response_ID": "participant_id",
        "submitdate. Date_submitted": "submitdate",
        "lastpage. Last_page": "lastpage",
        "startlanguage. Start_language": "startlanguage",
        "seed. Seed": "seed",
        "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
        
        # Standard demographic/background questions for Survey 1b
       "G02Q02_SQ001. What_is_your_fa..__[Faculty_of_Phil.._]": "Faculty_of_Philosophy",
        "G02Q02_SQ002. What_is_your_fa..__[Faculty_of_Arts]": "Faculty_of_Arts",
        "G02Q02_SQ003. What_is_your_fa..__[School_of_Manag.._]": "School_of_Management",
        "G02Q02_SQ004. What_is_your_fa..__[Faculty_of_Medi.._]": "Faculty_of_Medicine",
        "G02Q02_SQ005. What_is_your_fa..__[Faculty_of_Science]": "Faculty_of_Science",
        "G02Q02_SQ006. What_is_your_fa..[Faculty_of_Law]": "Faculty_of_Law",
        "G02Q02_SQ007. What_is_your_fa..__[Faculty_of_Soci.._]": "Faculty_of_Social_Science",
        "G02Q03. How_familiar_ar.._": "Familiar_with_AI",
        "G01Q04. How_often_do_yo.._": "Tratditional_usage",
        "G01Q05. How_often_do_yo.._": "ChatGPT_usage_amount",
        "G02Q06. How_much_do_you.._": "trust_traditional",
        "G02Q07. How_much_do_you.._": "trust_ChatGPT",
        "G01Q08. How_often_do_yo.._": "doublechecking_ChatGPT",
        "G02Q09.  __How_accurate.._": "accuracy_ChatGPT_study",
        "G02Q10. Have_you_ever_e.._": "was_traditionaly_wrong",
        "G01Q11. Regarding_the_q.._": "G01Q11",
        "G01Q12. Have_you_ever_e.._": "was_ChatGPT_wrong",
        "G01Q13. Regarding_the_q.._": "G01Q13",
        "G02Q14. Is_there_anythi.._": "G02Q14",
        
        # Survey 1b Text mappings
        # Text 1
        "G03Q32. How_trustworthy.._": "Sv1b_T1_trustworthy",
        "G03Q15. How_credible_do.._": "Sv1b_T1_credible",
        "G03Q31. Would_you_feel_.._": "Sv1b_T1_confident",
        
        # Text 7
        "G03Q32CopyCopyCopy. How_trustworthy.._": "Sv1b_T7_trustworthy",
        "G03Q27. How_credible_do.._": "Sv1b_T7_credible",
        "G03Q28. Would_you_feel_.._": "Sv1b_T7_confident",
        
        # Text 3
        "G03Q19. How_credible_do.._": "Sv1b_T3_credible",
        "G03Q32CCopyCopy. How_trustworthy.._": "Sv1b_T3_trustworthy",
        "G03Q20. Would_you_feel_.._": "Sv1b_T3_confident",
        
        # Text 2
        "G03Q32Copy. How_trustworthy.._": "Sv1b_T2_trustworthy",
        "G03Q17. How_credible_do.._": "Sv1b_T2_credible",
        "G03Q31Copy. Would_you_feel_.._": "Sv1b_T2_confident",
        
        # Text 4
        "G03Q32CopyCopy. How_trustworthy.._": "Sv1b_T4_trustworthy",
        "G03Q21. How_credible_do.._": "Sv1b_T4_credible",
        "G03Q31CC. Would_you_feel_.._": "Sv1b_T4_confident",
        
        # Text 12
        "G03Q32CCCC. How_trustworthy.._": "Sv1b_T12_trustworthy",
        "G03Q26CopyCopyCopy. How_credible_do.._": "Sv1b_T12_credible",
        "G03Q31CopyCopy. Would_you_feel_.._": "Sv1b_T12_confident",
        
        # Text 10
        "G03Q32CCC. How_trustworthy.._": "Sv1b_T10_trustworthy",
        "G03Q25Copy. How_credible_do.._": "Sv1b_T10_credible",
        "G03Q24CopyCopy. Would_you_feel_.._": "Sv1b_T10_confident",
        
        # Text 8
        "G03Q32C. How_trustworthy.._": "Sv1b_T8_trustworthy",
        "G03Q29. How_credible_do.._": "Sv1b_T8_credible",
        "G03Q30. Would_you_feel_.._": "Sv1b_T8_confident",
        
        # Text 9
        "G03Q32CCopy. How_trustworthy.._": "Sv1b_T9_trustworthy",
        "G03Qcopy. How_credible_do.._": "Sv1b_T9_credible",
        "G03Q30Copy. Would_you_feel_.._": "Sv1b_T9_confident",
        
        # Text 5
        "G03Q32CC. How_trustworthy.._": "Sv1b_T5_trustworthy",
        "G03Q23. How_credible_do.._": "Sv1b_T5_credible",
        "G03Q24. Would_you_feel_.._": "Sv1b_T5_confident",
        
        # Text 6
        "G03Q32CCCopy. How_trustworthy.._": "Sv1b_T6_trustworthy",
        "G03Q25. How_credible_do.._": "Sv1b_T6_credible",
        "G03Q24Copy. Would_you_feel_.._": "Sv1b_T6_confident",
        
        # Text 11
        "G03Q25CopyCopy. How_credible_do.._": "Sv1b_T11_credible",
        "G03Q32CCCCopy. How_trustworthy.._": "Sv1b_T11_trustworthy",
        "G03Q24C. Would_you_feel_.._": "Sv1b_T11_confident",
        
        # Belief columns for Survey 1b
        "G03Q16. Do_you_believe_.._": "Sv1b_T1_belief",
        "G03Q16C. Do_you_believe_.._": "Sv1b_T7_belief",
        "G03Q18. Do_you_believe_.._": "Sv1b_T3_belief",
        "G03Q16Copy. Do_you_believe_.._": "Sv1b_T2_belief",
        "G03Q16CopyCopy. Do_you_believe_.._": "Sv1b_T4_belief",
        "G03Q26CopyCopy. Do_you_believe_.._": "Sv1b_T12_belief",
        "G03Q22. Do_you_believe_.._": "Sv1b_T10_belief",
        "G03Q16CCopy. Do_you_believe_.._": "Sv1b_T8_belief",
        "G03Q16CCopyCopy. Do_you_believe_.._": "Sv1b_T9_belief",
        "G03Q25CopyCopyCopy. Do_you_believe_.._": "Sv1b_T5_belief",
        "G03Q26. Do_you_believe_.._": "Sv1b_T6_belief",
        "G03Q26Copy. Do_you_believe_.._": "Sv1b_T11_belief"
}

survey2b_col_mapping= {
        "id. Response_ID": "participant_id",
        "submitdate. Date_submitted": "submitdate",
        "lastpage. Last_page": "lastpage",
        "startlanguage. Start_language": "startlanguage",
        "seed. Seed": "seed",
        "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
        
        # Standard demographic/background questions for Survey 2b
        "G02Q02_SQ001. What_is_your_fa..__[Faculty_of_Phil.._]": "Faculty_of_Philosophy",
        "G02Q02_SQ002. What_is_your_fa..__[Faculty_of_Arts]": "Faculty_of_Arts",
        "G02Q02_SQ003. What_is_your_fa..__[School_of_Manag.._]": "School_of_Management",
        "G02Q02_SQ004. What_is_your_fa..__[Faculty_of_Medi.._]": "Faculty_of_Medicine",
        "G02Q02_SQ005. What_is_your_fa..__[Faculty_of_Science]": "Faculty_of_Science",
        "G02Q02_SQ006. What_is_your_fa..[Faculty_of_Law]": "Faculty_of_Law",
        "G02Q02_SQ007. What_is_your_fa..__[Faculty_of_Soci.._]": "Faculty_of_Social_Science",
        "G02Q03. How_familiar_ar.._": "Familiar_with_AI",
        "G01Q04. How_often_do_yo.._": "Tratditional_usage",
        "G01Q05. How_often_do_yo.._": "ChatGPT_usage_amount",
        "G02Q06. How_much_do_you.._": "trust_traditional",
        "G02Q07. How_much_do_you.._": "trust_ChatGPT",
        "G01Q08. How_often_do_yo.._": "doublechecking_ChatGPT",
        "G02Q09.  __How_accurate.._": "accuracy_ChatGPT_study",
        "G02Q10. Have_you_ever_e.._": "was_traditionaly_wrong",
        "G01Q11. Regarding_the_q.._": "G01Q11",
        "G01Q12. Have_you_ever_e.._": "was_ChatGPT_wrong",
        "G01Q13. Regarding_the_q.._": "G01Q13",
        "G02Q14. Is_there_anythi.._": "G02Q14",
        
        # Survey 2b Text mappings
        # Text 1
        "G03Q32. How_trustworthy.._": "Sv2b_T1_trustworthy",
        "G03Q15. How_credible_do.._": "Sv2b_T1_credible",
        "G03Q31. Would_you_feel_.._": "Sv2b_T1_confident",
        
        # Text 2
        "G03Q32Copy. How_trustworthy.._": "Sv2b_T2_trustworthy",
        "G03Q17. How_credible_do.._": "Sv2b_T2_credible",
        "G03Q31Copy. Would_you_feel_.._": "Sv2b_T2_confident",
        
        # Text 3
        "G03Q19. How_credible_do.._": "Sv2b_T3_credible",
        "G03Q32CCopyCopy. How_trustworthy.._": "Sv2b_T3_trustworthy",
        "G03Q20. Would_you_feel_.._": "Sv2b_T3_confident",
        
        # Text 4
        "G03Q32CopyCopy. How_trustworthy.._": "Sv2b_T4_trustworthy",
        "G03Q21. How_credible_do.._": "Sv2b_T4_credible",
        "G03Q31CC. Would_you_feel_.._": "Sv2b_T4_confident",
        
        # Text 5
        "G03Q32CC. How_trustworthy.._": "Sv2b_T5_trustworthy",
        "G03Q23. How_credible_do.._": "Sv2b_T5_credible",
        "G03Q24. Would_you_feel_.._": "Sv2b_T5_confident",
        
        # Text 6
        "G03Q25CopyCopy. How_credible_do.._": "Sv2b_T6_credible",
        "G03Q32CCCCopy. How_trustworthy.._": "Sv2b_T6_trustworthy",
        "G03Q24C. Would_you_feel_.._": "Sv2b_T6_confident",
        
        # Text 7
        "G03Q32CopyCopyCopy. How_trustworthy.._": "Sv2b_T7_trustworthy",
        "G03Q27. How_credible_do.._": "Sv2b_T7_credible",
        "G03Q28. Would_you_feel_.._": "Sv2b_T7_confident",
        
        # Text 8
        "G03Q32C. How_trustworthy.._": "Sv2b_T8_trustworthy",
        "G03Q29. How_credible_do.._": "Sv2b_T8_credible",
        "G03Q30. Would_you_feel_.._": "Sv2b_T8_confident",
        
        # Text 9
        "G03Q32CCopy. How_trustworthy.._": "Sv2b_T9_trustworthy",
        "G03Qcopy. How_credible_do.._": "Sv2b_T9_credible",
        "G03Q30Copy. Would_you_feel_.._": "Sv2b_T9_confident",
        
        # Text 10
        "r154q0. How_credible_do.._": "Sv2b_T10_credible",
        "r563q0. How_trustworthy.._": "Sv2b_T10_trustworthy",
        "r693q0. Would_you_feel_.._": "Sv2b_T10_confident",
        
        # Text 11
        "r479q0. How_credible_do.._": "Sv2b_T11_credible",
        "r733q0. How_trustworthy.._": "Sv2b_T11_trustworthy",
        "r328q0. Would_you_feel_.._": "Sv2b_T11_confident",
        
        # Text 12
        "r938q0. How_credible_do.._": "Sv2b_T12_credible",
        "r259q0. How_trustworthy.._": "Sv2b_T12_trustworthy",
        "r882q0. Would_you_feel_.._": "Sv2b_T12_confident",
        
        # Belief columns for Survey 2b
        "G03Q16. Do_you_believe_.._": "Sv2b_T1_belief",
        "r895q0. Do_you_believe_.._": "Sv2b_T2_belief",
        "r928q0. Do_you_believe_.._": "Sv2b_T7_belief",
        "r778q0. Do_you_believe_.._": "Sv2b_T8_belief",
        "r781q0. Do_you_believe_.._": "Sv2b_T3_belief",
        "r213q0. Do_you_believe_.._": "Sv2b_T10_belief",
        "r198q0. Do_you_believe_.._": "Sv2b_T4_belief",
        "r857q0. Do_you_believe_.._": "Sv2b_T5_belief",
        "r78q0. Do_you_believe_.._": "Sv2b_T11_belief",
        "r572q0. Do_you_believe_.._": "Sv2b_T6_belief",
        "r877q0. Do_you_believe_.._": "Sv2b_T9_belief",
        "r91q0. Do_you_believe_.._": "Sv2b_T12_belief"
}

def data_cleaner(
    df,
    column_mapping,
    survey_number,
    survey_text_origins=None,
    survey_prefix=None
):
    """
    Clean and transform survey data, then optionally add AI‑flagging and belief‑correction
    
    Parameters
    - df: DataFrame containing the survey data
    - column_mapping: dict mapping original column names to desired names
    - survey_number: int indicating the survey number
    - survey_text_origins: optional dict mapping text numbers to bool (AI vs traditional)
    - survey_prefix: optional string prefix for survey columns (eg "Sv2b")
    
    Returns
    - Cleaned and transformed DataFrame
    """
    # create a copy to avoid SettingWithCopyWarning
    result = df.copy()
    # apply name column mapping
    result.rename(columns=column_mapping, inplace=True)
    # filter out participants who did not agree to participate
    result = result[result["do_you_agree_to_participate"] == "Yes"]

    # filter out participants who did not complete the survey
    result = result.dropna(subset=["Faculty_of_Philosophy"])
    # drop irrelevant columns
    result = result.drop(columns=["submitdate", "startlanguage", "seed"])
    
    
    # build participant_id with suffix
    result["participant_id"] = result["participant_id"].astype(str) + f"_{survey_number}"
    print(survey_number)
    
    # drop participants with majority missing trust scores//so the participans that filled out NaN
    trust_cols = [f"{survey_prefix}_T{i}_trustworthy" for i in range(1, 13)]
    existing_trust_cols = [col for col in trust_cols if col in result.columns]
    result["trustworthy_nan_count"] = result[existing_trust_cols].isna().sum(axis=1)
    result = result[result["trustworthy_nan_count"] <= 2]
    result.drop(columns=["trustworthy_nan_count"], inplace=True)


    # add AI‑generated and correct belief columns if requested
    if survey_text_origins is not None and survey_prefix is not None:
        result = create_ai_generated_column(
            result,
            survey_text_origins,
            survey_prefix=survey_prefix
        )
        result = correct_belief(
            result,
            survey_prefix=survey_prefix
        )
    
    return result

# %% ==========================================================================
# ========== Calculate correct_belief column ===================================
# =============================================================================

def create_ai_generated_column(df, survey_text_origins, survey_prefix="Sv1a"):
    """
    Create ai_generated columns for each text in the survey
    
    Parameters:
    - df: DataFrame containing the survey data
    - survey_text_origins: Dict mapping text numbers to boolean (True if AI generated, False if traditional)
    - survey_prefix: String prefix used for column names (Sv1a, Sv1b, Sv2a, or Sv2b)
    
    Returns:
    - DataFrame with ai_generated columns added
    """
    # Create a copy of the DataFrame to ensure we're not working with a view
    result = df.copy()
    
    for i in range(1, 13):  
        column_name = f"{survey_prefix}_T{i}_ai_generated"
        if survey_text_origins[i]:
            result.loc[:, column_name] = True
        else:
            result.loc[:, column_name] = False

    return result

def correct_belief(df, survey_prefix="Sv1a"):
    """
    Create correct_belief columns for each text in the survey.
    
    For each text (1 to 12) a new column named '{survey_prefix}_T{i}_correct_belief' is created.
    A value is True if:
      - The AI-generated column equals "True" (as a string) and the belief column equals "Yes" (case-insensitive), or
      - The AI-generated column equals "False" and the belief column equals "No" (case-insensitive).
    Otherwise, the value is False.
    
    Parameters:
      df: DataFrame containing the survey data
      survey_prefix: A string such as "Sv1a", "Sv1b", "Sv2a" or "Sv2b"
      
    Returns:
      The DataFrame with new correct_belief columns added.
    """
    # Create a copy to avoid SettingWithCopyWarning
    result = df.copy()
    
    for i in range(1, 13):
        belief_col = f"{survey_prefix}_T{i}_belief"
        ai_generated_col = f"{survey_prefix}_T{i}_ai_generated"
        
        # Only process if both columns exist
        if belief_col in result.columns and ai_generated_col in result.columns:
            # Convert both to lowercase strings for comparison
            ai_generated_str = result[ai_generated_col].astype(str).str.strip().str.lower()
            belief_str = result[belief_col].astype(str).str.strip().str.lower()
            
            result.loc[:, f"{survey_prefix}_T{i}_correct_belief"] = (
                ((ai_generated_str == "true") & (belief_str == "yes")) |
                ((ai_generated_str == "false") & (belief_str == "no"))
            )
    correct_belief_cols = [f"{survey_prefix}_T{i}_correct_belief" for i in range(1, 13)]

    #count number of True values across the row, skipping NaNs
    result[f"{survey_prefix}_aggregated_correct_belief"] = result[correct_belief_cols].sum(axis=1, skipna=True)

    #print(result[[f"{survey_prefix}_correct_count"]])
    return result


# === After processing the individual survey DataFrames ===

df_1a = data_cleaner(
    raw_Survey1a,
    survey1a_col_mapping,
    survey_number="1a",
    survey_text_origins=survey1_text_origins,
    survey_prefix="Sv1a"
)

df_2a = data_cleaner(
    raw_Survey2a,
    survey2a_col_mapping,
    survey_number="2a",
    survey_text_origins=survey2_text_origins,
    survey_prefix="Sv2a"
)

df_1b = data_cleaner(
    raw_Survey1b,
    survey1b_col_mapping,
    survey_number="1b",
    survey_text_origins=survey1_text_origins,
    survey_prefix="Sv1b"
)

df_2b = data_cleaner(
    raw_Survey2b,
    survey2b_col_mapping,
    survey_number="2b",
    survey_text_origins=survey2_text_origins,
    survey_prefix="Sv2b"
)
df_1a['survey_type'] = '1a'
df_1b['survey_type'] = '1b'
df_2a['survey_type'] = '2a'
df_2b['survey_type'] = '2b'

# Combine for modeling
df_combined_long = pd.concat([df_1a, df_1b, df_2a, df_2b], ignore_index=True)

# %%==========================================================================
# ========== Printing the dataframes ===================================
# =============================================================================


print("df_1a head:")
print(df_1a.to_string())
print("df_2a head:")
print(df_2a.to_string())
print("df_1b head:")
print(df_1b.to_string())
print("df_2b head:")
print(df_2b.to_string())
print(f"df_1a shape: {df_1a.shape}")
print(f"df_2a shape: {df_2a.shape}")
print(f"df_1b shape: {df_1b.shape}")
print(f"df_2b shape: {df_2b.shape}")


# %%==========================================================================
# ========== Checking if the correct text belief rate exceeds 50% ===================================
# =============================================================================

# survey 1a
total_successes_1a = int(df_1a["Sv1a_aggregated_correct_belief"].sum())
total_trials_1a = len(df_1a) * 12
binom_test_result_1a = binomtest(total_successes_1a, total_trials_1a, p=0.5, alternative='greater')
print(f"Binomial test result for Survey 1a: {binom_test_result_1a}")

# survey 1b
total_successes_1b = int(df_1b["Sv1b_aggregated_correct_belief"].sum())
total_trials_1b = len(df_1b) * 12

binom_test_result_1b = binomtest(total_successes_1b, total_trials_1b, p=0.5, alternative='greater')
print(f"Binomial test result for Survey 1b: {binom_test_result_1b}")

# for survey 2a
total_successes_2a = int(df_2a["Sv2a_aggregated_correct_belief"].sum())
total_trials_2a = len(df_2a) * 12
binom_test_result_2a = binomtest(total_successes_2a, total_trials_2a, p=0.5, alternative='greater')
print(f"Binomial test result for Survey 2a: {binom_test_result_2a}")

# for survey 2b
total_successes_2b = int(df_2b["Sv2b_aggregated_correct_belief"].sum())
total_trials_2b = len(df_2b) * 12

binom_test_result_2b = binomtest(total_successes_2b, total_trials_2b, p=0.5, alternative='greater')
print(f"Binomial test result for Survey 2a: {binom_test_result_2b}")


# %% ==========================================================================
# ==========Finding background means// sd's /frequency distributions ===================================
# =============================================================================
def background_insights(df):
    df = df.copy()
    background_cols = [ "Familiar_with_AI", "Tratditional_usage", "ChatGPT_usage_amount",
    "trust_traditional", "trust_ChatGPT", "doublechecking_ChatGPT", "was_traditionaly_wrong",
    "was_ChatGPT_wrong"]
    df_bg = df[background_cols]

    categorical_vars = [ "was_traditionaly_wrong", "was_ChatGPT_wrong", "doublechecking_ChatGPT", "ChatGPT_usage_amount"]
    print("Type of list:", type(list))
    numeric_vars = list(set(df_bg.columns) - set(categorical_vars))    
    desc_numeric = df_bg[numeric_vars].describe().T[['mean', 'std']]
    freq_categorical = {}
    for col in categorical_vars:
        freq_categorical[col] = df_bg[col].value_counts(dropna=False)

    # Display results
    print("=== Numeric Variable Summary ===")
    print(desc_numeric)

    print("\n=== Frequency Distributions (Categorical Variables) ===")
    for col, dist in freq_categorical.items():
        print(f"\n{col}:")
        print(dist)

concatenated_df_front= pd.concat([df_1a, df_2b], ignore_index=True)

concatenated_df_back = pd.concat([df_1b, df_2a], ignore_index=True)

print('========BACK=======')
background_insights(concatenated_df_back)

print('========FRONT=======')
background_insights(concatenated_df_front)

# %% ==========================================================================
# ==========Finding means//SD'S for different text origins===================================
# =============================================================================

def survey_split_text_origin(df, prefix):
    """
    Splits survey 2 DataFrame into two:
    - One containing only traditional texts (T1–T6)
    - One containing only AI-generated texts (T7–T12)
    """
    if prefix in ['Sv2a', 'Sv2b']:
        trad_texts = [f"T{i}" for i in range(1, 7)]
        ai_texts = [f"T{i}" for i in range(7, 13)]
    else:
        trad_texts = [f"T{i}" for i in [1,2,4,7,8,9]]
        ai_texts = [f"T{i}" for i in [3,5,6,10,11,12]]
    # Build lists of full column names for each set
    trad_cols = [col for col in df.columns if any(f"{prefix}_{t}_" in col for t in trad_texts)]
    ai_cols = [col for col in df.columns if any(f"{prefix}_{t}_" in col for t in ai_texts)]

    # Also include participant identifiers or general info if needed
    id_cols = [col for col in df.columns if "participant_id" in col or "Familiar_with_AI" in col]

    df_trad = df[id_cols + trad_cols]
    df_ai = df[id_cols + ai_cols]

    return df_trad, df_ai

def survey_insights(df):
    numeric_cols = df.select_dtypes(include='number').drop(columns=[col for col in df.columns if col.endswith('_std')])

    overall_mean = numeric_cols.mean()
    overall_std = numeric_cols.std(ddof=1)

    summary_df = pd.DataFrame({
        'mean': overall_mean,
        'std': overall_std
    })
    return summary_df

def find_scores(df, survey_prefix, origin):
    """
    Function that finds trust, credibility, confidence and respective means for dataframe
    Parameters:
      df: DataFrame containing the survey data
      
    Returns:
      participant_scores: dictionary (currently) with the scores and their means
    """
    df_copy = df.copy()
    rows =[]
    if survey_prefix in ['Sv2a', 'Sv2b']:
        if origin == 'trad':
            text_nums = [1,2,3,4,5,6]
        else:
            text_nums = [7,8,9,10,11,12]
    else:
        if origin == 'trad':
            text_nums = [1,2,4,7,8,9]
        else:
            text_nums = [3,5,6,10,11,12]
    for participant_idx in range(df_copy.shape[0]): #for each participant
        trustworthy = []
        confident = []
        credible = []
        for text_num in text_nums: #for each text
            trustworthy_col = f"{survey_prefix}_T{text_num}_trustworthy"
            confident_col = f"{survey_prefix}_T{text_num}_confident"
            credible_col = f"{survey_prefix}_T{text_num}_credible"
            if trustworthy_col in df_copy.columns and confident_col in df_copy.columns and credible_col in df_copy.columns:
                trustworthy_int = df_copy.iloc[participant_idx][trustworthy_col]
                confident_int = df_copy.iloc[participant_idx][confident_col]
                credible_int = df_copy.iloc[participant_idx][credible_col]
                trustworthy.append(trustworthy_int)
                confident.append(confident_int)
                credible.append(credible_int)
        mean_trustworthy = np.mean(trustworthy) if trustworthy else np.nan
        std_trustworthy = np.std(trustworthy, ddof=1) if len(trustworthy) > 1 else np.nan
        
        mean_confident = np.mean(confident) if confident else np.nan
        std_confident = np.std(confident, ddof=1) if len(confident) > 1 else np.nan
        
        mean_credible = np.mean(credible) if credible else np.nan
        std_credible = np.std(credible, ddof=1) if len(credible) > 1 else np.nan
        
        participant_id = df_copy.iloc[participant_idx]["participant_id"]
        
        rows.append({
            "participant_id": participant_id,
            "trustworthy_mean": mean_trustworthy,
            "trustworthy_std": std_trustworthy,
            "confident_mean": mean_confident,
            "confident_std": std_confident,
            "credible_mean": mean_credible,
            "credible_std": std_credible
        })
    df_scores = pd.DataFrame(rows)
    return df_scores

df1a_trad, df1a_ai = survey_split_text_origin(df_1a, 'Sv1a')
df1b_trad, df1b_ai = survey_split_text_origin(df_1b, 'Sv1b')
df1a_trad_scores = find_scores(df1a_trad, 'Sv1a', 'trad')
df1a_ai_scores = find_scores(df1a_ai, 'Sv1a', 'ai')

df1b_trad_scores = find_scores(df1b_trad, 'Sv1b', 'trad')
df1b_ai_scores = find_scores(df1b_ai, 'Sv1b', 'ai')
    
df2a_trad, df2a_ai = survey_split_text_origin(df_2a, 'Sv2a')
df2b_trad, df2b_ai = survey_split_text_origin(df_2b, 'Sv2b')

df2a_trad_scores = find_scores(df2a_trad, 'Sv2a', 'trad')
df2a_ai_scores = find_scores(df2a_ai, 'Sv2a', 'ai')

df2b_trad_scores = find_scores(df2b_trad, 'Sv2b', 'trad')
df2b_ai_scores = find_scores(df2b_ai, 'Sv2b', 'ai')

concatenated_ai_df= pd.concat([df1a_ai_scores, df1b_ai_scores, df2a_ai_scores, df2b_ai_scores], ignore_index=True)

concatenated_trad_df= pd.concat([df1a_trad_scores, df1b_trad_scores, df2a_trad_scores, df2b_trad_scores], ignore_index=True)

stats_ai = survey_insights(concatenated_ai_df)
stats_trad = survey_insights(concatenated_trad_df)

print("=== Numeric Variable Text Origin AI Summary ===")
print(stats_ai)

print("=== Numeric Variable Text Origin TRADITIONAL Summary ===")
print(stats_trad)
# %% ==========================================================================
# ==========Checking whether background q's influence the answers===================================
# =============================================================================
df1a_ai_scores['question_order'] = 'front'
df2b_ai_scores['question_order'] = 'front'
df1b_ai_scores['question_order'] = 'back'
df2a_ai_scores['question_order'] = 'back'

all_scores = pd.concat([df1a_ai_scores, df1b_ai_scores, df2a_ai_scores, df2b_ai_scores], ignore_index=True)

for metric in ['trustworthy_mean', 'credible_mean', 'confident_mean']:
    sns.boxplot(data=all_scores, x='question_order', y=metric)
    plt.title(f"{metric.replace('_mean', '').capitalize()} by Question Order")
    plt.show()

#No social desireability, as the plots are roughly the same
# %% ==========================================================================
# ========== Checking normality and homogeneity of variance ===================================
# =============================================================================

df_combined = pd.merge(concatenated_ai_df, concatenated_trad_df, on='participant_id', suffixes=('_ai', '_trad'))
for metric in ['trustworthy_mean', 'credible_mean', 'confident_mean']:
    diff = df_combined[f"{metric}_ai"] - df_combined[f"{metric}_trad"]
    plt.figure(figsize=(6, 4))
    stats.probplot(diff.dropna(), dist="norm", plot=plt)
    plt.title(f"Q-Q Plot of Differences in {metric.replace('_mean', '').capitalize()} (AI - Trad)")
    plt.xlabel("Theoretical Quantiles (Normal Distribution)")
    plt.ylabel("Observed Quantiles (Sample Data)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

levene_stat, p_value = levene(concatenated_ai_df['trustworthy_mean'].dropna(), concatenated_trad_df['trustworthy_mean'].dropna())
print(f"Levene test statistic: {levene_stat}, p-value: {p_value}")

#normality and homogeneity of variance good for paired ttest

# %% ==========================================================================
# ==========Paired T test ===================================
# =============================================================================
df_concatenated = pd.concat([df_1a, df_2a, df_1b, df_2b], ignore_index=True)

# unifying correct count column
df_concatenated["correct_count"] = df_concatenated[
    [col for col in df_concatenated.columns if col.endswith("_aggregated_correct_belief")]
].bfill(axis=1).iloc[:, 0]
# Label participants who correctly identified 75% or more of the texts
df_concatenated["good_differentiator"] = df_concatenated["correct_count"] >= 9

df_concatenated["familiarity"] = df_concatenated[
    [col for col in df_concatenated.columns if "Familiar_with_AI" in col]
].bfill(axis=1).iloc[:, 0]

for metric in ['trustworthy_mean', 'credible_mean', 'confident_mean']:
    ai_scores = concatenated_ai_df[metric]
    trad_scores = concatenated_trad_df[metric]
    
    paired_data = pd.concat([ai_scores, trad_scores], axis=1).dropna()
    paired_data.columns = ['AI', 'Trad']  # rename for clarity
    
    t_stat, p_val = stats.ttest_rel(paired_data['AI'], paired_data['Trad'])
    print(f"Paired t-test for {metric}: t={t_stat:.4f}, p={p_val:.4f}")

# === Paired t-test for good differentiators only ===
good_ids = df_concatenated[df_concatenated['good_differentiator']]['participant_id']

ai_good = concatenated_ai_df[concatenated_ai_df['participant_id'].isin(good_ids)]
trad_good = concatenated_trad_df[concatenated_trad_df['participant_id'].isin(good_ids)]

for metric in ['trustworthy_mean', 'credible_mean', 'confident_mean']:
    paired = pd.merge(ai_good[['participant_id', metric]], trad_good[['participant_id', metric]],
                      on='participant_id', suffixes=('_ai', '_trad'))
    tstat, pval = stats.ttest_rel(paired[f'{metric}_ai'], paired[f'{metric}_trad'])
    print(f"[Good Differentiators] Paired t-test for {metric}: t={tstat:.4f}, p={pval:.4f}")
#No significant score differences, all p values > 0.05

#So this means that participants’ trust and perceived credibility do not differ strongly 
#between the two content sources, but their confidence might be somewhat affected

def create_long_df_for_belief_trust_plot(df, prefix):
    melted_trust = df.melt(
        id_vars=['participant_id'],
        value_vars=[f'{prefix}_T{i}_trustworthy' for i in range(1,13)],
        var_name='text', value_name='trustworthy'
    )
    melted_belief = df.melt(
        id_vars=['participant_id'],
        value_vars=[f'{prefix}_T{i}_belief' for i in range(1,13)],
        var_name='text', value_name='belief'
    )
    melted_ai = df.melt(
        id_vars=['participant_id'],
        value_vars=[f'{prefix}_T{i}_ai_generated' for i in range(1,13)],
        var_name='text', value_name='actual_ai'
    )

    # Clean text labels
    for melted in [melted_trust, melted_belief, melted_ai]:
        melted['text'] = melted['text'].str.extract(r'T(\d+)', expand=False)

    df_long = melted_trust.merge(melted_belief, on=['participant_id', 'text']) \
                          .merge(melted_ai, on=['participant_id', 'text'])
    df_long['belief'] = df_long['belief'].str.strip().str.lower()
    return df_long

# Create combined belief-trust dataset
df_long_1a = create_long_df_for_belief_trust_plot(df_1a, "Sv1a")
df_long_1b = create_long_df_for_belief_trust_plot(df_1b, "Sv1b")
df_long_2a = create_long_df_for_belief_trust_plot(df_2a, "Sv2a")
df_long_2b = create_long_df_for_belief_trust_plot(df_2b, "Sv2b")

df_belief_trust = pd.concat([df_long_1a, df_long_1b, df_long_2a, df_long_2b], ignore_index=True)

# Normalize belief values for consistent grouping
df_belief_trust['belief_normalized'] = df_belief_trust['belief'].map({
    'yes': 'Believed AI',
    'no': 'Believed Traditional'
})

# Drop missing trust or belief
df_belief_trust = df_belief_trust.dropna(subset=['trustworthy', 'belief_normalized'])

# Plot
plt.figure(figsize=(8, 6))
sns.boxplot(data=df_belief_trust, x='belief_normalized', y='trustworthy')
plt.title("Trust Ratings by Belief About Authorship")
plt.xlabel("Belief About Authorship")
plt.ylabel("Trust Rating")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
# %% ==========================================================================
# ========== Cohen's D ===================================
# =============================================================================
def cohen_d_paired(diff_series):
    diff = diff_series.dropna()
    mean_diff = diff.mean()
    std_diff = diff.std(ddof=1)
    return mean_diff / std_diff if std_diff != 0 else float('nan')

diffs = concatenated_ai_df[['trustworthy_mean', 'credible_mean', 'confident_mean']] - \
        concatenated_trad_df[['trustworthy_mean', 'credible_mean', 'confident_mean']]

for metric in ['trustworthy_mean', 'credible_mean', 'confident_mean']:
    d = cohen_d_paired(diffs[metric])
    print(f"Cohen's d for {metric.replace('_mean','')}: {d:.3f}")

#Not a really significant cohen's D score as everything is belove <0.5

# %% ==========================================================================
#==== Multiple regression model ========================================
# =============================================================================

def multiple_regression_model_with_background(df, survey_prefix):
    # melt trust, cred, conf, belief and ai flags into long form
    df_trust = df.melt(
        id_vars=['participant_id'],
        value_vars=[f'{survey_prefix}_T{i}_trustworthy'   for i in range(1,13)],
        var_name='text', value_name='trustworthy'
    )
    df_cred  = df.melt( id_vars=['participant_id'],
                        value_vars=[f'{survey_prefix}_T{i}_credible'     for i in range(1,13)],
                        var_name='text', value_name='credible')
    df_conf  = df.melt( id_vars=['participant_id'],
                        value_vars=[f'{survey_prefix}_T{i}_confident'    for i in range(1,13)],
                        var_name='text', value_name='confident')
    df_bel   = df.melt( id_vars=['participant_id'],
                        value_vars=[f'{survey_prefix}_T{i}_belief'       for i in range(1,13)],
                        var_name='text', value_name='belief')
    df_ai    = df.melt( id_vars=['participant_id'],
                        value_vars=[f'{survey_prefix}_T{i}_ai_generated' for i in range(1,13)],
                        var_name='text', value_name='ai_generated')

    # strip the “Sv2a_” prefix so you can merge on just “text”
    for df_ in (df_trust, df_cred, df_conf, df_bel, df_ai):
        df_['text'] = df_['text'].str.replace(r'^' + survey_prefix + r'_T(\d+)_.+$', r'T\1', regex=True)
    # merge them all
    df_long = (df_trust
            .merge(df_cred,  on=['participant_id','text'])
            .merge(df_conf,  on=['participant_id','text'])
            .merge(df_bel,   on=['participant_id','text'])
            .merge(df_ai,    on=['participant_id','text'])
    )

    # Merge background questions
    background_cols = ["trust_traditional", "trust_ChatGPT", "doublechecking_ChatGPT", "was_traditionaly_wrong", "was_ChatGPT_wrong", "Familiar_with_AI"]
    df_long = df_long.merge(df[['participant_id'] + background_cols].drop_duplicates(subset=['participant_id']), on='participant_id', how='left')

    # now run one regression for every row
    formula = 'trustworthy ~ credible + confident + belief + ai_generated + trust_traditional + trust_ChatGPT + doublechecking_ChatGPT + was_traditionaly_wrong + was_ChatGPT_wrong + Familiar_with_AI'
    model = smf.ols(formula=formula, data=df_long).fit()
    
    return model

def create_long_df_for_modeling(df, survey_prefix):
    df_trust = df.melt(id_vars=['participant_id'], value_vars=[f'{survey_prefix}_T{i}_trustworthy' for i in range(1,13)], var_name='text', value_name='trustworthy')
    df_cred  = df.melt(id_vars=['participant_id'], value_vars=[f'{survey_prefix}_T{i}_credible' for i in range(1,13)], var_name='text', value_name='credible')
    df_conf  = df.melt(id_vars=['participant_id'], value_vars=[f'{survey_prefix}_T{i}_confident' for i in range(1,13)], var_name='text', value_name='confident')
    df_bel   = df.melt(id_vars=['participant_id'], value_vars=[f'{survey_prefix}_T{i}_belief' for i in range(1,13)], var_name='text', value_name='belief')
    df_ai    = df.melt(id_vars=['participant_id'], value_vars=[f'{survey_prefix}_T{i}_ai_generated' for i in range(1,13)], var_name='text', value_name='ai_generated')

    for df_ in (df_trust, df_cred, df_conf, df_bel, df_ai):
        df_['text'] = df_['text'].str.replace(r'^' + survey_prefix + r'_T(\d+)_.+$', r'T\1', regex=True)

    df_long = df_trust.merge(df_cred, on=['participant_id','text']) \
                      .merge(df_conf, on=['participant_id','text']) \
                      .merge(df_bel,  on=['participant_id','text']) \
                      .merge(df_ai,   on=['participant_id','text'])

    background_cols = ["trust_traditional", "trust_ChatGPT", "doublechecking_ChatGPT", "was_traditionaly_wrong", "was_ChatGPT_wrong", "Familiar_with_AI", "survey_type"]
    df_long = df_long.merge(df[['participant_id'] + background_cols].drop_duplicates(), on='participant_id', how='left')

    return df_long
df_long_all = pd.concat([
    create_long_df_for_modeling(df_1a, 'Sv1a'),
    create_long_df_for_modeling(df_1b, 'Sv1b'),
    create_long_df_for_modeling(df_2a, 'Sv2a'),
    create_long_df_for_modeling(df_2b, 'Sv2b')
], ignore_index=True)

# Run regression with interaction to check if survey type influences effect of ai_generated
model_with_interaction = smf.ols(
    'trustworthy ~ ai_generated * survey_type + credible + confident + belief + trust_traditional + trust_ChatGPT + doublechecking_ChatGPT + was_traditionaly_wrong + was_ChatGPT_wrong + Familiar_with_AI',
    data=df_long_all
).fit()
print(model_with_interaction.summary())
    
# %%=========================================================================
# ==========Multiple regression model per participant to compare to background questions ===================================
# =============================================================================


def analyze_single_participant_with_background(df, participant_id, survey_prefix):
    df_single_participant = df[df['participant_id'] == participant_id].copy()
    model_single_participant = multiple_regression_model_with_background(df_single_participant, str(survey_prefix))
    print(f"\nRegression results for participant {participant_id} ({survey_prefix}):")
    print(model_single_participant.summary())
    # Extract background questions
    background =   df_single_participant[["trust_traditional","trust_ChatGPT", "doublechecking_ChatGPT", "was_traditionaly_wrong", "was_ChatGPT_wrong","Familiar_with_AI"]].iloc[0] # Take the first row as background is constant for a participant
    print("\nBackground questions:")
    print(background)

# Assuming you have your DataFrames df_1a, df_1b, df_2a, df_2b loaded
# Example usage for analyzing a single participant with the background in the regression:
print("\nRunning multiple regression model with background (example for participant 3_1a)...")
model_df_1a_with_background = multiple_regression_model_with_background(df_1a, "Sv1a")
model_df_2a_with_background = multiple_regression_model_with_background(df_2a, "Sv2a")
model_df_1b_with_background = multiple_regression_model_with_background(df_1b, "Sv1b")
model_df_2b_with_background = multiple_regression_model_with_background(df_2b, "Sv2b")


print(model_df_1a_with_background.summary())
print(model_df_2a_with_background.summary())
print(model_df_1b_with_background.summary())
print(model_df_2b_with_background.summary())

print("\nAnalyzing single participant with background...")
print(analyze_single_participant_with_background(df_1a, "3_1a", "Sv1a"))
# %%=========================================================================
# ========== Plotting background against performance of correct belief ====================================
# =============================================================================
df_concatenated = pd.concat([df_1a, df_2a, df_1b, df_2b], ignore_index=True)

# unifying correct count column
df_concatenated["correct_count"] = df_concatenated[
    [col for col in df_concatenated.columns if col.endswith("_aggregated_correct_belief")]
].bfill(axis=1).iloc[:, 0]
# Label participants who correctly identified 75% or more of the texts
df_concatenated["good_differentiator"] = df_concatenated["correct_count"] >= 9

df_concatenated["familiarity"] = df_concatenated[
    [col for col in df_concatenated.columns if "Familiar_with_AI" in col]
].bfill(axis=1).iloc[:, 0]

plt.figure(figsize=(10, 6))
plt.scatter(df_concatenated["familiarity"], df_concatenated["correct_count"], alpha=0.5)
sns.regplot(x="familiarity", y="correct_count", data=df_concatenated, scatter=False, color='red')
plt.xlabel("Familiarity with AI")
plt.ylabel("Correct Belief Count")
plt.title("Familiarity with AI vs. Correct Belief Count")
plt.show()




# %% ==========================================================================
# ========== RAF AND FERDI TESTS LEAVE===================================
# =============================================================================

def correlate_trust_usage(df, survey_prefix):
    """
    Correlating the trust in a text and the confidence of the participant in using it in an essay
    Does so by collecting for all the texts per participant the trust and confidence in the text
    Next we find the corr_score which is the correlation score: trust-confidence and the average.
    we find the means of these per participant, if mean_abs_trust_conf_diff is close to 0, the 
    participant has a good correlational level over all texts, mean_trust_conf_avg indicates the mean of the trust
    and confidence level combined over all texts

    Parameters:
      df: DataFrame containing the survey data
      survey_prefix: A string such as "Sv1a", "Sv1b", "Sv2a" or "Sv2b"
      
    Returns:
      new resulting dataframe
    """
    result = df.copy()

    agg_corr_trust_conf_per_participant = []
    agg_average_trust_conf_per_partcipant = []
    for participant_idx in range(result.shape[0]): #for each participant
        agg_corr_trust_conf = []
        agg_average_trust_conf = []
        for text_num in range(1, 13): #for each text
            trustworthy_col = f"{survey_prefix}_T{text_num}_trustworthy"
            confident_col = f"{survey_prefix}_T{text_num}_confident"
            if trustworthy_col in result.columns and confident_col in result.columns:
                trustworthy_int = result.iloc[participant_idx][trustworthy_col]
                confident_int = result.iloc[participant_idx][confident_col]
                #print(f"Participant {participant_idx + 1}, Text {text_num} → Trustworthy: {trustworthy_int}, Confident: {confident_int}")
                corr_score = trustworthy_int - confident_int
                corr_average = (trustworthy_int + trustworthy_int) /2
                agg_corr_trust_conf.append(corr_score)
                agg_average_trust_conf.append(corr_average)
        mean_score = np.mean([abs(x) for x in agg_corr_trust_conf])
        mean_combined = np.mean(agg_average_trust_conf)
        agg_corr_trust_conf_per_participant.append(mean_score)
        agg_average_trust_conf_per_partcipant.append(mean_combined)

    result["mean_abs_trust_conf_diff"] = agg_corr_trust_conf_per_participant #currently i add columns here you do it differently ferdi?
    result["mean_trust_conf_avg"] = agg_average_trust_conf_per_partcipant 
    return result
# %%=========================================================================
# ========== Test text performance over all essays  ===================================
# =============================================================================

# so check if a text is guessed correctly / incorrectly often or not 
def test_text_performance(df):
    # create a dict to store the correct counts
    text_performance = {}

    for i in range(1, 13):
        col_suffix = f"T{i}_correct_belief"
        matching_column = [col for col in df.columns if col.endswith(col_suffix)]
        
        if matching_column:
            col = matching_column[0]
            correct_count_in_precent = df[col].sum() / len(df[col])
            text_performance[f"Text_{i}"] = correct_count_in_precent

            incorrect_count = len(df) - df[col].sum()
            # print(f"Text {i}: Correct beliefs: {correct_count_in_precent}, Incorrect beliefs: {incorrect_count}")

    # convert to a DataFrame with one row and texts as columns
    df_text_performance = pd.DataFrame([text_performance])
    # print(df_text_performance)
    return df_text_performance
    

        


print(test_text_performance(df_1a))
print(test_text_performance(df_2a))

def combinded_text_perfomace_by_a_b(df_1a, df_2a):
    # create a dict to store the correct counts
    text_performance = {}

    for i in range(1, 13):
        col_suffix = f"T{i}_correct_belief"
        matching_column = [col for col in df_1a.columns if col.endswith(col_suffix)]
        
        if matching_column:
            col = matching_column[0]
            correct_count_in_precent = df_1a[col].sum() / len(df_1a[col])
            text_performance[f"Text_{i}"] = correct_count_in_precent

            incorrect_count = len(df_1a) - df_1a[col].sum()
            # print(f"Text {i}: Correct beliefs: {correct_count_in_precent}, Incorrect beliefs: {incorrect_count}")

    # convert to a DataFrame with one row and texts as columns
    df_text_performance = pd.DataFrame([text_performance])
    # print(df_text_performance)
    return df_text_performance
print(combinded_text_perfomace_by_a_b(df_1a, df_2a))
print(combinded_text_perfomace_by_a_b(df_1b, df_2b))

# %%=========================================================================
# ========== Finding the scores for trust,cred,conf ===================================
# =============================================================================
def find_scores(df, survey_prefix):
    """
    Function that finds trust, credibility, confidence and respective means for dataframe
    Parameters:
      df: DataFrame containing the survey data
      
    Returns:
      participant_scores: dictionary (currently) with the scores and their means
    """
    df_copy = df.copy()
    participant_scores = {}

    for participant_idx in range(df_copy.shape[0]): #for each participant
        trustworthy = []
        confident = []
        credible = []
        for text_num in range(1, 13): #for each text
            trustworthy_col = f"{survey_prefix}_T{text_num}_trustworthy"
            confident_col = f"{survey_prefix}_T{text_num}_confident"
            credible_col = f"{survey_prefix}_T{text_num}_credible"
            if trustworthy_col in df_copy.columns and confident_col in df_copy.columns and credible_col in df_copy.columns:
                trustworthy_int = df_copy.iloc[participant_idx][trustworthy_col]
                confident_int = df_copy.iloc[participant_idx][confident_col]
                credible_int = df_copy.iloc[participant_idx][credible_col]
                trustworthy.append(trustworthy_int)
                confident.append(confident_int)
                credible.append(credible_int)
        mean_trustworthy = np.mean(trustworthy)
        mean_confident = np.mean(confident)
        mean_credible = np.mean(credible)
        participant_id = df_copy.iloc[participant_idx]["participant_id"]
        participant_scores[participant_id] = {
        "trustworthy": {
            "values": trustworthy,
            "mean": mean_trustworthy
        },
        "confident": {
            "values": confident,
            "mean": mean_confident
        },
        "credible": {
            "values": credible,
            "mean": mean_credible
        }
    }
    return participant_scores




"""
1. Trustworthiness, Credibility, Confidence by Question Order (first 3 plots)
- Compared whether belief questions were shown at the front or back of the survey.
- Observation:
    • Slightly higher medians in the 'back' condition across all three metrics.
    • Suggests possible priming or order effects on trust, credibility, and confidence.

2. Q-Q Plots of Differences Between AI and Traditional Texts (plots 4-6)
- Q-Q plots for trustworthy_mean, credible_mean, and confident_mean differences (AI - Traditional).
- Observation:
    • Data points fall mostly along the diagonal.
    • Differences are approximately normally distributed.
    • Justifies the use of paired t-tests.

3. Paired t-Tests and Cohen's d (Effect Sizes)
| Variable     | t-value | p-value | Cohen’s d | Interpretation                  |
|--------------|---------|---------|-----------|---------------------------------|
| Trustworthy  |  0.43   |  0.671  |   0.078   | 🟦 No significant difference     |
| Credible     |  0.96   |  0.347  |   0.178   | 🟦 No significant difference     |
| Confident    |  1.93   |  0.064  |   0.358   | 🟨 Trend toward higher confidence in AI texts - we could maybe say it's kinda significant - 0.05 is a hard margin by the scientific community, but as we have seen on Bayesian, this can be arbitrary, so 0.064 is acceptable we think.


4. Trust Ratings by Belief About Authorship
- Compared trust ratings between texts participants believed were AI vs. traditional.
- Observation:
    • Median trust higher for texts believed to be traditional.
    • Belief influences trust more than actual authorship.

5. Familiarity with AI vs. Belief Accuracy
- Explored whether AI familiarity predicted correct identification of AI-generated texts.
- Observation:
    • Weak negative trend (slope slightly downward).
    • No strong correlation—familiarity doesn’t improve detection accuracy.

6. Multiple Regression Model (trustworthy as DV)
- Predictors included: credible, confident, belief, ai_generated, trust variables, and familiarity.
- Key findings:
    • credible and confident were strong and significant predictors of trust.
    • ai_generated and belief had no significant effects.
    • Interaction term (ai_generated * survey_type) not significant.

Overall Summary:
- Trust ratings were not driven by actual authorship (AI vs. traditional).
- Beliefs about authorship and perceived credibility/confidence mattered more.
- Question order showed weak trends but no strong effects.
- Familiarity with AI did not improve authorship identification ability.
"""
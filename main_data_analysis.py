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


raw_Survey1a = pd.read_csv('file:///Users/ferdinandpaar/Library/Mobile%20Documents/com~apple~CloudDocs/AI_Bachelor/Year_2/TSP_Team_Science_Project/TSP_Data_analysis/SOW-BKI263TSP/Survey1a.csv')
raw_Survey2a = pd.read_csv('file:///Users/ferdinandpaar/Library/Mobile%20Documents/com~apple~CloudDocs/AI_Bachelor/Year_2/TSP_Team_Science_Project/TSP_Data_analysis/SOW-BKI263TSP/Survey2a.csv')


raw_Survey1b = pd.read_csv('file:///Users/ferdinandpaar/Library/Mobile%20Documents/com~apple~CloudDocs/AI_Bachelor/Year_2/TSP_Team_Science_Project/TSP_Data_analysis/SOW-BKI263TSP/Survey1b.csv')
raw_Survey2b = pd.read_csv('file:///Users/ferdinandpaar/Library/Mobile%20Documents/com~apple~CloudDocs/AI_Bachelor/Year_2/TSP_Team_Science_Project/TSP_Data_analysis/SOW-BKI263TSP/Survey2b.csv')

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

survey1b_col_mapping= {
        "id. Response_ID": "id",
        "submitdate. Date_submitted": "submitdate",
        "lastpage. Last_page": "lastpage",
        "startlanguage. Start_language": "startlanguage",
        "seed. Seed": "seed",
        "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
        
        # Standard demographic/background questions for Survey 1b
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
        "id. Response_ID": "id",
        "submitdate. Date_submitted": "submitdate",
        "lastpage. Last_page": "lastpage",
        "startlanguage. Start_language": "startlanguage",
        "seed. Seed": "seed",
        "Q00. Do_you_agree_to.._": "do_you_agree_to_participate",
        
        # Standard demographic/background questions for Survey 2b
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
    background_first,
    survey_text_origins=None,
    survey_prefix=None
):
    """
    Clean and transform survey data, then optionally add AI‑flagging and belief‑correction
    
    Parameters
    - df: DataFrame containing the survey data
    - column_mapping: dict mapping original column names to desired names
    - survey_number: int indicating the survey number
    - background_first: bool indicating whether background questions were first
    - survey_text_origins: optional dict mapping text numbers to bool (AI vs traditional)
    - survey_prefix: optional string prefix for survey columns (eg "Sv2b")
    
    Returns
    - Cleaned and transformed DataFrame
    """
    # create a copy to avoid SettingWithCopyWarning
    result = df.copy()
    
    # apply column mapping
    result.rename(columns=column_mapping, inplace=True)
    result = result.drop(columns=["submitdate", "startlanguage", "seed"])
    # drop rows with any missing values
    result = result.dropna()
    
    # ensure participant_id exists
    if 'participant_id' not in result.columns:
        if 'PROLIFIC_PID' in result.columns:
            result['participant_id'] = result['PROLIFIC_PID']
        else:
            result['participant_id'] = result.index.astype(str)
    
    # tweak participant_id and add metadata
    pid_suffix = f"_{survey_number}" + ("a" if background_first else "b")
    result.loc[:, 'participant_id'] = result['participant_id'].astype(str) + pid_suffix
    result.loc[:, 'background_first'] = background_first
    result.loc[:, 'survey_number'] = survey_number
    
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
            print(f"Correct belief for {survey_prefix}_T{i}: {result[f'{survey_prefix}_T{i}_correct_belief'].values}")
    return result


# === After processing the individual survey DataFrames ===

df_1a = data_cleaner(
    raw_Survey1a,
    survey1a_col_mapping,
    survey_number=1,
    background_first=True,
    survey_text_origins=survey1_text_origins,
    survey_prefix="Sv1a"
)

df_2a = data_cleaner(
    raw_Survey2a,
    survey2a_col_mapping,
    survey_number=2,
    background_first=False,
    survey_text_origins=survey2_text_origins,
    survey_prefix="Sv2a"
)

df_1b = data_cleaner(
    raw_Survey1b,
    survey1b_col_mapping,
    survey_number=1,
    background_first=False,
    survey_text_origins=survey1_text_origins,
    survey_prefix="Sv1b"
)

df_2b = data_cleaner(
    raw_Survey2b,
    survey2b_col_mapping,
    survey_number=2,
    background_first=True,
    survey_text_origins=survey2_text_origins,
    survey_prefix="Sv2b"
)
# For Survey 1a:
# Create a new column aggregating correct answers from all texts
df_1a["aggregated_correct_belief"] = df_1a.filter(like="_correct_belief").sum(axis=1)

# Total correct responses across all participants:
total_successes_1a = int(df_1a["aggregated_correct_belief"].sum())
# Total trials is the number of participants multiplied by 12
total_trials_1a = len(df_1a) * 12


from scipy.stats import binomtest
# Example hypothesis: testing if the correct response rate exceeds 50%
binom_test_result_1a = binomtest(total_successes_1a, total_trials_1a, 0.5, alternative='greater')
# print(f"Binomial test result for Survey 1a: {binom_test_result_1a}")

# For Survey 2a (make sure to use df_2a, not df_2b):
df_2a["aggregated_correct_belief"] = df_2a.filter(like="_correct_belief").sum(axis=1)
total_successes_2a = int(df_2a["aggregated_correct_belief"].sum())
total_trials_2a = len(df_2a) * 12



binom_test_result_2a = binomtest(total_successes_2a, total_trials_2a, 0.5, alternative='greater')
# print(f"Binomial test result for Survey 2a: {binom_test_result_2a}")

# %% ==========================================================================
# ========== Correlating trust with essay confidence usage column ===================================
# =============================================================================
df_1a = data_cleaner(raw_Survey1a, survey1a_col_mapping, survey_number=1, background_first=True)
#print(df_1a)
df_2a = data_cleaner(raw_Survey2a, survey2a_col_mapping, survey_number=2,background_first=False)

def correlate_trust_usage(df, survey_prefix="Sv2a"):
    """
    Correlating the trust in a text and the confidence of the participant in using it in an essay

    STILL WIP WILL EXPLAIN LATER

    Parameters:
      df: DataFrame containing the survey data
      survey_prefix: A string such as "Sv1a", "Sv1b", "Sv2a" or "Sv2b"
      
    Returns:
      STILL WIP WILL fix later
    """
    result = df.copy()
    for i in range(1, 13):
        trustworthy_col = f"{survey_prefix}_T{i}_trustworthy"
        confident_col = f"{survey_prefix}_T{i}_confident"
        if trustworthy_col in result.columns and confident_col in result.columns:
            for idx in result.index:
            # Only process if both columns exist
                if trustworthy_col in result.columns and confident_col in result.columns:
                    trustworthy_int = result.loc[idx, trustworthy_col]
                    confident_int = result.loc[idx, confident_col]
                    participant_id = result.loc[idx, "id"]
                    if trustworthy_int == confident_int:
                        print(f"MATCH {survey_prefix}_T{i}: trust and confidence for {survey_prefix}_T{i} match, trust: {trustworthy_int}, confidence: {confident_int}, participant: {participant_id}")
                    if trustworthy_int > confident_int:
                        print(f"MISMATCH TRUST HIGHER {survey_prefix}_T{i}: trust and confidence for {survey_prefix}_T{i} don't match, trust is higher: {trustworthy_int} than confidence: {confident_int}, participant: {participant_id}")
                    if trustworthy_int < confident_int:
                        print(f"MISMATCH TRUST LOWER {survey_prefix}_T{i}: trust and confidence for {survey_prefix}_T{i} don't match, trust is lower: {trustworthy_int} than confidence: {confident_int}, participant: {participant_id}")
    return result

#correlate_trust_usage(df_1a, "Sv1a")
correlate_trust_usage(df_2a, "Sv2a")
# %%

def process_surveys_to_csv(df_1a, df_2a, df_1b, df_2b, output_filename="trust_metrics_processed.csv"):
    """
    Process survey dataframes directly into a simplified CSV with columns:
    participant_id, text_number, ai_generated, metric, rating
    
    Parameters:
    - df_1a, df_2a, df_1b, df_2b: Processed survey dataframes
    - output_filename: Name of output CSV file
    """
    import pandas as pd
    
    # Initialize an empty list to store all records
    all_records = []
    
    # Process each dataframe
    for df, survey_suffix in [(df_1a, "1a"), (df_2a, "2a"), (df_1b, "1b"), (df_2b, "2b")]:
        # For each text in the survey (1-12)
        for text_num in range(1, 13):
            # Column name for AI generated status
            ai_col = f"Sv{survey_suffix}_T{text_num}_ai_generated"
            
            # Only process if the AI column exists
            if ai_col in df.columns:
                # Get trustworthy ratings
                trustworthy_col = f"Sv{survey_suffix}_T{text_num}_trustworthy"
                if trustworthy_col in df.columns:
                    for idx, row in df.iterrows():
                        participant_id = row["participant_id"]
                        ai_generated = row[ai_col]
                        rating = row.get(trustworthy_col)
                        
                        # Create a text_number in the format "1_1a"
                        text_id = f"{text_num}_{survey_suffix}"
                        
                        # Add record if rating is not NaN
                        if pd.notna(rating):
                            all_records.append({
                                "participant_id": participant_id,
                                "text_number": text_id,
                                "ai_generated": ai_generated,
                                "metric": "trustworthy",
                                "rating": rating
                            })
    
    # Convert to DataFrame and save to CSV
    result_df = pd.DataFrame(all_records)
    print(result_df.head())
    result_df.to_csv(output_filename, index=False)
    print(f"Data saved to {output_filename}")
    return result_df

# Execute the function with your dataframes
processed_df = process_surveys_to_csv(df_1a, df_2a, df_1b, df_2b)
# %%

print("print df_1a",df_1a.head())
print("print df_2a",df_2a.head())
print("print df_1b",df_1b.head())
print("print df_2b",df_2b.head())

# Save the cleaned dataframes to CSV files
# %%
import os
import pandas as pd
from scipy.stats import f


# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)
# Treatmet (C): Treatement Description (0 ST, 1 LT)

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# # Define Functions
# Calculate T Statistic
# $ Add more Stats as needed $


def oneway_ANOVA(y, x):
    list = []
    command = 'oneway '+y+' '+x
    # Run Stata Anova Test
    stata.run(command)

    # Collect results
    SS = round(Scalar.getValue('r(mss)'), 3)
    dfn = Scalar.getValue('r(df_m)')
    MS = SS/dfn
    F = round(Scalar.getValue('r(F)'), 3)
    dfd = Scalar.getValue('r(df_r)')
    p = round(1-f.cdf(F, dfn, dfd), 3)

    if p < 0.05:
        hypo = 'Reject Ho'
    else:
        hypo = 'Fail to reject Ho'

    list.extend((SS, dfn, MS, dfd, F, p, hypo))
    return list


def get_data(data, y, x):
    dtf0 = pd.DataFrame()
    for key in DataFrameDict.keys():
        DataFrameDict[key] = data[data['Subject'] == key]
        stata.pdataframe_to_data(DataFrameDict[key], force=True)
        res = oneway_ANOVA(y, x)
        if res[4] == 8.98846567431158e+307:
            res[4] = 'NaN'
            res[5] = 'NaN'
            res[6] = 'Fail to reject Ho'
        else:
            res[4]
        dt = pd.DataFrame(data=[res])
        dtf0 = dtf0.append(dt, ignore_index=True)

    dtf0.set_index(Subjects, inplace=True)
    dtf0.rename(columns={0: "SS", 1: "dfn", 2: "MS",
                        3: "dfd", 4: "F", 5: "Prob > F",
                        6: "Hypothesis"}, inplace=True)
    return dtf0
# Split


#############################################################################
# # ################ $$$ Monte Carlo $$$ ######################
# Load the Data

dtf = pd.read_csv('40PerSubjectData.csv', header=0, na_filter = True,
                  dtype={'Treatment (D)': int,
                        'Subject': int, 'Year': int}).dropna()


# #  ################ $$ Import Stata  $$ ####################
# Overall
import stata_setup
stata_setup.config('/Applications/Stata', 'be')
from pystata import stata
from sfi import Scalar, Matrix




# # ################ $$ Per Subject Analysis  all blocks $$ ##################
# Create a data frame dictionary to store your data frames

Subjects = dtf.Subject.unique()
DataFrameDict = {elem: pd.DataFrame for elem in Subjects}

# Select data frame to be analyzed

Anova_Belief = get_data(dtf, 'Belief', 'TreatmentC')
Anova_Allocation = get_data(dtf, 'PerAllo', 'TreatmentC')
Anova_Earnings = get_data(dtf, 'EAB', 'TreatmentC')

Anova_Belief
Anova_Allocation
Anova_Earnings

# #  ################ $$ Per Subject Analysis block 0 and 1 $$ ################
blocks = [0, 2]
dtf2 = dtf.loc[dtf['Treatment (C)'].isin(blocks)]

# Select data frame to be analyzed

Anova_Belief2 = get_data(dtf2, 'Belief', 'TreatmentC')
Anova_Allocation2 = get_data(dtf2, 'PerAllo', 'TreatmentC')
Anova_Earnings2 = get_data(dtf2, 'EAB', 'TreatmentC')

Anova_Belief2
Anova_Allocation2
Anova_Earnings2

# #  ################ $$ Test $$ ####################
# stata.pdataframe_to_data(dtf, force=True)
# stata.run('summarize')
# stata.run('oneway Belief TreatmentC, tabulate')
# stata.run('oneway PerAllo TreatmentC, tabulate')
# stata.run('oneway EAB TreatmentC, tabulate')
# stata.run('oneway Belief TreatmentC, bonferroni')
# stata.run('oneway PerAllo TreatmentC, bonferroni')
# stata.run('oneway EAB TreatmentC, bonferroni')

# stata.pdataframe_to_data(dtf[dtf['Subject'] == 41], force=True)
# test = oneway_ANOVA('Belief', 'TreatmentC')
#
# if test[4] == 8.98846567431158e+307:
#     test[4] = 'NaN'
# else:
#     test[4]
#
# print(test)

import os
import pandas as pd
import statistics
import scipy.stats as stat

# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)
path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# # Define Functions
# Calculate Statistics
# $ Add more Stats as needed $


def calc_sum_stats(boot_df):
    sum_stats = boot_df.describe().T[['count', 'mean', 'std', 'min', 'max']]
    sum_stats['variance'] = statistics.variance(boot_df)
    sum_stats['SE'] = stat.sem(boot_df)
    sum_stats['median'] = boot_df.median()
    sum_stats['skew'] = boot_df.skew()
    sum_stats['kurtosis'] = boot_df.kurtosis()
    sum_stats['IQR'] = boot_df.quantile(0.75) - boot_df.quantile(0.25)
    return sum_stats.T


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0)
    st = calc_sum_stats(dtf[col])

    # Get Control and Treatmet Groups
    dtfCG = dtf[dtf[tname] == CG]
    stCG = calc_sum_stats(dtfCG[col])

    dtfTG = dtf[dtf[tname] == TG]
    stTG = calc_sum_stats(dtfTG[col])

    return dtf, dtfCG, dtfTG, st, stCG, stTG


#############################################################################
# # ################ $$$ Exploratory Data Analysis $$$ ######################


#  ########### $$ Objective Return Distributions $$ ################
dfOb = pd.read_csv('ObjDistribution.csv', header=0) # Overall
stOb = calc_sum_stats(dfOb['Objective'])

dfObDC = dfOb[dfOb['Actual Year'] <= 1944]  # During Crash
stObDC = calc_sum_stats(dfObDC['Objective'])

dfObNC = dfOb[dfOb['Actual Year'] >= 1945]  # Post Crash
stObNC = calc_sum_stats(dfObNC['Objective'])


#  ################ $$ All Stats $$ ####################
dtf20, dtf20ST, dtf20LT, st20, st20CG, st20TG = split('20PerSubjectData.csv',
                                            'Belief', 'Treatment (D)', 0, 1)
dtf40, dtf40ST, dtf40LT, st40, st40CG, st40TG = split('40PerSubjectData.csv',
                                         'Belief', 'Treatment (D)', 0, 1)

# 0 is for Short Term 1 Long Term

#  ################ $$ Overall $$ ####################

C0stats = pd.concat([st40, stOb, st20, stObNC], axis=1,
                keys=['Mar40', 'Objective', 'Mar20', 'Objective'])
print(C0stats.round(3).to_latex(index=True))

#  ################ $$ Short vs. Long Term Description $$ ####################

Cstats = pd.concat([st40CG, st40TG, st20CG, st20TG], axis=1,
                keys=['ST Crash', 'LT Crash', 'ST NC', 'LT NC'])
print(Cstats.round(3).to_latex(index=True))

#  ################ $$ During Crash vs. No Crash $$ ####################
dtf40DC = dtf40[dtf40['Year'] <= 20]
st40DC = calc_sum_stats(dtf40DC['Belief'])

C1stats = pd.concat([st40DC, stObDC, st20, stObNC], axis=1,
                keys=['During C', 'ObjectiveDC', 'Marginal20', 'Objective'])
print(C1stats.round(3).to_latex(index=True))

#  ################ $$ Post Crash vs.  No Crash $$ ####################
dtf40PC = dtf40[dtf40['Year'] >= 21]
st40PC = calc_sum_stats(dtf40PC['Belief'])

C2stats = pd.concat([st40PC, st20, stObNC], axis=1,
                keys=['Post C', 'Marginal20', 'Objective'])

print(C2stats.round(3).to_latex(index=True))

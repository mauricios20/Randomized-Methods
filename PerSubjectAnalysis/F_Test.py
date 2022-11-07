import os
import pandas as pd
import scipy
import statistics
from scipy import stats
import numpy as np


# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# # Define Functions
# Calculate T Statistic
# $ Add more Stats as needed $


def f_test(x, y, a, name):
    x = np.array(x)
    y = np.array(y)
    varx = statistics.variance(x)
    vary = statistics.variance(y)
    # calculate F test statistic
    if varx > vary:
        f = varx / vary
        dfn = x.size - 1
        dfd = y.size - 1
        print("Var(x)={} > Var(y)={}, thus x is the nominator".format(
            round(varx, 3), round(vary, 3)))
        print("dfn={}, dfd={}".format(dfn, dfd))
        s2max = varx
        s2min = vary
    else:
        f = vary / varx
        dfn = y.size - 1
        dfd = x.size - 1
        print("Var(x)={} < Var(y)={}, thus y is the nominator".format(
            round(varx, 3), round(vary, 3)))
        print("dfn={}, dfd={}".format(dfn, dfd))
        s2max = vary
        s2min = varx
    b = a / 2
    q = 1 - b
    Fcr = scipy.stats.f.ppf(q, dfn, dfd)  # Critical Value Right Tail
    Fcl = scipy.stats.f.ppf(b, dfn, dfd)  # Left Tail
    p = 1 - scipy.stats.f.cdf(f, dfn, dfd)  # find p-value of F test statistic

    if f > Fcr or f < Fcl:
        print("f {} > Fcr {} or f {} < Fcl {}: Reject Null Hypothesis, Var(x) neq Var(Y)".format(
            round(f, 3), round(Fcr, 3), round(f, 3), round(Fcl, 3)))
        dt = pd.DataFrame(data={'Subject': name, 's2max': round(s2max, 3), 's2min': round(s2min, 3),
                                'dfn': dfn, 'dfd': dfd, 'F': round(f, 3),
                                '$F_{1-a/2}$': round(Fcr, 3), '$F_{a/2}$': round(Fcl, 3),
                                'H_{o}': 'Reject'}, index=[0])
    else:
        print("f {} < Fcr {} or f {} > Fcl {}: Fail to Reject Null Hypothesis, Var(x) = Var(y)".format(
            round(f, 3), round(Fcr, 3), round(f, 3), round(Fcl, 3)))
        dt = pd.DataFrame(data={'Subject': name, 's2max': round(s2max, 3), 's2min': round(s2min, 3),
                                'dfn': dfn, 'dfd': dfd, 'F': round(f, 3),
                                '$F_{1-a/2}$': round(Fcr, 3), '$F_{a/2}$': round(Fcl, 3),
                                'H_{o}': 'Fail to Reject'}, index=[0])
    return dt

# Split


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0,
                      dtype={'Treatment (D)': int, 'Subject': int, 'Year': int})
    # st = calc_sum_stats(dtf[col])

    # Get Control and Treatmet Groups
    dtfCG = dtf[dtf[tname] == CG]

    dtfTG = dtf[dtf[tname] == TG]

    return dtf, dtfCG, dtfTG,

# Calculate n, k, p and Hypothesis

#############################################################################
# # ################ $$$ Monte Carlo $$$ ######################
# Load the Data


dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)


# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Overall
dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
Subjects = dtf40.Subject.unique()
Years = dtf40.Year.unique()

# Total number of observations only for demostration
# print(Ylen)
# print(DC)
# print(PC)

# Create a data frame dictionary to store your data frames

DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
# print(len(DataFrameDict))  # Make sure it equals the same number of subjects
# print(DataFrameDict.keys())  # Look at the keys, Keys = Subject ID

Tobs = pd.DataFrame()
for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf40[dtf40['Subject'] == key]
    dtfDC = DataFrameDict[key][DataFrameDict[key].Year <= 20]
    dtfPC = DataFrameDict[key][DataFrameDict[key].Year >= 21]
    res = f_test(dtfPC['Belief'], dtfDC['Belief'], 0.05, key)
    Tobs = Tobs.append(res, ignore_index=True)


print(Tobs.to_latex(index=False))


failsubjects = Tobs[Tobs['H_{o}'] == 'Reject']
failsubjects.Subject.unique().tolist()

exclude = [41, 104, 42, 43, 45, 47, 55, 59, 106, 108, 110, 114, 118, 119]
dtf = Tobs.loc[~Tobs.Subject.isin(exclude)]
Subjects2 = dtf.Subject.unique()
print(dtf.to_latex(index=False))
len(exclude)
len(dtf.Subject.unique())
# #### F-Test ########

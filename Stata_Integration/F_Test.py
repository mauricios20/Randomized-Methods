import os
import pandas as pd
import numpy as np
import scipy
import statistics
from scipy import stats


path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0,
                      dtype={'Treatment (D)': int, 'Subject': int, 'Year': int})
    # st = calc_sum_stats(dtf[col])

    # Get Control and Treatmet Groups
    dtfCG = dtf[dtf[tname] == CG]

    dtfTG = dtf[dtf[tname] == TG]

    return dtf, dtfCG, dtfTG,


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
        dt = pd.DataFrame(data={'Name': name, 's2max': round(s2max, 3), 's2min': round(s2min, 3),
                                'dfn': dfn, 'dfd': dfd, 'F': round(f, 3),
                                '$F_{1-a/2}$': round(Fcr, 3), '$F_{a/2}$': round(Fcl, 3),
                                'H_{o}': 'Reject'}, index=[0])
    else:
        print("f {} < Fcr {} or f {} > Fcl {}: Fail to Reject Null Hypothesis, Var(x) = Var(y)".format(
            round(f, 3), round(Fcr, 3), round(f, 3), round(Fcl, 3)))
        dt = pd.DataFrame(data={'Name': name, 's2max': round(s2max, 3), 's2min': round(s2min, 3),
                                'dfn': dfn, 'dfd': dfd, 'F': round(f, 3),
                                '$F_{1-a/2}$': round(Fcr, 3), '$F_{a/2}$': round(Fcl, 3),
                                'H_{o}': 'Fail to Reject'}, index=[0])
    return dt


# #  ################ $$ During Crash / Post Crash/ No Crash $$ ###############
# Extract Data
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

frames = [dtf40DC, dtf40PC, dtf20]

# ~~~~~~~~~~~~ Homogeneity of Variance ~~~~~~~~~~~~

dtPC_NC = f_test(dtf20['Belief'], dtf40PC['Belief'], 0.05, 'PCvsNC')

dtDC_PC = f_test(dtf40DC['Belief'], dtf40PC['Belief'], 0.05, 'DCvsPC')

dtDC_NC = f_test(dtf40DC['Belief'], dtf20['Belief'], 0.05, 'DCvsNC')

final_dtf = pd.concat([dtDC_NC, dtDC_PC, dtPC_NC])
print(final_dtf.to_latex(index=False))

# ~~~~~~~~~~~~ Homogeneity of Variance Description ~~~~~~~~~~~~
dtfLT_ST_C = f_test(dtf40ST['Belief'], dtf40LT['Belief'], 0.05, 'STvsLT Crash')

dtfLT_ST_NC = f_test(dtf20ST['Belief'], dtf20LT['Belief'], 0.05, 'STvsLT NC')

final_dtf_Description = pd.concat([dtfLT_ST_C, dtfLT_ST_NC])
print(final_dtf_Description.to_latex(index=False))

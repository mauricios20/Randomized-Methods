import os
import pandas as pd
import numpy as np
import scipy
import statistics


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


def f_test(x, y, a):
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
    else:
        f = vary / varx
        dfn = y.size - 1
        dfd = x.size - 1
        print("Var(x)={} < Var(y)={}, thus y is the nominator".format(
            round(varx, 3), round(vary, 3)))
        print("dfn={}, dfd={}".format(dfn, dfd))

    q = 1 - (a / 2)
    Fc = scipy.stats.f.ppf(q, dfn, dfd)  # Critical Value
    p = 1 - scipy.stats.f.cdf(f, dfn, dfd)  # find p-value of F test statistic

    if f < Fc:
        print("f {} < Fc {}: Reject Null Hypothesis, Var(x) neq Var(Y)".format(
            round(f, 3), round(Fc, 3)))
    else:
        print("f {} > Fc {}: Fail to Reject Null Hypothesis, Var(x) = Var(y)".format(
            round(f, 3), round(Fc, 3)))
    return f, Fc, p


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

f, Fc, p = f_test(dtf20['Belief'], dtf40PC['Belief'], 0.05)

f, Fc, p = f_test(dtf40DC['Belief'], dtf40PC['Belief'], 0.05)

f, Fc, p = f_test(dtf40DC['Belief'], dtf20['Belief'], 0.05)

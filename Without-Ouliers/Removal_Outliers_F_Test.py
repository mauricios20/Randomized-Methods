import os
import pandas as pd
import statistics
import scipy.stats as stat
import numpy as np
import scipy

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


def calc_sum_stats(boot_df):
    sum_stats = boot_df.describe().T[['count', 'mean', 'std', 'min', 'max']]
    sum_stats['variance'] = statistics.variance(boot_df)
    sum_stats['SE'] = stat.sem(boot_df)
    sum_stats['median'] = boot_df.median()
    sum_stats['skew'] = boot_df.skew()
    sum_stats['kurtosis'] = boot_df.kurtosis()
    sum_stats['IQR'] = boot_df.quantile(0.75) - boot_df.quantile(0.25)
    return sum_stats.T


def remove_outliers(data, x):
    # Define Quartiles
    Q1 = data[x].quantile(0.25)
    Q3 = data[x].quantile(0.75)
    IQR = Q3 - Q1

    # Old Shape
    print("Old Shape", data.shape)
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    print("Upper Bound:", upper)
    OutlierUp = data.index[data[x] >= upper].tolist()
    print(OutlierUp)

    print("Lower Bound:", lower)
    OutlierLow = data.index[data[x] <= lower].tolist()
    print(OutlierLow)

    # Removing Outliers
    dtf = data.drop(OutlierUp, axis=0)
    dtfNO = dtf.drop(OutlierLow, axis=0)
    print("New Shape", dtfNO.shape)
    return dtfNO


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

# ~~~~~~~~~~~~~ Remove Outliers ~~~~~~~~~~~~~~~~~~~
dtf_DC = remove_outliers(dtf40DC, 'Belief')
dtf_PC = remove_outliers(dtf40PC, 'Belief')
dtf_NC = remove_outliers(dtf20, 'Belief')

# ~~~~~~~~~~~~~ Recalculate Stats ~~~~~~~~~~~~~~~~~~~
statsDC = calc_sum_stats(dtf_DC['Belief'])
statsPC = calc_sum_stats(dtf_PC['Belief'])
statsNC = calc_sum_stats(dtf_NC['Belief'])


#  $$ Objective Return Distributions $$
dfOb = pd.read_csv('ObjDistribution.csv', header=0)  # Overall
stOb = calc_sum_stats(dfOb['Objective'])

dfObDC = dfOb[dfOb['Actual Year'] <= 1944]  # During Crash
stObDC = calc_sum_stats(dfObDC['Objective'])

dfObNC = dfOb[dfOb['Actual Year'] >= 1945]  # Post Crash
stObNC = calc_sum_stats(dfObNC['Objective'])

# ## Combine All Stats
C1stats = pd.concat([statsDC, stObDC, statsNC, stObNC, statsPC, stObNC], axis=1,
                    keys=['DC', 'ObDC', 'NC', 'dfObNC', 'PC', 'dfObNC'])
print(C1stats.round(3).to_latex(index=True))

# ~~~~~~~~~~~~ Homogeneity of Variance ~~~~~~~~~~~~
f, Fc, p = f_test(dtf_DC['Belief'], dtf_NC['Belief'], 0.05)

f, Fc, p = f_test(dtf_DC['Belief'], dtf_PC['Belief'], 0.05)

f, Fc, p = f_test(dtf_PC['Belief'], dtf_NC['Belief'], 0.05)

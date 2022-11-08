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


def remove_outliers(data, x, name):
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
    obsup = len(OutlierUp)

    print("Lower Bound:", lower)
    OutlierLow = data.index[data[x] <= lower].tolist()
    obslow = len(OutlierLow)

    totalout = obsup + obslow
    # Removing Outliers
    dtf = data.drop(OutlierUp, axis=0)
    dtfNO = dtf.drop(OutlierLow, axis=0)
    print("New Shape", dtfNO.shape)

    dt = pd.DataFrame(data={'Name': name, 'Q1': round(Q1, 2), 'Q3': round(Q3, 3),
                            'IQR': IQR, 'Upper Bound': round(upper, 3),
                            'Lower Bound': round(lower, 3),
                            'obs>Upper': obsup, 'obs<Lower': obslow,
                            'Total Outliers': totalout}, index=[0])
    return dtfNO, dt


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
    Fcl = scipy.stats.f.ppf(b, dfn, dfd)  # Critical Value Left Tail
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

# ~~~~~~~~~~~~~ Remove Outliers ~~~~~~~~~~~~~~~~~~~
# Overall
dtf_DC, dtnumDC = remove_outliers(dtf40DC, 'Belief', 'During Crash')
dtf_PC, dtnumPC = remove_outliers(dtf40PC, 'Belief', 'Post Crash')
dtf_NC, dtnumNC = remove_outliers(dtf20, 'Belief', 'No Crash')

Outliers_dtf = pd.concat([dtnumDC, dtnumPC, dtnumNC])
print(Outliers_dtf.to_latex(index=False))

# Description
dtf_DC_ST, dtnumDC_ST = remove_outliers(dtf40ST, 'Belief', 'DC_ST')
dtf_DC_LT, dtnumDC_LT = remove_outliers(dtf40LT, 'Belief', 'DC_LT')
dtf_NC_ST, dtnumNC_ST = remove_outliers(dtf20ST, 'Belief', 'NC_ST')
dtf_NC_LT, dtnumNC_LT = remove_outliers(dtf20LT, 'Belief', 'NC_LT')

Outliers_dtf_D = pd.concat([dtnumDC_ST, dtnumDC_LT, dtnumNC_ST, dtnumNC_LT])
print(Outliers_dtf_D.to_latex(index=False))

# ~~~~~~~~~~~~~ Recalculate Stats ~~~~~~~~~~~~~~~~~~~
# Overall
statsDC = calc_sum_stats(dtf_DC['Belief'])
statsPC = calc_sum_stats(dtf_PC['Belief'])
statsNC = calc_sum_stats(dtf_NC['Belief'])

# Description
statsDC_ST = calc_sum_stats(dtf_DC_ST['Belief'])
statsDC_LT = calc_sum_stats(dtf_DC_LT['Belief'])
statsNC_ST = calc_sum_stats(dtf_NC_ST['Belief'])
statsNC_LT = calc_sum_stats(dtf_NC_LT['Belief'])

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

C2stats = pd.concat([statsDC_LT, statsDC_ST, statsNC_LT, statsNC_ST], axis=1,
                    keys=['LT_DC', 'ST_DC', 'LT_NC', 'ST_NC'])
print(C2stats.round(3).to_latex(index=True))

# ~~~~~~~~~~~~ Homogeneity of Variance ~~~~~~~~~~~~
dtDC_NC = f_test(dtf_DC['Belief'], dtf_NC['Belief'], 0.05, 'DCvsNC')

dtDC_PC = f_test(dtf_DC['Belief'], dtf_PC['Belief'], 0.05, 'DCvsPC')

dtPC_NC = f_test(dtf_PC['Belief'], dtf_NC['Belief'], 0.05, 'PCvsNC')

final_dtf = pd.concat([dtDC_NC, dtDC_PC, dtPC_NC])
print(final_dtf.to_latex(index=False))

# ~~~~~~~~~~~~ Homogeneity of Variance Description ~~~~~~~~~~~~
dtfLTvsST_C = f_test(dtf_DC_ST['Belief'], dtf_DC_LT['Belief'], 0.05, 'STvsLT Crash')

dtfLTvsST_NC = f_test(dtf_NC_ST['Belief'], dtf_NC_LT['Belief'], 0.05, 'STvsLT NC')

final_dtf_Description = pd.concat([dtfLTvsST_C, dtfLTvsST_NC])
print(final_dtf_Description.to_latex(index=False))

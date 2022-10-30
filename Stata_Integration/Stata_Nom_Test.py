import os
import pandas as pd
import stata_setup
stata_setup.config('/Applications/Stata', 'be')
from sfi import Scalar, Matrix
from pystata import stata


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


def collectWilk_results(vname):

    # Collect results
    N = round(Scalar.getValue('r(N)'), 0)
    W = round(Scalar.getValue('r(W)'), 3)
    V = round(Scalar.getValue('r(V)'), 3)
    z = round(Scalar.getValue('r(z)'), 3)
    p = round(Scalar.getValue('r(p)'), 3)

    d = {'Variable': vname, 'Obs': N, 'W': W, 'V': V, 'z': z, 'Prob>z': p}
    dtf = pd.DataFrame(data=d, index=[0])
    return dtf


def collectSkeKu_results(vname):

    # Collect results
    N = round(Scalar.getValue('r(N)'), 0)
    S = round(Scalar.getValue('r(p_skew)'), 3)
    K = round(Scalar.getValue('r(p_kurt)'), 3)
    x2 = round(Scalar.getValue('r(chi2)'), 3)
    px2 = round(Scalar.getValue('r(p_chi2)'), 3)

    d = {'Variable': vname, 'Obs': N,
         'Pr(skewness)': S, 'Pr(kurtosis)': K, 'Adj chi2(2)': x2, 'Prob>chi2': px2}
    dtf = pd.DataFrame(data=d, index=[0])
    return dtf

# #  ################ $$ During Crash / Post Crash/ No Crash $$ ###############
# Extract Data
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

frames = [dtf40DC, dtf40PC, dtf20]
# ~~~~~~~~~~~~ Test for normality ~~~~~~~~~~~~
# Durin Crash (DC)
stata.pdataframe_to_data(dtf40DC, force=True)

# #### Visual Representation of normality
stata.run('hist Belief, normal')
stata.run('pnorm Belief')
stata.run('qnorm Belief')

# #### Shapiro–Wilk Test for normality
stata.run('swilk Belief')
# Collect results
dtfSwilkDC = collectWilk_results('DC Belief')
# dtfSwilkDC

# #### Skewness and kurtosis tests for normality
stata.run('sktest Belief')
dtfSkeKuDC = collectSkeKu_results('DC Belief')
# dtfSkeKuDC

# $$$$$$$ Post Crash (PC) $$$$$$$
stata.pdataframe_to_data(dtf40PC, force=True)

# #### Visual Representation of normality
stata.run('hist Belief, normal')
stata.run('pnorm Belief')
stata.run('qnorm Belief')

# #### Shapiro–Wilk Test for normality
stata.run('swilk Belief')
# Collect results
dtfSwilkPC = collectWilk_results('PC Belief')
# dtfSwilkPC

# #### Skewness and kurtosis tests for normality
stata.run('sktest Belief')
dtfSkeKuPC = collectSkeKu_results('PC Belief')
# dtfSkeKuPC


# $$$$$$$ Non Crash $$$$$$$
stata.pdataframe_to_data(dtf20, force=True)

# #### Visual Representation of normality
stata.run('hist Belief, normal')
stata.run('pnorm Belief')
stata.run('qnorm Belief')

# #### Shapiro–Wilk Test for normality
stata.run('swilk Belief')
# Collect results
dtfSwilkNC = collectWilk_results('NC Belief')
# dtfSwilkNC

# #### Skewness and kurtosis tests for normality
stata.run('sktest Belief')
dtfSkeKuNC = collectSkeKu_results('NC Belief')
# dtfSkeKuNC

final_dtfShapiro = pd.concat([dtfSwilkDC, dtfSwilkPC, dtfSwilkNC])
print(final_dtfShapiro.to_latex(index=False))

final_dtfSkeKu = pd.concat([dtfSkeKuDC, dtfSkeKuPC, dtfSkeKuNC])
print(final_dtfSkeKu.to_latex(index=False))

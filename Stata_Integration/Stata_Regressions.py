
from sfi import Scalar, Matrix
from pystata import stata
import os
import pandas as pd
import stata_setup
stata_setup.config('/Applications/Stata', 'be')


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


# def collectSkeKu_results(vname):
#
#     # Collect results
#     N = round(Scalar.getValue('r(N)'), 0)
#     S = round(Scalar.getValue('r(p_skew)'), 3)
#     K = round(Scalar.getValue('r(p_kurt)'), 3)
#     x2 = round(Scalar.getValue('r(chi2)'), 3)
#     px2 = round(Scalar.getValue('r(p_chi2)'), 3)
#
#     d = {'Variable': vname, 'Obs': N, 'Pr(skewness)': S, 'Pr(kurtosis)': K, 'Adj chi2(2)': x2, 'Prob>chi2': px2}
#     dtf = pd.DataFrame(data=d, index=[0])
#     return dtf


# #  ################ $$ During Crash / Post Crash/ No Crash $$ ###############
# Extract Data
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

# ~~~~~~~~~~~~ Lag Regression ~~~~~~~~~~~~
# Durin Crash (DC)
Group40DC = dtf40DC.groupby('Year').mean().reset_index()
Group40DC.to_stata('group40DC.dta')

stata.pdataframe_to_data(Group40DC, force=True)

# #### Lag Regression
stata.run('tsset Year')
stata.run('reg D.Belief L(0/1).D.Objective')
stata.run('lincom D.Objective+L.D.Objective')
stata.run('estat ic')


# $$$$$$$ Post Crash (PC) $$$$$$$
Group40PC = dtf40PC.groupby('Year').mean().reset_index()
Group40PC.to_stata('group40PC.dta')

stata.pdataframe_to_data(Group40PC, force=True)

# #### Lag Regression
stata.run('tsset Year')
stata.run('reg D.Belief L(0/3).D.Objective')
stata.run('lincom D.Objective+L.D.Objective+L2.D.Objective+L3.D.Objective')
stata.run('lincom D.Objective+L.D.Objective+L2.D.Objective')
stata.run('lincom D.Objective+L.D.Objective')
stata.run('estat ic')

# $$$$$$$ Non Crash $$$$$$$
Group20 = dtf20.groupby('Year').mean().reset_index()
Group20.to_stata('group20NC.dta')
stata.pdataframe_to_data(Group20, force=True)

# #### Visual Representation of normality
stata.run('tsset Year')
stata.run('reg D.Belief L(0/1).D.Objective')
stata.run('predict r, resid')
stata.run('kdensity r, normal')
stata.run('pnorm r')
stata.run('qnorm r')
stata.run('swilk r')
stata.run('lincom D.Objective+L.D.Objective')
stata.run('estat ic')


# ~~~~~~~~~~~~ Correlation Matrix ~~~~~~~~~~~~
Group20.to_stata('group20NC.dta')
stata.pdataframe_to_data(Group20, force=True)
stata.run('tsset Year')
stata.run('corrgram Belief')
stata.run('spearman Belief Objective')
stata.run('pwcorr Belief Objective, sig star(.05) obs')
stata.run('scatter Belief Objective')
# stata.run("regress PerAllo Belief")
# stata.run("graph twoway (scatter PerAllo Belief) (lfit PerAllo Belief) , ytitle (% Allocation)")
# stata.run("predict res, residuals")
# stata.run("predict fitted, xb")
# stata.run("rvfplot, addplot(lfit res fitted)")

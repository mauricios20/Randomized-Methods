
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


# Calculate n, k, p and Hypothesis
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)


# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Overall

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

print(dtf40DC)
stata.pdataframe_to_data(dtf40, force=True)
stata.run('summarize')

stata.run("regress PerAllo Belief")
stata.run("graph twoway (scatter PerAllo Belief) (lfit PerAllo Belief) , ytitle (% Allocation)")
stata.run("predict res, residuals")
stata.run("predict fitted, xb")
stata.run("rvfplot, addplot(lfit res fitted)")

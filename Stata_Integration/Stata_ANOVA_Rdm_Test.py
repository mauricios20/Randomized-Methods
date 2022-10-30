import os
import pandas as pd
import random
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


def MC(Subjects, GlenC, nper, dtf):
    F_values = []
    for __ in range(nper):
        # Groups and positions will be assigned in order, so shuffle beforehand.
        # Ignore Setting Copy message
        random.shuffle(Subjects)
        control = Subjects[:GlenC]
        Treatment = Subjects[GlenC:]
        dtfCG = dtf.loc[dtf['Subject'].isin(control)].copy(deep=True)
        dtfCG['Condition'] = 'Control'
        dtfTG = dtf.loc[dtf['Subject'].isin(Treatment)].copy(deep=True)
        dtfTG['Condition'] = 'Treatment'
        newframe = [dtfCG, dtfTG]
        dtfMC = pd.concat(newframe)
        # F-Statistic
        stata.pdataframe_to_data(dtfMC, force=True)
        stata.run('oneway Belief Condition, tabulate')
        FMC = round(Scalar.getValue('r(F)'), 2)
        F_values.append(FMC)

    F_values
    dtFv = pd.DataFrame(F_values, columns=['F_values'])

    obs = abs(FO)  # Observed result of experiment difference kurtosis
    # to get numbers > k
    count = sum(i >= obs for i in abs(dtFv['F_values']))
    count
    # printing the intersection
    print('Number of observations that are >= than the observed F of ' + str(FO) + ' in ' +
          str(nper) + ' permutations is: ' + str(count))
    p_value = count / nper
    corrected = (count + 1) / (nper + 1)
    print('P(|Observed Diff|>={0:}) = {1:.2f}'.format(obs, p_value))

    a = 0.05
    if p_value < a:
        dt = pd.DataFrame(data={'k': nper, 'r': count, 'p_values': round(p_value, 3), 'Correction': round(
            corrected, 3), 'Hypothesis': 'Reject Ho'}, index=[0])
    else:
        dt = pd.DataFrame(data={'k': nper, 'r': count, 'p_values': round(p_value, 3), 'Correction': round(
            corrected, 3), 'Hypothesis': 'Fail to eject Ho'}, index=[0])

    return dtFv, dt


# #  ################ $$ During Crash / Post Crash/ No Crash $$ ###############
# Extract Data
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

frames = [dtf40DC, dtf40PC, dtf20]

# ~~~~~~~~~~~~ ONE WAY ANOVA TEST ~~~~~~~~~~~~
final_dtf = pd.concat(frames)
stata.pdataframe_to_data(final_dtf, force=True)

stata.run('oneway Belief Condition, tabulate')
# F = round(Scalar.getValue('r(F)'), 3)
stata.run('encode Condition, gen(treatment)')
stata.run('pwmean Belief, over(treatment) mcompare(tukey) effects')

# $$$$$$$$$$$ During Crash vs No Crash Anova Monte Carlo
frame = [dtf40DC, dtf20]
dtfDcNc = pd.concat(frame)
# $ F-STATISTC Original
stata.pdataframe_to_data(dtfDcNc, force=True)
stata.run('oneway Belief Condition, tabulate')
FO = round(Scalar.getValue('r(F)'), 2)
Subjects = dtfDcNc.Subject.unique()
GlenC = len(dtf20.Subject.unique())

MC1, dt1 = MC(Subjects, GlenC, 10000, dtfDcNc)
MC1
stata.pdataframe_to_data(MC1, force=True)
stata.run('hist F_values, plot(scatteri 0 2.13 0.4 2.13, recast(line) lpattern(dash)) legend(off)')

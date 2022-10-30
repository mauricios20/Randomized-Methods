import os
import pandas as pd
import random


# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# # Define Functions
# Calculate T Statistic
# $ Add more Stats as needed $


def calc_diff(dtfCG, dtfTG, x, n):
    list = []
    meanT = round(dtfTG[x].mean(), n)
    meanC = round(dtfCG[x].mean(), n)
    Tx = round((meanT - meanC), n)

    stdT = round(dtfTG[x].std(), n)
    stdC = round(dtfCG[x].std(), n)
    Ty = round((stdT - stdC), n)

    skewT = round(dtfTG[x].skew(), n)
    skewC = round(dtfCG[x].skew(), n)
    Tz = round((abs(skewT) - abs(skewC)), n)

    kurtT = round(dtfTG[x].kurtosis(), n)
    kurtC = round(dtfCG[x].kurtosis(), n)
    Tk = round((abs(kurtT) - abs(kurtC)), n)
    list.extend((meanC, meanT, Tx, stdC, stdT, Ty,
                skewC, skewT, abs(Tz), kurtC, kurtT, abs(Tk)))
    return list

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


def result(x, a):

    final_results = pd.DataFrame()
    for i in Subjects:
        # Observed result of experiment difference kurtosis
        obs = abs(Tobs.loc[i, [x]])
        # to get numbers > k
        count = sum(t >= obs for t in abs(PermuFrameDict[i][x]))

        p_value = count / len(PermuFrameDict[i])
        corrected = (count + 1) / (len(PermuFrameDict[i]) + 1)

        dt = pd.DataFrame(data={'Subject': i, 'n': len(
            PermuFrameDict[i]), 'r': count, 'p_values': p_value, 'Correction': round(corrected, 2)})
        final_results = final_results.append(dt, ignore_index=True)

    hypo = []
    for p in final_results['p_values']:
        if p < a:
            hypo.append('Reject')
        else:
            hypo.append('Fail to Reject')

    final_results['Hypothesis'] = hypo
    return final_results
#############################################################################
# # ################ $$$ Monte Carlo $$$ ######################
# Load the Data


dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)


# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Overall

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

res = calc_diff(dtf40PC, dtf40DC, 'Belief', 3)
res

# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
Subjects = dtf40.Subject.unique()
Years = dtf40.Year.unique()
Ylen = int(len(Years) / 2)
DC = Years[:Ylen]
PC = Years[Ylen:]

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
    res = calc_diff(dtfPC, dtfDC, 'Belief', 3)
    dt = pd.DataFrame(data=[res])
    Tobs = Tobs.append(dt, ignore_index=True)

Tobs.set_index(Subjects, inplace=True)

print(Tobs.to_latex(index=True))

# #### Monte Carlo ########

random.seed(180)
PermuFrameDict = {elem: pd.DataFrame for elem in Subjects}

for key in PermuFrameDict.keys():
    PermuFrameDict[key] = pd.DataFrame()
    for __ in range(5000):  # Doing 2 iterations.
        # Groups and positions will be assigned in order, so shuffle beforehand.
        random.shuffle(Years)
        DC = Years[:Ylen]
        PC = Years[Ylen:]
        dtfCG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(PC)]
        dtfTG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(DC)]
        resMC = calc_diff(dtfCG, dtfTG, 'Belief', 3)
        dtMC = pd.DataFrame(data=[resMC])
        PermuFrameDict[key] = PermuFrameDict[key].append(
            dtMC, ignore_index=True)

# Change Subject ID to see other results

# Belief is 2, PA is 5, and EA is 8

dt_mean = result(2, 0.05)
dt_mean
# print(dt_mean.to_latex(index=False))
dt_std = result(5, 0.05)
dt_std
# print(dt_std.to_latex(index=False))
dt_skew = result(8, 0.05)
dt_skew
# print(dt_skew.to_latex(index=False))
dt_kurt = result(11, 0.05)
dt_kurt
# print(dt_kurt.to_latex(index=False))

import os
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# # Define Functions
# Calculate T Statistic
# $ Add more Stats as needed $


def calc_diff_kurt(dtfCG, dtfTG, x, n):
    list = []
    kurtT = round(dtfTG[x].kurtosis(), n)
    kurtC = round(dtfCG[x].kurtosis(), n)
    T = round((kurtT-kurtC), n)
    list.extend((kurtC, kurtT, T))
    return list


# Split Data Frame


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0,
                      dtype={'Treatment (D)': int, 'Subject': int, 'Year': int})
    # st = calc_sum_stats(dtf[col])

    # Get Control and Treatmet Groups
    dtfCG = dtf[dtf[tname] == CG]

    dtfTG = dtf[dtf[tname] == TG]

    return dtf, dtfCG, dtfTG,

#############################################################################
# # ################ $$$ Monte Carlo $$$ ######################
# Load the Data


dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)


# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Overall

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

res = calc_diff_kurt(dtf40PC, dtf40DC, 'Belief', 2)
print(res)

# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
Subjects = dtf40.Subject.unique()
Years = dtf40.Year.unique()
Ylen = int(len(Years)/2)
DC = Years[:Ylen]
PC = Years[Ylen:]

# Create a data frame dictionary to store your data frames

DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
print(len(DataFrameDict))  # Make sure it equals the same number of subjects
print(DataFrameDict.keys()) # Look at the keys, Keys = Subject ID

Tobs = pd.DataFrame()
for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf40[dtf40['Subject'] == key]
    dtfDC = DataFrameDict[key][DataFrameDict[key].Year <= 20]
    dtfPC = DataFrameDict[key][DataFrameDict[key].Year >= 21]
    res = calc_diff_kurt(dtfPC, dtfDC, 'Belief', 2)
    dt = pd.DataFrame(data=[res])
    Tobs = Tobs.append(dt, ignore_index=True)

Tobs.set_index(Subjects, inplace=True)
print(Tobs)

##### Monte Carlo ########

random.seed(180)
PermuFrameDict = {elem: pd.DataFrame for elem in Subjects}

for key in PermuFrameDict.keys():
    PermuFrameDict[key] = pd.DataFrame()
    for __ in range(10000):  # Doing 2 iterations.
        # Groups and positions will be assigned in order, so shuffle beforehand.
        random.shuffle(Years)
        DC = Years[:Ylen]
        PC = Years[Ylen:]
        dtfCG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(PC)]
        dtfTG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(DC)]
        resMC = calc_diff_kurt(dtfCG, dtfTG, 'Belief', 2)
        dtMC = pd.DataFrame(data=[resMC])
        PermuFrameDict[key] = PermuFrameDict[key].append(dtMC, ignore_index=True)

final_results = pd.DataFrame()
for i in Subjects:
    obs = abs(Tobs.loc[i, [2]])  # Observed result of experiment difference kurtosis
    # to get numbers > k
    count = sum(t >= obs for t in abs(PermuFrameDict[i][2]))

    p_value = count/len(PermuFrameDict[i])
    corrected = (count+1)/(len(PermuFrameDict[i])+1)

    dt = pd.DataFrame(data={'Subject': i, 'n': len(PermuFrameDict[i]), 'k': count, 'p_values': p_value, 'Correction': round(corrected, 2)})
    final_results = final_results.append(dt, ignore_index=True)

hypo = []
for p in final_results['p_values']:
    if p < 0.05:
        hypo.append('Reject Ho')
    else:
        hypo.append('Fail to reject Ho')


final_results['Hypothesis'] = hypo
print(final_results)
# print(Tobs.loc[44, [2]])
# print(PermuFrameDict[41])
    # print(PC)
    # print(dtfCG[['Year', 'Belief']])
    # print(DC)
    # print(dtfTG[['Year', 'Belief']])


#
# print(len(permu[2]))
# obs = abs(res0[2])  # Observed result of experiment difference kurtosis
# # to get numbers > k
# count = sum(i >= obs for i in abs(permu[2]))
#
# # printing the intersection
# print('Number of observations that are >= than the observed kurtosis in ' +
#       str(nper) + ' permutations is:' + str(count))
# p_value = count/len(permu[2])
# corrected = (count+1)/(len(permu[2])+1)
# print(round(p_value, 3))
# print(round(corrected, 3))
# print('P(|Observed Diff|>={0:}) = {1:.2f}'.format(obs, p_value))
# for i in Subjects:
#     DataFrameDict[i]


# TO see what the loop is doing
# dtfDC = DataFrameDict[41][DataFrameDict[41].Year <= 20]
# dtfPC = DataFrameDict[41][DataFrameDict[41].Year >= 21]
# res = calc_diff_kurt(dtfPC, dtfDC, 'Belief', 2)
# dt = pd.DataFrame(data=[res])
# Tobs = Tobs.append(dt)
# Tobs.set_index(Subjects)

# dt = pd.DataFrame(data=[res])

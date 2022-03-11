
import os
import pandas as pd

import stata_setup
stata_setup.config('/Applications/Stata', 'be')
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

stata.run('''
regress PerAllo Belief i.Gender i.TreatmentD
ereturn list
''')


# res = calc_diff_mean(dtf40PC, dtf40DC, 'Belief', 'PerAllo', 'EAB', 2)
# print(res)


# # #  ################ $$ During Crash vs. Post Crash $$ ####################
# # Per Subject
# Subjects = dtf40.Subject.unique()
# Years = dtf40.Year.unique()
# Ylen = int(len(Years)/2)
# DC = Years[:Ylen]
# PC = Years[Ylen:]
#
# # Create a data frame dictionary to store your data frames
#
# DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
# print(len(DataFrameDict))  # Make sure it equals the same number of subjects
# print(DataFrameDict.keys()) # Look at the keys, Keys = Subject ID
#
# Tobs = pd.DataFrame()
# for key in DataFrameDict.keys():
#     DataFrameDict[key] = dtf40[dtf40['Subject'] == key]
#     dtfDC = DataFrameDict[key][DataFrameDict[key].Year <= 20]
#     dtfPC = DataFrameDict[key][DataFrameDict[key].Year >= 21]
#     res = calc_diff_mean(dtfPC, dtfDC, 'Belief', 'PerAllo', 'EAB', 2)
#     dt = pd.DataFrame(data=[res])
#     Tobs = Tobs.append(dt, ignore_index=True)
#
# Tobs.set_index(Subjects, inplace=True)
# print(Tobs)
#
# # #### Monte Carlo ########
#
# random.seed(180)
# PermuFrameDict = {elem: pd.DataFrame for elem in Subjects}
#
# for key in PermuFrameDict.keys():
#     PermuFrameDict[key] = pd.DataFrame()
#     for __ in range(5000):  # Doing 2 iterations.
#         # Groups and positions will be assigned in order, so shuffle beforehand.
#         random.shuffle(Years)
#         DC = Years[:Ylen]
#         PC = Years[Ylen:]
#         dtfCG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(PC)]
#         dtfTG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(DC)]
#         resMC = calc_diff_mean(dtfCG, dtfTG, 'Belief', 'PerAllo', 'EAB', 2)
#         dtMC = pd.DataFrame(data=[resMC])
#         PermuFrameDict[key] = PermuFrameDict[key].append(dtMC, ignore_index=True)
#
# # Belief is 2, PA is 5, and EA is 8
# dt_Beliefs = result(2, 0.05)
# dt_PerAllo = result(5, 0.05)
# dt_EA = result(8, 0.05)
#
# print(dt_Beliefs)
# print(dt_PerAllo)
# print(dt_EA)
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




# Run Multiple Permutations
# random.seed(180)
# obs = abs(res0[2])
# permu1 = MC(Subjects, GlenC, 1000, dtfall)
# permu2 = MC(Subjects, GlenC, 2500, dtfall)
# permu3 = MC(Subjects, GlenC, 5000, dtfall)
# permu4 = MC(Subjects, GlenC, 7500, dtfall)
# permu5 = MC(Subjects, GlenC, 10000, dtfall)
#
# print(permu1.head(3).to_latex(index=True))
# print(permu3.head(3).to_latex(index=True))
# print(permu5.head(3).to_latex(index=True))
# # Plot kernel densities of each permuatation
# fig, axes = plt.subplots()
# MCfig(fig, permu1, permu2, permu3, permu4, permu5, 2, 0.5)
# fig.axes[0].set_xlabel('Kurtosis Difference')
# fig.axes[0].axvline(x=obs, color='black', linestyle="--", linewidth=1)
# fig.axes[0].axvline(x=-obs, color='black', linestyle="--", linewidth=1)
# fig.axes[0].text(5, 0.120, str(obs), rotation=90, verticalalignment='center')
# fig.axes[0].text(-5.1, 0.120, str(-obs), rotation=90, verticalalignment='center')
#
# # #  ################ $$ Post Crash vs. No Crash $$ ####################
# plt.show()

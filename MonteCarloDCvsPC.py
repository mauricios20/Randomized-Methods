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

# Permutations


def MC(Subjects, GlenC, nper, dtf):
    permu = pd.DataFrame()
    for __ in range(nper):  # Doing 5 iterations.
        # Groups and positions will be assigned in order, so shuffle beforehand.
        random.shuffle(Subjects)
        control = Subjects[:GlenC]
        Treatment = Subjects[GlenC:]
        dtfCG = dtf.loc[dtf['Subject'].isin(control)]
        dtfTG = dtf.loc[dtf['Subject'].isin(Treatment)]
        res = calc_diff_kurt(dtfCG, dtfTG, 'Belief', 2)
        dt = pd.DataFrame(data=[res])
        permu = permu.append(dt, ignore_index=True)

    print(len(permu[2]))
    obs = abs(res0[2])  # Observed result of experiment difference kurtosis
    # to get numbers > k
    count = sum(i >= obs for i in abs(permu[2]))

    # printing the intersection
    print('Number of observations that are >= than the observed kurtosis in ' +
          str(nper) + ' permutations is:' + str(count))
    p_value = count/len(permu[2])
    corrected = (count+1)/(len(permu[2])+1)
    print(round(p_value, 3))
    print(round(corrected, 3))
    print('P(|Observed Diff|>={0:}) = {1:.2f}'.format(obs, p_value))

    a = 0.05
    if p_value < a:
        print('Reject the null hypothesis of no Treatment effect, thus treatment worked')
    else:
        print('Fail to reject the null hypothesis, thus treatment did not work')

    return permu
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

# Monte Carlo Figure


def MCfig(figu, dtf, dtf2, dtf3, dtf4, dtf5, x, bw):

    # firt 1000 permutations
    sns.kdeplot(data=dtf, x=dtf[x], bw_adjust=bw,
                ax=figu.axes[0])

    # 2500 permutations
    sns.kdeplot(data=dtf2, x=dtf2[x], bw_adjust=bw, ax=figu.axes[0])

    # 5500 permutatios
    sns.kdeplot(data=dtf3, x=dtf3[x], bw_adjust=bw, ax=figu.axes[0])

    # 7500 permutatios
    sns.kdeplot(data=dtf4, x=dtf4[x], bw_adjust=bw, ax=figu.axes[0])

    # 10000 permutatios
    sns.kdeplot(data=dtf5, x=dtf5[x], bw_adjust=bw, ax=figu.axes[0],
                legend=True).legend(labels=['1,000', '2,500', '5,000', '7,500', '10,000'])
#############################################################################
# # ################ $$$ Monte Carlo $$$ ######################
# Load the Data


dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
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

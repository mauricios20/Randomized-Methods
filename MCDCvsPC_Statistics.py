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


def calc_diff_mean(dtfCG, dtfTG, x, y, z, n):
    list = []
    meanxT = round(dtfTG[x].mean(), n)
    meanxC = round(dtfCG[x].mean(), n)
    Tx = round((meanxT-meanxC), n)
    meanyT = round(dtfTG[y].mean(), n)
    meanyC = round(dtfCG[y].mean(), n)
    Ty = round((meanyT-meanyC), n)
    meanzT = round(dtfTG[z].mean(), n)
    meanzC = round(dtfCG[z].mean(), n)
    Tz = round((meanzT-meanzC), n)
    list.extend((meanxC, meanxT, Tx, meanyC, meanyT, Ty, meanzC, meanzT, Tz))
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
        obs = abs(Tobs.loc[i, [x]])  # Observed result of experiment difference kurtosis
        # to get numbers > k
        count = sum(t >= obs for t in abs(PermuFrameDict[i][x]))

        p_value = count/len(PermuFrameDict[i])
        corrected = (count+1)/(len(PermuFrameDict[i])+1)

        dt = pd.DataFrame(data={'Subject': i, 'n': len(PermuFrameDict[i]), 'k': count, 'p_values': p_value, 'Correction': round(corrected, 2)})
        final_results = final_results.append(dt, ignore_index=True)

    hypo = []
    for p in final_results['p_values']:
        if p < a:
            hypo.append('Reject Ho')
        else:
            hypo.append('Fail to reject Ho')

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

res = calc_diff_mean(dtf40PC, dtf40DC, 'Belief', 'PerAllo', 'EAB', 2)
print(res)

# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
Subjects = dtf40.Subject.unique()
Years = dtf40.Year.unique()
Ylen = int(len(Years)/2)
DC = Years[:Ylen]
PC = Years[Ylen:]

# Total number of observations only for demostration
# print(Ylen)
# print(DC)
# print(PC)

# Create a data frame dictionary to store your data frames

DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
print(len(DataFrameDict))  # Make sure it equals the same number of subjects
print(DataFrameDict.keys()) # Look at the keys, Keys = Subject ID

Tobs = pd.DataFrame()
for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf40[dtf40['Subject'] == key]
    dtfDC = DataFrameDict[key][DataFrameDict[key].Year <= 20]
    dtfPC = DataFrameDict[key][DataFrameDict[key].Year >= 21]
    res = calc_diff_mean(dtfPC, dtfDC, 'Belief', 'PerAllo', 'EAB', 2)
    dt = pd.DataFrame(data=[res])
    Tobs = Tobs.append(dt, ignore_index=True)

Tobs.set_index(Subjects, inplace=True)
Tobs.rename(columns={0: "YcObsB", 1: "YtObsB", 2: "TObsB",
                    3: "YcObsPA", 4: "YtObsPA", 5: "TObsPA",
                    6: "YcObsE", 7: "YtObsE", 8: "TObsE"})


# #### Monte Carlo ########

random.seed(180)
PermuFrameDict = {elem: pd.DataFrame for elem in Subjects}

for key in PermuFrameDict.keys():
    PermuFrameDict[key] = pd.DataFrame()
    for __ in range(5000):  # Doing 2 iterations.
        # Groups and positions will be assigned in order, so shuffle beforehand.
        random.shuffle(Years)
        print(Years)
        DC = Years[:Ylen]
        print(DC)
        PC = Years[Ylen:]
        print(PC)
        dtfCG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(PC)]
        dtfTG = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(DC)]
        resMC = calc_diff_mean(dtfCG, dtfTG, 'Belief', 'PerAllo', 'EAB', 2)
        print(resMC)
        dtMC = pd.DataFrame(data=[resMC])
        PermuFrameDict[key] = PermuFrameDict[key].append(dtMC, ignore_index=True)

print(PermuFrameDict[43])
PermuFrameDict[105].rename(columns={0: "Y_{c}B", 1: "Y_{t}B", 2: "TB",
                    3: "Y_{c}PA", 4: "Y_{t}PA", 5: "TPA",
                    6: "Y_{c}E", 7: "Y_{t}E", 8: "TE"}) # Change Subject ID to see other results
# Belief is 2, PA is 5, and EA is 8

dt_Beliefs = result(2, 0.05)
dt_PerAllo = result(5, 0.05)
dt_EA = result(8, 0.05)

dt_Beliefs
dt_PerAllo
dt_EA

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

# For MC Calculation


def calc_diff_mean(fixed, b1, b2, x, y, z, n):
    list = []
    meanxb1 = round(b1[x].mean(), n)
    meanxb2 = round(b2[x].mean(), n)
    meanxf = round(fixed[x].mean(), n)
    Txb1 = round((meanxf-meanxb1), n)
    Txb2 = round((meanxf-meanxb2), n)

    meanyb1 = round(b1[y].mean(), n)
    meanyb2 = round(b2[y].mean(), n)
    meanyf = round(fixed[y].mean(), n)
    Tyb1 = round((meanyf-meanyb1), n)
    Tyb2 = round((meanyf-meanyb2), n)

    meanzb1 = round(b1[z].mean(), n)
    meanzb2 = round(b2[z].mean(), n)
    meanzf = round(fixed[z].mean(), n)
    Tzb1 = round((meanzf-meanzb1), n)
    Tzb2 = round((meanzf-meanzb2), n)
    list.extend((meanxf, meanyf, meanzf, meanxb1, meanyb1, meanzb1,
                meanxb2, meanyb2, meanzb2, Txb1, Tyb1, Tzb1, Txb2, Tyb2, Tzb2))
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

print(dtf40.columns)
# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Overall

FEB0 = dtf40[dtf40['Year'] <= 20]
PEB0 = dtf40[dtf40['Year'] >= 21]
# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
Subjects = dtf40.Subject.unique()
YearsFE = FEB0.Year.unique()
Years = PEB0.Year.unique()
Ylen = int(len(Years)/2)
B1 = Years[:Ylen]
B2 = Years[Ylen:]

print(YearsFE)
print(B1)
print(B2)
# Create a data frame dictionary to store your data frames

DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
print(len(DataFrameDict))  # Make sure it equals the same number of subjects
print(DataFrameDict.keys()) # Look at the keys, Keys = Subject ID

Tobs = pd.DataFrame()
for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf40[dtf40['Subject'] == key]
    dtfFE = DataFrameDict[key][DataFrameDict[key].Year.isin(YearsFE)]
    dtfB1 = DataFrameDict[key][DataFrameDict[key].Year.isin(B1)]
    # thresh_low = 11
    # thresh_high = 20
    # mask = (DataFrameDict[key].Year >= thresh_low) & (DataFrameDict[key].Year <= thresh_high)
    dtfB2 = DataFrameDict[key][DataFrameDict[key].Year.isin(B2)]
    res = calc_diff_mean(dtfFE, dtfB1, dtfB2, 'Belief', 'PerAllo', 'EAB', 2)
    dt = pd.DataFrame(data=[res])
    Tobs = Tobs.append(dt, ignore_index=True)

Tobs.set_index(Subjects, inplace=True)
print(Tobs)
Tobs.rename(columns={0: "YFE B", 1: "YFE PA", 2: "YFE EAB",
                    3: "YB1 B", 4: "YB1 PA", 5: "YB1 EAB",
                    6: "YB2 B", 7: "YB2 PA", 8: "YB2 EAB",
                    9: "TobsB1 B", 10: "TobsB1 PA", 11: "TObsB1 EAB",
                    12: "TobsB2 B", 13: "TobsB2 PA", 14: "TobsB2 EAB"})


# #### Monte Carlo ########

random.seed(180)
PermuFrameDict = {elem: pd.DataFrame for elem in Subjects}

for key in PermuFrameDict.keys():
    PermuFrameDict[key] = pd.DataFrame()
    dtfFE = DataFrameDict[key][DataFrameDict[key].Year.isin(YearsFE)]
    for __ in range(5000):  # Doing 2 iterations.
        # Groups and positions will be assigned in order, so shuffle beforehand.
        random.shuffle(Years)
        Years
        B1 = Years[:Ylen]
        B2 = Years[Ylen:]
        dtfB1 = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(B1)]
        dtfB2 = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(B2)]
        resMC = calc_diff_mean(dtfFE, dtfB2, dtfB1, 'Belief', 'PerAllo', 'EAB', 2)
        dtMC = pd.DataFrame(data=[resMC])
        PermuFrameDict[key] = PermuFrameDict[key].append(dtMC, ignore_index=True)

PermuFrameDict[105]

# Belief is 2, PA is 5, and EA is 8
dt_BeliefsB1 = result(9, 0.05)
dt_PerAlloB1 = result(10, 0.05)
dt_EAB1 = result(11, 0.05)

dt_BeliefsB2 = result(12, 0.05)
dt_PerAlloB2 = result(13, 0.05)
dt_EAB2 = result(14, 0.05)

dt_BeliefsB1
dt_PerAlloB1
dt_EAB1

dt_BeliefsB2
dt_PerAlloB2
dt_EAB2

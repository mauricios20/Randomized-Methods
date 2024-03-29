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


def calc_diff(fixed, b1, b2, x, n):
    list = []
    meanxb1 = round(b1[x].kurtosis(), n)
    meanxb2 = round(b2[x].kurtosis(), n)
    meanxf = round(fixed[x].kurtosis(), n)
    Txb1 = round((abs(meanxf)-abs(meanxb1)), n)
    Txb2 = round((abs(meanxf)-abs(meanxb2)), n)
    Txb12 = round((abs(meanxb1)-abs(meanxb2)), n)

    list.extend((meanxf, meanxb1, meanxb2, abs(Txb1), abs(Txb2), abs(Txb12)))
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

        dt = pd.DataFrame(data={'Subject': i, 'r': count, 'p_values': p_value, 'Correction': round(corrected, 2)})
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

print(dtf40.columns)
# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Overall

thresh_low = 5    # 1929
thresh_high = 16  # 1940
# mask = (DataFrameDict[key].Year >= thresh_low) & (DataFrameDict[key].Year <= thresh_high)
mask = (dtf40.Year >= thresh_low) & (dtf40.Year <= thresh_high)

FEB0 = dtf40[mask]
PEB0 = dtf40[dtf40['Year'] >= 17]

FEB0.head(17)
PEB0.head(25)
# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
exclude = [41, 104, 42, 43, 45, 47, 55, 59, 106, 108, 110, 114, 118, 119]
dtf = dtf40.loc[~dtf40.Subject.isin(exclude)]
Subjects = dtf.Subject.unique()

YearsFE = FEB0.Year.unique()
Years = PEB0.Year.unique()
Ylen = int(len(Years)/2)
B1 = Years[:Ylen]
B2 = Years[Ylen:]

# print(len(Years))
# print(YearsFE)
# print(B1)
# print(B2)
# Create a data frame dictionary to store your data frames

DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
print(len(DataFrameDict))  # Make sure it equals the same number of subjects
print(DataFrameDict.keys()) # Look at the keys, Keys = Subject ID

Tobs = pd.DataFrame()
for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['Subject'] == key]
    dtfFE = DataFrameDict[key][DataFrameDict[key].Year.isin(YearsFE)]
    dtfB1 = DataFrameDict[key][DataFrameDict[key].Year.isin(B1)]

    dtfB2 = DataFrameDict[key][DataFrameDict[key].Year.isin(B2)]
    res = calc_diff(dtfFE, dtfB1, dtfB2, 'Belief', 3)
    dt = pd.DataFrame(data=[res])
    Tobs = Tobs.append(dt, ignore_index=True)

Tobs.set_index(Subjects, inplace=True)
Tobs
print(Tobs.to_latex(index=True))
Tobs.rename(columns={0: "YFE", 1: "YB1", 2: "YB2",
                    3: "TB1", 4: "TB2", 5: "TB12"})


# #### Monte Carlo ########

random.seed(180)
PermuFrameDict = {elem: pd.DataFrame for elem in Subjects}

for key in PermuFrameDict.keys():
    PermuFrameDict[key] = pd.DataFrame()
    dtfFE = DataFrameDict[key][DataFrameDict[key].Year.isin(YearsFE)]
    for __ in range(10000):  # Doing 2 iterations.
        # Groups and positions will be assigned in order, so shuffle beforehand.
        random.shuffle(Years)
        Years
        B1 = Years[:Ylen]
        B2 = Years[Ylen:]
        dtfB1 = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(B1)]
        dtfB2 = DataFrameDict[key].loc[DataFrameDict[key].Year.isin(B2)]
        resMC = calc_diff(dtfFE, dtfB2, dtfB1, 'Belief', 3)
        dtMC = pd.DataFrame(data=[resMC])
        PermuFrameDict[key] = PermuFrameDict[key].append(dtMC, ignore_index=True)

# Belief is 2, PA is 5, and EA is 8
dt_BeliefsB1 = result(3, 0.05)
dt_BeliefsB2 = result(4, 0.05)
dt_BeliefsB12 = result(5, 0.05)

dt_BeliefsB1
dt_BeliefsB2

B1_B2 = pd.merge(dt_BeliefsB1, dt_BeliefsB2, on ='Subject')
print(B1_B2.to_latex(index=False))

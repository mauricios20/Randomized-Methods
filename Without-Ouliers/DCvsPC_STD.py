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


def calc_diff(dtfCG, dtfTG, x, n):
    list = []
    Td = round(dtfTG[x].std(), n)
    Cd = round(dtfCG[x].std(), n)
    T = round((Td - Cd), n)
    list.extend((Td, Cd, T))
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
        res = calc_diff(dtfCG, dtfTG, 'Belief', 3)
        dt = pd.DataFrame(data=[res])
        permu = permu.append(dt, ignore_index=True)

    print(len(permu[2]))
    obs = abs(res0[2])  # Observed result of experiment difference kurtosis
    # to get numbers > k
    count = sum(i >= obs for i in abs(permu[2]))

    # printing the intersection
    print('Number of observations that are >= than the observed kurtosis in ' +
          str(nper) + ' permutations is:' + str(count))
    p_value = count / nper
    corrected = (count + 1) / (nper + 1)
    print('P(|Observed Diff|>={0:}) = {1:.2f}'.format(obs, p_value))

    a = 0.05
    if p_value < a:
        dt = pd.DataFrame(data={'k': nper, 'r': count, 'p_values': round(p_value, 3), 'Correction': round(
            corrected, 3), 'Hypothesis': 'Reject'}, index=[0])
    else:
        dt = pd.DataFrame(data={'k': nper, 'r': count, 'p_values': round(p_value, 3), 'Correction': round(
            corrected, 3), 'Hypothesis': 'Fail to Reject'}, index=[0])

    return permu, dt
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
                legend=True).legend(labels=['1,000', '2,500',
                                            '5,000', '7,500', '10,000'])


def remove_outliers(data, x):
    # Define Quartiles
    Q1 = data[x].quantile(0.25)
    Q3 = data[x].quantile(0.75)
    IQR = Q3 - Q1

    # Old Shape
    print("Old Shape", data.shape)
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    print("Upper Bound:", upper)
    OutlierUp = data.index[data[x] >= upper].tolist()
    print(OutlierUp)

    print("Lower Bound:", lower)
    OutlierLow = data.index[data[x] <= lower].tolist()
    print(OutlierLow)

    # Removing Outliers
    dtf = data.drop(OutlierUp, axis=0)
    dtfNO = dtf.drop(OutlierLow, axis=0)
    print("New Shape", dtfNO.shape)
    return dtfNO
#############################################################################
# # ################ $$$ Monte Carlo $$$ ######################
# Load the Data


dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)


# # ############### $$ Post Crash vs. During Crash $$ ####################

dtf40PC = dtf40[dtf40['Year'] >= 21]
dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40DC['Subject'] = dtf40DC['Subject'].astype(str) + 'DC'
dtf40PC['Subject'] = dtf40PC['Subject'].astype(str) + 'PC'

dtf_PC = remove_outliers(dtf40PC, 'Belief')
dtf_DC = remove_outliers(dtf40DC, 'Belief')

res0 = calc_diff(dtf_DC, dtf_PC, 'Belief', 3)
dtfall = dtf_DC.append(dtf_PC, sort=False)
Subjects = dtfall.Subject.unique()
GlenC = len(dtf_DC.Subject.unique())
print(res0)

# Run Multiple Permutations
random.seed(180)
obs = abs(res0[2])
permu1, dt1 = MC(Subjects, GlenC, 1000, dtfall)
permu2, dt2 = MC(Subjects, GlenC, 2500, dtfall)
permu3, dt3 = MC(Subjects, GlenC, 5000, dtfall)
permu4, dt4 = MC(Subjects, GlenC, 7500, dtfall)
permu5, dt5 = MC(Subjects, GlenC, 10000, dtfall)

# print(permu1.head(3).to_latex(index=True))
# print(permu3.head(3).to_latex(index=True))
print(permu5.head(3).to_latex(index=True))

final_dtf = pd.concat([dt1, dt2, dt3, dt4, dt5])
print(final_dtf.to_latex(index=False))

# Plot kernel densities of each permuatation
fig1, axes = plt.subplots()
MCfig(fig1, permu1, permu2, permu3, permu4, permu5, 2, 0.5)
fig1.axes[0].set_xlabel('')
fig1.axes[0].axvline(x=obs, color='black', linestyle="--", linewidth=1)
fig1.axes[0].axvline(x=-obs, color='black', linestyle="--", linewidth=1)
fig1.axes[0].text(0.005, 50, str(obs), fontweight='bold', fontsize='x-large')
fig1.axes[0].text(-0.017, 50, str(-obs), fontweight='bold', fontsize='x-large')
plt.show()

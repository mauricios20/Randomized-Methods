import os
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

os.chdir("C:/Users/mauri/Dropbox/Family Room/1 Hi Lo Exp Data/Randomization Methods/Data")

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
    print(p_value)
    print(round(corrected, 3))
    print('P(|Observed Diff|>={0:}) = {1:.2f}'.format(obs, p_value))

    a = 0.05
    if p_value < a:
        print('Reject the null hypothesis of no Treatment effect, thus treatment worked')
    else:
        print('Fail to reject the null hypothesis, thus treatment did not work you lil piece of shit')

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


# #  ################ $$ Per Subject 40 Cohort $$ ####################

dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)


res0 = calc_diff_kurt(dtf20, dtf40, 'Belief', 2)
dtfall = dtf20.append(dtf40, sort=False)
Subjects = dtfall.Subject.unique()
GlenC = len(dtf20.Subject.unique())


# Run Multiple Permutations
random.seed(180)
obs = abs(res0[2])
permu1 = MC(Subjects, GlenC, 1000, dtfall)
permu2 = MC(Subjects, GlenC, 2500, dtf40)
permu3 = MC(Subjects, GlenC, 5000, dtf40)
permu4 = MC(Subjects, GlenC, 7500, dtf40)
permu5 = MC(Subjects, GlenC, 10000, dtf40)

print(permu1.head(3).to_latex(index=True))
print(permu3.head(3).to_latex(index=True))
print(permu5.head(3).to_latex(index=True))
# Plot kernel densities of each permuatation
fig, axes = plt.subplots()
MCfig(fig, permu1, permu2, permu3, permu4, permu5, 2, 0.5)
fig.axes[0].set_xlabel('Kurtosis Difference')
fig.axes[0].axvline(x=obs, color='black', linestyle="--", linewidth=1)
fig.axes[0].axvline(x=-obs, color='black', linestyle="--", linewidth=1)
plt.show()

# ######################## # Sanity Check # ###################################
# print(groupings[0][0])
# print(groupings[0][1])
# dtfCG = dtf40.loc[dtf40['Subject'].isin(groupings[0][0])]
# dtfTG = dtf40.loc[dtf40['Subject'].isin(groupings[0][1])]
#
# print(calc_diff_kurt(dtfCG, dtfTG, 'Belief', 2))
# res1 = calc_diff_kurt(dtfCG, dtfTG, 'Belief', 2)
# # # Check
# # print(dtfCG.head(5))
# # print(dtfCG.tail(5))
# # print(dtfTG.head(5))
# # print(dtfTG.tail(5))
# # print(len(dtfCG['Subject']))  # Check if N matches group  (760)
# # print(dtfCG['Subject'].unique())  # Check if Lenght of group matches (19)
#
#
# firs = pd.DataFrame(data=[res0])
# per = pd.DataFrame(data=[res1])
# final = firs.append(per)
# print(final)
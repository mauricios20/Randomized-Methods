import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
from scipy import stats
import scipy.stats as stat

# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# # Define Functions

# Split Data Frame


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0)

    # Get Control and Treatmet Groups
    dtfCG = dtf[dtf[tname] == CG]

    dtfTG = dtf[dtf[tname] == TG]

    return dtf, dtfCG, dtfTG

# Create KernelDensity Figures


def kdefig1(figu, dtfCG, dtfTG, dtfTG2, x, bw):


    # Add first plot to figure
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw)

    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw)

    sns.kdeplot(data=dtfTG2, x=x, bw_adjust=bw)


def kdefig2(figu, dtfCG, dtfTG, dtfTG2, x, bw):
    # Add Second plot to figure
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw,
                cumulative=True, common_norm=False,
                common_grid=True)
    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw,
                cumulative=True, common_norm=False,
                common_grid=True)

    sns.kdeplot(data=dtfTG2, x=x, bw_adjust=bw,
                cumulative=True, common_norm=False,
                common_grid=True)


def boxes(figu, dtfCG, dtfTG2, y):
    # Define boxes
    sns.boxplot(data=dtfCG, y=y, ax=figu.axes[0])
    sns.boxplot(data=dtfTG2, y=y, ax=figu.axes[1], color='#2ca02c')


def violins(figu, dtfCG, dtfTG2, y):
    sns.violinplot(data=dtfCG, y=y, ax=figu.axes[0])
    sns.violinplot(data=dtfTG2, y=y, ax=figu.axes[1], color='#2ca02c')


def regplots(figu, dtfCG, dtfTG2, x, y):
    sns.regplot(data=dtfCG, x=x, y=y, ax=figu.axes[0])
    sns.regplot(data=dtfTG2, x=x, y=y, ax=figu.axes[1], color='#2ca02c')


def remove_outliers(data, x, name):
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
    obsup = len(OutlierUp)

    print("Lower Bound:", lower)
    OutlierLow = data.index[data[x] <= lower].tolist()
    obslow = len(OutlierLow)

    totalout = obsup+obslow
    # Removing Outliers
    dtf = data.drop(OutlierUp, axis=0)
    dtfNO = dtf.drop(OutlierLow, axis=0)
    print("New Shape", dtfNO.shape)

    dt = pd.DataFrame(data={'Name': name, 'Q1': round(Q1, 2), 'Q3': round(Q3, 3),
                            'IQR': IQR, 'Upper Bound': round(upper, 3),
                            'Lower Bound': round(lower, 3),
                            'obs>Upper': obsup, 'obs<Lower': obslow,
                            'Total Outliers': totalout}, index=[0])
    return dtfNO, dt

# ##################### Display Data ####################################


dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

# #  ################ $$ During Crash vs. No Crash $$ ####################

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

# ~~~~~~~~~~~~~ Remove Outliers ~~~~~~~~~~~~~~~~~~~
dtf_DC, dtnumDC = remove_outliers(dtf40DC, 'Belief', 'During Crash')
dtf_PC, dtnumPC = remove_outliers(dtf40PC, 'Belief', 'Post Crash')
# fig = plt.figure()
# kdefig1(fig, dtf40DC, dtf20, dtf40PC, 'Belief', 0.6)
# plt.legend(['DC', 'NC', 'PC'])
# plt.grid(True)
#
# fig1 = plt.figure()
# kdefig2(fig1, dtf40DC, dtf20, dtf40PC, 'Belief', 0.6)
# plt.legend(['DC', 'NC', 'PC'])
# plt.grid(True)


fig2, axes = plt.subplots(1, 2, sharey=True)
boxes(fig2, dtf_DC, dtf_PC, 'Belief')
axes[1].set(ylabel=None)
axes[1].set(ylabel=None)
axes[0].legend(['DC'])
axes[1].legend(['PC'])


fig3, axes = plt.subplots(1, 2, sharey=True)
violins(fig3, dtf_DC, dtf_PC, 'Belief')
axes[1].set(ylabel=None)
axes[1].set(ylabel=None)
axes[0].legend(['DC'])
axes[1].legend(['PC'])
plt.show()
#
#
# fig4, axes = plt.subplots(1, 3, sharey=True)
# regplots(fig4, dtf40DC, dtf20, dtf40PC, 'PerAllo', 'Belief')
# axes[1].set(ylabel=None)
# axes[2].set(ylabel=None)
# axes[0].legend(['DC'])
# axes[1].legend(['NC'])
# axes[2].legend(['PC'])
# for i in range(0, 3):
#     axes[i].grid(True)
#
#
# plt.show()
# fig5, axes = plt.subplots(1, 3, sharey=True)
# regplots(fig5, dtf40DC, dtf20, dtf40PC, 'Objective', 'Belief')
# axes[1].set(ylabel=None)
# axes[2].set(ylabel=None)
# axes[0].legend(['DC'])
# axes[1].legend(['NC'])
# axes[2].legend(['PC'])
# for i in range(0, 3):
#     axes[i].grid(True)
# plt.show()

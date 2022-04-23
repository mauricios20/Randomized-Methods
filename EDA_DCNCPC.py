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


def boxes(figu, dtfCG, dtfTG, dtfTG2, y):
    # Define boxes
    sns.boxplot(data=dtfCG, y=y, ax=figu.axes[0])
    sns.boxplot(data=dtfTG, y=y, ax=figu.axes[1], color='#ff7f0e')
    sns.boxplot(data=dtfTG2, y=y, ax=figu.axes[2], color='#2ca02c')


def violins(figu, dtfCG, dtfTG, dtfTG2, y):
    sns.violinplot(data=dtfCG, y=y, ax=figu.axes[0])
    sns.violinplot(data=dtfTG, y=y, ax=figu.axes[1], color='#ff7f0e')
    sns.violinplot(data=dtfTG2, y=y, ax=figu.axes[2], color='#2ca02c')


def regplots(figu, dtfCG, dtfTG, dtfTG2, x, y):
    sns.regplot(data=dtfCG, x=x, y=y, ax=figu.axes[0])
    sns.regplot(data=dtfTG, x=x, y=y, ax=figu.axes[1], color='#ff7f0e')
    sns.regplot(data=dtfTG2, x=x, y=y, ax=figu.axes[2], color='#2ca02c')


# ##################### Display Data ####################################
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

# #  ################ $$ During Crash vs. No Crash $$ ####################

dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

fig = plt.figure()
kdefig1(fig, dtf40DC, dtf20, dtf40PC, 'Belief', 0.6)
plt.legend(['DC', 'NC', 'PC'])
plt.grid(True)

fig1 = plt.figure()
kdefig2(fig1, dtf40DC, dtf20, dtf40PC, 'Belief', 0.6)
plt.legend(['DC', 'NC', 'PC'])
plt.grid(True)



fig2, axes = plt.subplots(1, 3, sharey=True)
boxes(fig2, dtf40DC, dtf20, dtf40PC, 'Belief')
axes[1].set(ylabel=None)
axes[2].set(ylabel=None)
axes[0].legend(['DC'])
axes[1].legend(['NC'])
axes[2].legend(['PC'])


fig3, axes = plt.subplots(1, 3, sharey=True)
violins(fig3, dtf40DC, dtf20, dtf40PC, 'Belief')
axes[1].set(ylabel=None)
axes[2].set(ylabel=None)
axes[0].legend(['DC'])
axes[1].legend(['NC'])
axes[2].legend(['PC'])


fig4, axes = plt.subplots(1, 3, sharey=True)
regplots(fig4, dtf40DC, dtf20, dtf40PC, 'PerAllo', 'Belief')
axes[1].set(ylabel=None)
axes[2].set(ylabel=None)
axes[0].legend(['DC'])
axes[1].legend(['NC'])
axes[2].legend(['PC'])
for i in range(0, 3):
    axes[i].grid(True)

fig5, axes = plt.subplots(1, 3, sharey=True)
regplots(fig5, dtf40DC, dtf20, dtf40PC, 'Objective', 'Belief')
axes[1].set(ylabel=None)
axes[2].set(ylabel=None)
axes[0].legend(['DC'])
axes[1].legend(['NC'])
axes[2].legend(['PC'])
for i in range(0, 3):
    axes[i].grid(True)
plt.show()

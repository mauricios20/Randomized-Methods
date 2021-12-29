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


# Marginal Distribution


def margfig(figu, dtf, x, bw, dtfob, obj):
    # Top of Figure
    Sp = [0.2, 0.3, 0.4, 0.5]  # Smoothing Parameter
    for s in Sp:
        sns.kdeplot(data=dtf, x=x, bw_adjust=s,
                    ax=figu.axes[0]).legend(labels=Sp)

    # Bottom Part of Figure
    sns.kdeplot(data=dtf, x=x, bw_adjust=bw, ax=figu.axes[1])

    # Add Ibjective Distribution
    if obj:
        sns.kdeplot(data=dtfob, x="Objective", bw_adjust=bw, ax=figu.axes[1],
                    linestyle="--", color="red",
                    legend=True).legend(labels=['Observed', 'Objective'])


# Create KernelDensity Figures


def kdefig(figu, dtfCG, dtfTG, x, bw):


    # Add first plot to figure
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw,
                ax=figu.axes[0], fill=True)

    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw,
                ax=figu.axes[0], fill=True)


    # Add Second plot to figure
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw,
                cumulative=True, common_norm=False,
                common_grid=True, ax=figu.axes[1])
    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw,
                cumulative=True, common_norm=False,
                common_grid=True, ax=figu.axes[1])

def boxes(figu, dtfCG, dtfTG, y):
    # Define boxes
    sns.boxplot(data=dtfCG, y=y, ax=figu.axes[0])
    sns.boxplot(data=dtfTG, y=y, ax=figu.axes[1], color='#ff7f0e')

# ##################### Display Data ####################################
# Split Data
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

# #  ################ $$ During Crash vs. No Crash $$ ####################

dtf40DC = dtf40[dtf40['Year'] <= 20]

fig, axes = plt.subplots(2, sharex=True)
kdefig(fig, dtf20, dtf40DC, 'Belief', 0.4)
axes[0].legend(['No Crash', 'During Crash'])
axes[0].set(xlabel=None)
axes[1].legend(['No Crash', 'During Crash'])


fig2, axes = plt.subplots(1,2, sharey=True)
boxes(fig2, dtf20, dtf40DC, 'Belief')
axes[1].set(ylabel=None)

# #  ################ $$ Post Crash vs. No Crash $$ ####################

dtf40PC = dtf40[dtf40['Year'] >= 21]

fig3, axes = plt.subplots(2, sharex=True)
kdefig(fig3, dtf20, dtf40PC, 'Belief', 0.4)
axes[0].legend(['No Crash', 'Post Crash'])
axes[0].set(xlabel=None)
axes[1].legend(['No Crash', 'Post Crash'])


fig4, axes = plt.subplots(1,2, sharey=True)
boxes(fig4, dtf20, dtf40PC, 'Belief')
axes[1].set(ylabel=None)

# #  ################ $$ During Crash vs. Post Crash $$ ####################


fig5, axes = plt.subplots(2, sharex=True)
kdefig(fig5, dtf40DC, dtf40PC, 'Belief', 0.4)
axes[0].legend(['During Crash', 'Post Crash'])
axes[0].set(xlabel=None)
axes[1].legend(['During Crash', 'Post Crash'])


fig6, axes = plt.subplots(1,2, sharey=True)
boxes(fig6, dtf40DC, dtf40PC, 'Belief')
axes[1].set(ylabel=None)
plt.show()

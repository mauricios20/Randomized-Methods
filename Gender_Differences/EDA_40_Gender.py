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


# ##################### Display Data ####################################
dtf40, dtf40ST, dtf40LT = split('40PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20, dtf20ST, dtf20LT = split('20PerSubjectData.csv',
                                'Belief', 'Treatment (D)', 0, 1)

dtf20.sort_values(by='Sex', ascending=False, inplace=True)
dt = pd.concat([dtf20, dtf40]).sort_values(by='Sex', ascending=False)

# #  ################ $$ During Crash vs. No Crash $$ ####################
dtf40DC = dtf40[dtf40['Year'] <= 20]
dtf40PC = dtf40[dtf40['Year'] >= 21]

fig, axes = plt.subplots()
sns.boxplot(data=dt, x='Condition', y='Belief', hue='Sex', ax=fig.axes[0])


fig2, axes = plt.subplots()
sns.kdeplot(data=dtf40, x='Belief', bw_adjust=0.5, common_norm=False,
            common_grid=True, hue='Sex', fill=True, linewidth=0.5, ax=fig2.axes[0])


fig3, axes = plt.subplots(1, 3, sharey=True)
sns.countplot(data=dtf40DC, x='BPay', hue='Sex', ax=fig3.axes[0])
sns.countplot(data=dtf40PC, x='BPay', hue='Sex', ax=fig3.axes[1])
sns.countplot(data=dtf20, x='BPay', hue='Sex', ax=fig3.axes[2])
axes[1].set(ylabel=None, title='PC', xlabel='Incentive Pay')
axes[0].set(title='DC', xlabel=None)
axes[2].set(ylabel=None, title='NC', xlabel=None)
axes[0].legend([], frameon=False)
axes[1].legend([], frameon=False)

dtf40_Group = dtf40.groupby(['Year', 'Sex']).mean().reset_index()
dtf20_Group = dtf20.groupby(['Year', 'Sex']).mean().reset_index().sort_values(by='Sex', ascending=False)

dtf40_Group = dtf40.groupby(['Blocks']).mean().reset_index()
dtf40_Group

fig4, axes = plt.subplots()
sns.lineplot(data=dtf40_Group, x='Year', y='Belief', hue='Sex', markers=True, ax=fig4.axes[0])

fig42, axes = plt.subplots()
sns.lineplot(data=dtf20_Group, x='Year', y='Belief', hue='Sex', markers=True, ax=fig42.axes[0])

dtf40_DC_G = dtf40DC.groupby(['Year', 'Sex']).mean().reset_index().sort_values(by='Sex', ascending=False)
dtf40_PC_G = dtf40PC.groupby(['Year', 'Sex']).mean().reset_index().sort_values(by='Sex', ascending=False)


fig5, axes = plt.subplots(1, 2, sharey=True)
sns.lineplot(data=dtf40_DC_G, x='Year', y='Belief', hue='Sex',
             ax=fig5.axes[0])
sns.lineplot(data=dtf40_PC_G, x='Year', y='Belief', hue='Sex',
             ax=fig5.axes[1])
axes[0].legend([], frameon=False)

fig6, axes = plt.subplots()
sns.pointplot(data=dtf40, x="Blocks", y="Belief", hue='Sex', ax=fig6.axes[0])

fig7, axes = plt.subplots()
sns.pointplot(data=dtf40, x="Blocks", y="Belief", ax=fig7.axes[0])
axes.set(title='Linear Predicitions', xlabel=None)


g = sns.FacetGrid(dtf40, col="Blocks")
g.map_dataframe(sns.pointplot, x="Sex", y="Belief")
g.add_legend()

p = sns.FacetGrid(dtf40, col="Blocks", hue="Sex")
p.map_dataframe(sns.ecdfplot, x="Belief")
p.add_legend()

plt.show()

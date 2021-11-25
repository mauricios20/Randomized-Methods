import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pylab
import statsmodels.api as sm
from scipy.stats import kstest, norm
from scipy import stats

# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

os.chdir("C:/Users/mauri/Dropbox/Family Room/1 Hi Lo Exp Data/Randomization Methods/Data")

# # Define Functions
# Calculate Statistics
# $ Add more Stats as needed $


def calc_sum_stats(boot_df):
    sum_stats = boot_df.describe().T[['count', 'mean', 'std', 'min', 'max']]
    sum_stats['median'] = boot_df.median()
    sum_stats['skew'] = boot_df.skew()
    sum_stats['kurtosis'] = boot_df.kurtosis()
    sum_stats['IQR'] = boot_df.quantile(0.75) - boot_df.quantile(0.25)
    return sum_stats.T

# Split Data Frame


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0)
    st = calc_sum_stats(dtf[col])

    # Get Control and Treatmet Groups
    dtfCG = dtf[dtf[tname] == CG]
    stCG = calc_sum_stats(dtfCG[col])

    dtfTG = dtf[dtf[tname] == TG]
    stTG = calc_sum_stats(dtfTG[col])

    # Concat Stats
    stats = pd.concat([st, stCG, stTG], axis=1,
                      keys=['Overall', 'Control', 'Treatment'])
    return dtf, dtfCG, dtfTG, stats

# Create KernelDensity Figures


def kdefig(figu, dtf, x, bw):
    # Top of Figure
    Sp = [0.2, 0.3, 0.4, 0.5]  # Smoothing Parameter
    for s in Sp:
        sns.kdeplot(data=dtf, x=x, bw_adjust=s,
                    ax=figu.axes[0]).legend(labels=Sp)

    figu.axes[0].set_title('Smoothing Parameters')
    # Bottom Part of Figure
    sns.kdeplot(data=dtf, x=x, bw_adjust=bw, ax=figu.axes[1])
    figu.axes[1].set_title(str(bw)+' Smoothing')

# Obtain the KernelDensity for each Treatmet


def kdefigCT(figu, dtf, dtfCG, dtfTG, x, bw, tname):
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw,
                ax=figu.axes[0], fill=True).set(xlabel=None)
    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw,
                ax=figu.axes[2], color='darkorange', fill=True)
    figu.axes[0].set_title('KDE Control vs Treatmet')

    sns.histplot(data=dtf, x=x, hue=tname, ax=figu.axes[1]).set(xlabel=None)
    sns.kdeplot(data=dtf, x=x, bw_adjust=bw,
                hue=tname, cumulative=True, common_norm=False,
                common_grid=True, ax=figu.axes[3]).set(ylabel=None)
    figu.axes[1].set_title('Histograms & CDFs')

# Obtain Violin and Boxplots


def vioandbox(figu, dtf, tname, y, bw):
    sns.violinplot(data=dtf, x=tname, y=y, ax=figu.axes[0], bw=bw)
    figu.axes[0].set_title('Violin Plot')

    sns.boxplot(data=dtf, x=tname, y=y, ax=figu.axes[1]).set(ylabel=None)
    figu.axes[1].set_title('Box Plot')

# Joint Plot AveExp with Ave Stock Allocation


def contrast(dtf, dtfCG, dtfTG, dtOB, x, y, ob, tname, levels):
    g = sns.jointplot(data=dtf, x=x, y=y,
                      hue=tname)
    g.plot_joint(sns.kdeplot, zorder=0, levels=levels)
    g.refline(x=dtfTG[x].mean(), y=dtfTG[y].mean(), color='orange')
    g.refline(x=dtfCG[x].mean(), y=dtfCG[y].mean(), color='blue')
    g.refline(x=dtOB[ob].mean(), color='r')
    g.set_axis_labels('Average Expectation', '(%) Stock Allocation')


#######################################################################
# # Exploratory Data Analysis

#  ################ $$ Objective Return Distribution $$ ####################
dfOb = pd.read_csv('ObjDistribution.csv', header=0)
dfObNC = dfOb[dfOb['Actual Year'] >= 1945]
# ################# $$ 20 Cohort Visualizations $$ #########################
dtf20, dtf20ST, dtf20LT, sts20 = split('20PeriodGroup.csv',
                                       'AveExp',
                                       'Treatment (D)', 0, 1)

# Create First Figure KDE
fig, axes = plt.subplots(2, sharex=True)
fig.suptitle('20 Cohort - Kernel Density Estimation')
kdefig(fig, dtf20, 'AveExp', 0.2)

# Create Second Figure Group Comparison
fig1, ax = plt.subplots(2, 2)
for i in range(0, 4):
    fig1.axes[i].grid(True)
fig1.suptitle('20 Cohort - Treatmet Comparison')
kdefigCT(fig1, dtf20, dtf20ST, dtf20LT, 'AveExp', 0.2, 'Treatment (D)')

# Create Third Visualization
fig2, axes = plt.subplots(1, 2, sharey=True)
fig2.suptitle('20 Cohort - Treatmet Comparison')
vioandbox(fig2, dtf20, 'Treatment (D)', 'AveExp', 0.2)

# Create Bivariate Plot
contrast(dtf20, dtf20ST, dtf20LT, dfObNC, 'AveExp', 'AveSA', 'Objective',
         'Treatment (D)', 7)

# ################# $$ 40 Cohort Visualizations $$ #########################
dtf40, dtf40ST, dtf40LT, sts40 = split('40PeriodGroup.csv',
                                       'AveExp',
                                       'Treatment (D)', 0, 1)
# Create First Figure KDE
fig3, axes = plt.subplots(2, sharex=True)
fig3.suptitle('40 Cohort - Kernel Density Estimation')
kdefig(fig3, dtf40, 'AveExp', 0.2)

# Create Second Figure Group Comparison
fig4, ax = plt.subplots(2, 2)
for i in range(0, 4):
    fig1.axes[i].grid(True)
fig4.suptitle('40 Cohort - Treatmet Comparison')
kdefigCT(fig4, dtf40, dtf40ST, dtf40LT, 'AveExp', 0.2, 'Treatment (D)')

# Create Third Visualization
fig5, axes = plt.subplots(1, 2, sharey=True)
fig5.suptitle('40 Cohort - Treatmet Comparison')
vioandbox(fig5, dtf40, 'Treatment (D)', 'AveExp', 0.2)

# Create Bivariate Plot
contrast(dtf40, dtf40ST, dtf40LT, dfOb, 'AveExp', 'AveSA', 'Objective',
         'Treatment (D)', 5)

# #####################################################################
# # Compare Stats with Objective Distribution
stOb = calc_sum_stats(dfOb['Objective'])

# SW_test(dfOb, 'Objective')
stObNC = calc_sum_stats(dfObNC['Objective'])

G20stats = pd.concat([sts20, stObNC], axis=1)
G40stats = pd.concat([sts40, stOb], axis=1)
print(G20stats)
print(G40stats)

# fig5, ax = plt.subplots(2,  sharex=True)
# sns.kdeplot(data=dfOb, x="Rdecimal", bw_adjust=0.2, ax=fig1.axes[2],
#             linestyle="--", color="r", legend=True)
#
# fig5.axes[0].set_title('Objective Kernel Distribution')

# plt.show()

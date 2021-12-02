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

os.chdir("C:/Users/mauri/Dropbox/Family Room/1 Hi Lo Exp Data/Randomization Methods/Data")

# # Define Functions
# Calculate Statistics
# $ Add more Stats as needed $


def calc_sum_stats(boot_df):
    sum_stats = boot_df.describe().T[['count', 'mean', 'std', 'min', 'max']]
    sum_stats['variance'] = statistics.variance(boot_df)
    sum_stats['SE'] = stat.sem(boot_df)
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


def kdefig(figu, dtfCG, dtfTG, x, y, bw, dtfob, obj):
    # Add first plot to figure
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw,
                ax=figu.axes[0], fill=True).set(xlabel=None)

    # Add Second plot to figure
    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw,
                ax=figu.axes[0], fill=True).set(xlabel=None)

    # Add Ibjective Distribution
    if obj:
        f = sns.kdeplot(data=dtfob, x="Objective", bw_adjust=bw, ax=figu.axes[0],
                        linestyle="--", color="red",
                        legend=True)
        f.set(xlabel=None)
        f.legend(labels=['Objective', 'Control', 'Treatment'])
    # CDFs
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw, cumulative=True, common_norm=True,
                common_grid=True, ax=figu.axes[1]).set(ylabel=None, xlabel=None)

    d = sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw, cumulative=True, common_norm=False,
                    common_grid=True, ax=figu.axes[1])
    d.set(ylabel=None, xlabel=None)
    d.legend(labels=['Control', 'Treatment'])
    # Regression
    # get coeffs of linear fit
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        dtfCG[x], dtfCG[y])
    # use line_kws to set line label for legend
    g = sns.regplot(x="Belief", y="PerAllo", data=dtfCG,
                    line_kws={'label':
                              "R^2:{0: .2f}".format(r_value)},
                    ax=figu.axes[2])
    g.set_ylabel('(%) Stock Allocation')
    g.set_xlabel('Average Belief')
    g.legend(loc='upper left')

    # get coeffs of linear fit
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        dtfTG[x], dtfTG[y])
    # use line_kws to set line label for legend
    g = sns.regplot(x="Belief", y="PerAllo", data=dtfTG,
                    line_kws={'label': "R^2:{0: .2f}".format(r_value)},
                    ax=figu.axes[3], color='#ff7f0e')
    g.set_ylabel('(%) Stock Allocation')
    g.set_xlabel('Average Belief')
    g.legend(loc='upper left')


# Two figures two axis


def two_scales(ax1, x, data1, data2, c1, c2):
    ax1.plot(x, data1, 'o-', color=c1)
    ax1.set_xlabel('Period')
    ax1.set_ylabel('Average Belief')
    ax1.set_xticks(range(1, 41, 1))
    ax1.axvspan(1, 2, alpha=0.2, color='crimson')
    ax1.axvspan(4, 7, alpha=0.2, color='red')
    ax1.axvspan(9, 10, alpha=0.2, color='crimson')
    ax1.axvspan(11, 13, alpha=0.2, color='crimson')
    ax1.axvspan(14, 17, alpha=0.2, color='silver')
    ax1.axvspan(21, 22, alpha=0.2, color='crimson')
    ax1.axvspan(27, 29, alpha=0.2, color='silver')
    ax1.axvspan(30, 33, alpha=0.2, color='crimson')
    ax1.axvspan(34, 36, alpha=0.2, color='crimson')
    ax1.axvspan(37, 38, alpha=0.2, color='silver')
    ax1.legend(labels=['Ave Belief'])
    ax2 = ax1.twinx()
    ax2.plot(x, data2, 'x--', color=c2, mec='black')
    ax2.axvspan(1, 2, alpha=0.2, color='crimson')
    ax2.axvspan(4, 7, alpha=0.2, color='red')
    ax2.axvspan(9, 10, alpha=0.2, color='crimson')
    ax2.axvspan(11, 13, alpha=0.2, color='crimson')
    ax2.axvspan(14, 17, alpha=0.2, color='silver')
    ax2.axvspan(21, 22, alpha=0.2, color='crimson')
    ax2.axvspan(27, 29, alpha=0.2, color='silver')
    ax2.axvspan(30, 33, alpha=0.2, color='crimson')
    ax2.axvspan(34, 36, alpha=0.2, color='crimson')
    ax2.axvspan(37, 38, alpha=0.2, color='silver')
    ax2.set_ylabel('(%) Stock Allocation')
    ax1.set_xlabel('Period')
    ax2.legend(labels=['Allocation'], loc='upper left')
    return ax1, ax2

# Last Plot


def contrast(dtf, dtOB, x, y, ob, levels, refl, color, c1, c2):
    g = sns.jointplot(data=dtf, x=x, y=y,
                      kind='reg', color=color, marginal_kws=dict(bins=13, fill=False))
    g.plot_joint(sns.kdeplot, color=c1, zorder=0, levels=levels)
    g.set_axis_labels('Average Belief', '(%) Stock Allocation')
    if refl:
        g.refline(x=dtf[x].mean(), y=dtf[y].mean(), color=c2)
        g.refline(x=dtOB[ob].mean(), color='r')
#############################################################################
# # ################ $$$ Exploratory Data Analysis $$$ ######################


#  ########### $$ Objective Return Distribution 20 Cochort$$ ################
dfOb = pd.read_csv('ObjDistribution.csv', header=0)
stOb = calc_sum_stats(dfOb['Objective'])

dfObNC = dfOb[dfOb['Actual Year'] >= 1945]
stObNC = calc_sum_stats(dfObNC['Objective'])

# #  ################ $$ Per Subject 40 Cohort $$ ####################

dtf40, dtf40ST, dtf40LT, stats40 = split('40PerSubjectData.csv',
                                         'Belief', 'Treatment (D)', 0, 1)
print(dtf40ST.Subject.unique())
print(dtf40LT.Subject.unique())
print(dtf40.columns)

PerP40 = dtf40.groupby(['Year']).mean()
PerP40ST = dtf40ST.groupby(['Year']).mean()
PerP40LT = dtf40LT.groupby(['Year']).mean()

# # Get statics for each Period in each Group
#
# P40stats = calc_sum_stats(PerP40['Belief'])
# P40STstats = calc_sum_stats(PerP40ST['Belief'])
# P40LTstats = calc_sum_stats(PerP40LT['Belief'])
#
# GP40stats = pd.concat([P40stats, P40STstats, P40LTstats, stOb], axis=1,
#                       keys=['Overall', 'Control', 'Treatment', 'Objective'])
#
# print(GP40stats.to_latex(index=True))

# Create Marginal Distribution
fig0, axes = plt.subplots(2, sharex=True)
margfig(fig0, PerP40, 'Belief', 0.4, dfObNC, obj=True)


# Create First Figure KDE

fig, axes = plt.subplots(2, 2)
kdefig(fig, PerP40ST, PerP40LT, 'Belief', 'PerAllo', 0.4, dfOb, obj=True)
plt.show()
#
# # Create Belief vs Per Allaction
# fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 4))
# ax1, ax1a = two_scales(ax1, PerP40ST.index, PerP40ST['Belief'],
#                        PerP40ST['PerAllo'], '#1f77b4', 'green')
# ax2, ax2a = two_scales(ax2, PerP40ST.index, PerP40LT['Belief'],
#                        PerP40LT['PerAllo'], '#ff7f0e', 'green')
# fig.suptitle('Control vs Treatment Per Period Comparison')
#
# # Bivariate Plot
# contrast(PerP40ST, dfOb, 'Belief',
#          'PerAllo', 'Objective', 5, True, '#1f77b4', '#d62728', 'Black')
#
# # Bivariate Plot
# contrast(PerP40LT, dfOb, 'Belief',
#          'PerAllo', 'Objective', 5, True, '#ff7f0e', '#d62728', 'Black')
#
# plt.show()

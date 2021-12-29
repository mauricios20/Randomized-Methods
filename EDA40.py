import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
import scipy.stats as stat
# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

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

# Create 2 axis for FaceGrid


def facetgrid_two_axes(*args, **kwargs):
    data = kwargs.pop('data')
    dual_axis = kwargs.pop('dual_axis')
    kwargs.pop('color')
    ax = plt.gca()
    if dual_axis:
        ax2 = ax.twinx()
        ax2.set_ylabel('(%) Stock Allocation')

    ax.plot(data['Year'], data['Belief'], 'o-')
    if dual_axis:
        ax2.plot(data['Year'], data['PerAllo'], 'x--', color='green', mec='black')


# Split Data Frame


def split(fname, col, tname, CG, TG):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0,
                      dtype={'Treatment (D)': int, 'Subject': int, 'Year': int})
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


def kdefig(figu, dtf, x, bw, dtfob, obj):
    # Top of Figure
    Sp = [0.2, 0.3, 0.4, 0.5]  # Smoothing Parameter
    for s in Sp:
        sns.kdeplot(data=dtf, x=x, bw_adjust=s,
                    ax=figu.axes[0]).legend(labels=Sp)

    # Bottom Part of Figure
    sns.kdeplot(data=dtf, x=x, bw_adjust=bw, ax=figu.axes[1])

    # Add Ibjective Distribution
    if obj:
        sns.kdeplot(data=dtfob, x="Objective", bw_adjust=0.3, ax=figu.axes[1],
                    linestyle="--", color="red",
                    legend=True).legend(labels=['Observed', 'Objective'])

# Obtain the KernelDensity for each Treatmet


def kdefigCT(figu, dtf, dtfCG, dtfTG, x, bw, tname, dtfob, obj):
    sns.kdeplot(data=dtfCG, x=x, bw_adjust=bw,
                ax=figu.axes[0], fill=True).set(xlabel=None)
    sns.kdeplot(data=dtfTG, x=x, bw_adjust=bw,
                ax=figu.axes[2], color='darkorange', fill=True)

    if obj:
        sns.kdeplot(data=dtfob, x="Objective", bw_adjust=0.3, ax=figu.axes[0],
                    linestyle="--", color="red",
                    legend=True).legend(labels=['Objective', 'CG'])
        sns.kdeplot(data=dtfob, x="Objective", bw_adjust=0.3, ax=figu.axes[2],
                    linestyle="--", color="red",
                    legend=True).legend(labels=['Objective', 'TG'])

    sns.histplot(data=dtf, x=x, hue=tname, ax=figu.axes[1]).set(xlabel=None)
    sns.kdeplot(data=dtf, x=x, bw_adjust=bw,
                hue=tname, cumulative=True, common_norm=False,
                common_grid=True, ax=figu.axes[3]).set(ylabel=None)


# Obtain Violin and Boxplots


def vioandbox(figu, dtf, tname, y, bw):
    sns.violinplot(data=dtf, x=tname, y=y, ax=figu.axes[0], bw=bw)

    sns.boxplot(data=dtf, x=tname, y=y, ax=figu.axes[1]).set(ylabel=None)


# Joint Plot AveExp with Ave Stock Allocation


def contrast(dtf, dtfCG, dtfTG, dtOB, x, y, ob, tname, levels, reg, refl):
    if reg:
        g = sns.jointplot(data=dtf, x=x, y=y,
                          kind='reg')
        g.plot_joint(sns.kdeplot, zorder=0, levels=levels)
        g.set_axis_labels('Average Belief', '(%) Stock Allocation')
    else:
        g = sns.jointplot(data=dtf, x=x, y=y,
                          hue=tname)
        g.plot_joint(sns.kdeplot, zorder=0, levels=levels)
        g.set_axis_labels('Average Belief', '(%) Stock Allocation')
    if refl:
        g.refline(x=dtfTG[x].mean(), y=dtfTG[y].mean(), color='orange')
        g.refline(x=dtfCG[x].mean(), y=dtfCG[y].mean(), color='blue')
        g.refline(x=dtOB[ob].mean(), color='r')
#############################################################################
# # ################ $$$ Exploratory Data Analysis $$$ ######################


#  ########### $$ Objective Return Distribution 20 Cochort$$ ################
dfOb = pd.read_csv('ObjDistribution.csv', header=0)
stOb = calc_sum_stats(dfOb['Objective'])

# # #  ########### $$ Objective Return Distribution 40 Cochort$$ ################
# 'SP 500 Return Stream from 1925 to 1964'
plt.figure(2)
plt.plot(dfOb['Actual Year'], dfOb['Return'], 'o-')
plt.axvspan(1925, 1926, facecolor='silver', alpha=0.5)
plt.axvspan(1928, 1931, facecolor='crimson', alpha=0.5)
plt.axvspan(1933, 1934, facecolor='crimson', alpha=0.5)
plt.axvspan(1935, 1937, facecolor='crimson', alpha=0.5)
plt.axvspan(1938, 1941, facecolor='silver', alpha=0.5)
plt.axvspan(1945, 1946, facecolor='crimson', alpha=0.5)
plt.axvspan(1951, 1953, facecolor='silver', alpha=0.5)
plt.axvspan(1954, 1957, facecolor='crimson', alpha=0.5)
plt.axvspan(1958, 1960, facecolor='crimson', alpha=0.5)
plt.axvspan(1961, 1962, facecolor='silver', alpha=0.5)
plt.axhline(y=dfOb['Return'].mean(), color='r', label='Average')
plt.text(1929, dfOb['Return'].mean()+0.01, '(Mean = 7.89%)')
plt.xlabel('Period')
plt.ylabel('(%) Return')

(plt.xticks(range(dfOb['Actual Year'].min(),
                  dfOb['Actual Year'].max()+1, 1), rotation=50))

# #  ################ $$ Per Subject 40 Cohort $$ ####################

dtf40, dtf40ST, dtf40LT, stats40 = split('40PerSubjectData.csv',
                                         'Belief', 'Treatment (D)', 0, 1)
print(dtf40ST.Subject.unique())
print(dtf40LT.Subject.unique())

# G40stats = pd.concat([stats40, stOb], axis=1)
# print(G40stats.to_latex(index=True))

# Create First Figure KDE (Marginal Distribution)
fig, axes = plt.subplots(2, sharex=True)

kdefig(fig, dtf40, 'Belief', 0.4, dfOb, obj=True)


# Create Second Figure Group Comparison (Conditional Distribution)
fig1, ax = plt.subplots(2, 2, sharex=True)
for i in range(0, 4):
    fig1.axes[i].grid(True)

kdefigCT(fig1, dtf40, dtf40ST, dtf40LT, 'Belief',
         0.3, 'Treatment (D)', dfOb, obj=True)

# Create Third Visualization
fig2, axes = plt.subplots(1, 2, sharey=True)

vioandbox(fig2, dtf40, 'Treatment (D)', 'Belief', 0.2)
plt.show()
#
# # Create Bivariate Plot
# contrast(dtf40, dtf40ST, dtf40LT, dfOb, 'Belief', 'PerAllo', 'Objective',
#          'Treatment (D)', 5, reg=False, refl=True)
# contrast(dtf40, dtf40ST, dtf40LT, dfOb, 'Belief', 'PerAllo', 'Objective',
#          'Treatment (D)', 5, reg=True, refl=False)
#
# # Per Subject in Control Group
# min = dtf40ST['Belief'].min()-0.1
# max = dtf40ST['Belief'].max()+0.1
#
# z = sns.FacetGrid(dtf40ST, col='Subject', col_wrap=5,
#                   height=3, ylim=(min, max), aspect=1.4)
# (z.map_dataframe(facetgrid_two_axes, dual_axis=True)
#     .set_axis_labels("Period", "Belief"))
# z.map(plt.fill_betweenx, y=[-1, 1], x1=1, x2=2, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=4, x2=7, alpha=0.5, color='red')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=9, x2=10, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=11, x2=13, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=14, x2=17, alpha=0.5, color='silver')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=21, x2=22, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=27, x2=29, alpha=0.5, color='silver')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=30, x2=33, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=34, x2=36, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=37, x2=38, alpha=0.5, color='silver')
#
# # Per Subject in Treatmet Group
# min = dtf40LT['Belief'].min()-0.1
# max = dtf40LT['Belief'].max()+0.1
#
# z = sns.FacetGrid(dtf40LT, col='Subject', col_wrap=5,
#                   height=3, ylim=(min, max), aspect=1.4)
# (z.map_dataframe(facetgrid_two_axes, dual_axis=True)
#     .set_axis_labels("Period", "Belief"))
# z.map(plt.fill_betweenx, y=[-1, 1], x1=1, x2=2, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=4, x2=7, alpha=0.5, color='red')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=9, x2=10, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=11, x2=13, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=14, x2=17, alpha=0.5, color='silver')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=21, x2=22, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=27, x2=29, alpha=0.5, color='silver')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=30, x2=33, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=34, x2=36, alpha=0.5, color='crimson')
# z.map(plt.fill_betweenx, y=[-1, 1], x1=37, x2=38, alpha=0.5, color='silver')
# plt.show()

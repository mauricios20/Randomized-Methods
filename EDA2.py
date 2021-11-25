import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pylab
import statsmodels.api as sm
from scipy.stats import kstest, norm
from scipy import stats
import numpy as np
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
#######################################################################
# # Exploratory Data Analysis


#  ########### $$ Objective Return Distribution 20 Cochort$$ ################
dfOb = pd.read_csv('ObjDistribution.csv', header=0)
dfObNC = dfOb[dfOb['Actual Year'] >= 1945]

print(dfObNC['Return'].mean())

plt.figure(1)
plt.plot(dfObNC['Actual Year'], dfObNC['Return'], 'o-')
plt.axvspan(1945, 1946, facecolor='crimson', alpha=0.5)
plt.axvspan(1951, 1953, facecolor='silver', alpha=0.5)
plt.axvspan(1954, 1957, facecolor='crimson', alpha=0.5)
plt.axvspan(1958, 1960, facecolor='crimson', alpha=0.5)
plt.axvspan(1961, 1962, facecolor='silver', alpha=0.5)
plt.axhline(y=dfObNC['Return'].mean(), color='r', label='Average')
plt.text(1946, dfObNC['Return'].mean()+0.01, '(Mean = 10.15%)')
plt.xlabel('Period')
plt.ylabel('(%) Return')
plt.title('SP 500 Return Stream from 1945 to 1964')
(plt.xticks(range(dfObNC['Actual Year'].min(),
                  dfObNC['Actual Year'].max()+1, 1), rotation=45))


#  ########### $$ Objective Return Distribution 40 Cochort$$ ################
print(dfOb['Return'].mean())

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
plt.title('SP 500 Return Stream from 1925 to 1964')
(plt.xticks(range(dfOb['Actual Year'].min(),
                  dfOb['Actual Year'].max()+1, 1), rotation=50))


#  ################ $$ Per Subject 20 Cohort $$ ####################
dtf = pd.read_csv('Test.csv', header=0)
print(dtf.Subject.unique())
print(dtf.columns)

z = sns.FacetGrid(dtf, col='Subject', col_wrap=3, height=4, ylim=(-0.3, 1))
(z.map_dataframe(facetgrid_two_axes, dual_axis=True)
    .set_axis_labels("Period", "Belief"))
z.map(plt.fill_betweenx, y=[-1, 1], x1=1, x2=2, alpha=0.5, color='crimson')
z.map(plt.fill_betweenx, y=[-1, 1], x1=7, x2=9, alpha=0.5, color='silver')
z.map(plt.fill_betweenx, y=[-1, 1], x1=10, x2=13, alpha=0.5, color='crimson')
z.map(plt.fill_betweenx, y=[-1, 1], x1=14, x2=16, alpha=0.5, color='crimson')
z.map(plt.fill_betweenx, y=[-1, 1], x1=17, x2=18, alpha=0.5, color='silver')
plt.show()

import os
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

# Description


def comparison(*args, **kwargs):
    data = kwargs.pop('data')
    kwargs.pop('color')
    ax = plt.gca()
    ax.plot(data['Year'], data['Belief'], 'o-')
    ax.plot(data['Year'], data['PerAllo'], 'x--', color='orange', mec='black')


# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)


path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)

# Load the Data
dtf = pd.read_csv('40PerSubjectData.csv', header=0,
                  dtype={'Subject': int, 'Year': int},
                  usecols=['Subject', 'During/Post', 'Year', 'Belief', 'PerAllo'])

# #  ################ $$ During Crash vs. Post Crash $$ ####################
# Per Subject
Subjects = dtf.Subject.unique()
# Create a data frame dictionary to store your data frames

DataFrameDict = {elem: pd.DataFrame for elem in Subjects}
PercentChange = {elem: pd.DataFrame for elem in Subjects}
for key in DataFrameDict.keys():
    DataFrameDict[key] = dtf[dtf['Subject'] == key]
    PercentChange[key] = DataFrameDict[key].set_index(
        ['Subject', 'Year']).pct_change(fill_method='ffill')


# Scatter Plot Belief vs Allocation
Group1 = Subjects[:10]
# Group
Group2 = Subjects[10:20]
# Group2
Group3 = Subjects[20:30]
# Group3
Group4 = Subjects[30:]

dtG1 = dtf.loc[dtf.Subject.isin(Group1)]
dtG2 = dtf.loc[dtf.Subject.isin(Group2)]
dtG3 = dtf.loc[dtf.Subject.isin(Group3)]
dtG4 = dtf.loc[dtf.Subject.isin(Group4)]

# Group 1
k = sns.FacetGrid(dtG1, col="Subject", col_wrap=5, height=3, aspect=1.4)
k.map_dataframe(sns.scatterplot, x='PerAllo', y='Belief', hue='During/Post').set_axis_labels(
    "(%) Allocation", "Belief")

# Group 2
k = sns.FacetGrid(dtG2, col="Subject", col_wrap=5, height=3, aspect=1.4)
k.map_dataframe(sns.scatterplot, x='PerAllo', y='Belief', hue='During/Post').set_axis_labels(
    "(%) Allocation", "Belief")

# Group 3
k = sns.FacetGrid(dtG3, col="Subject", col_wrap=5, height=3, aspect=1.4)
k.map_dataframe(sns.scatterplot, x='PerAllo', y='Belief', hue='During/Post').set_axis_labels(
    "(%) Allocation", "Belief")

# Group 4
k = sns.FacetGrid(dtG4, col="Subject", col_wrap=5,
                  height=3, aspect=1.4)
k.map_dataframe(sns.scatterplot, x='PerAllo', y='Belief', hue='During/Post').set_axis_labels(
    "(%) Allocation", "Belief")


# Split Individuals for PercentChange Visualization
OverallData = pd.concat(PercentChange).reset_index()

dtG1 = OverallData.loc[OverallData.Subject.isin(Group1)]
dtG2 = OverallData.loc[OverallData.Subject.isin(Group2)]
dtG3 = OverallData.loc[OverallData.Subject.isin(Group3)]
dtG4 = OverallData.loc[OverallData.Subject.isin(Group4)]

# Group 1
g = sns.FacetGrid(dtG1, col="Subject", col_wrap=5, height=3, aspect=1.4)
(g.map_dataframe(comparison).set_axis_labels("Period", "(%) Change"))
g.map(plt.axhline, y=2, color='r', linestyle='-')
g.map(plt.axhline, y=-2, color='r', linestyle='-')

# Group 2
g = sns.FacetGrid(dtG2, col="Subject", col_wrap=5, height=3, aspect=1.4)
g.map_dataframe(comparison).set_axis_labels("Period", "(%) Change")
g.map(plt.axhline, y=2, color='r', linestyle='-')
g.map(plt.axhline, y=-2, color='r', linestyle='-')

# Group 3
g = sns.FacetGrid(dtG3, col="Subject", col_wrap=5, height=3, aspect=1.4)
g.map_dataframe(comparison).set_axis_labels("Period", "(%) Change")
g.map(plt.axhline, y=2, color='r', linestyle='-')
g.map(plt.axhline, y=-2, color='r', linestyle='-')

# Group 4
g = sns.FacetGrid(dtG4, col="Subject", col_wrap=5, height=3, aspect=1.4)
g.map_dataframe(comparison).set_axis_labels("Period", "(%) Change")
g.map(plt.axhline, y=2, color='r', linestyle='-')
g.map(plt.axhline, y=-2, color='r', linestyle='-')


# KernelDensity Visualizations per Subject Excluding Outliers
exclude = [118, 104, 41, 43, 60, 47, 50, 58, 52, 113, 117]
kerneldtf = dtf.loc[~dtf.Subject.isin(exclude)]
Subjects2 = kerneldtf.Subject.unique()

Group1 = Subjects2[:9]
Group1
Group2 = Subjects2[9:18]
Group2
Group3 = Subjects2[18:]
Group3


dtG1 = kerneldtf.loc[kerneldtf.Subject.isin(Group1)]
dtG2 = kerneldtf.loc[kerneldtf.Subject.isin(Group2)]
dtG3 = kerneldtf.loc[kerneldtf.Subject.isin(Group3)]


z = sns.FacetGrid(dtG1, col="Subject", col_wrap=3, height=3, aspect=1.4)
z.map_dataframe(sns.kdeplot, x='Belief', bw_adjust=0.7,
                hue='During/Post', fill=True)


z = sns.FacetGrid(dtG2, col="Subject", col_wrap=3, height=3, aspect=1.4)
z.map_dataframe(sns.kdeplot, x='Belief', bw_adjust=0.7,
                hue='During/Post', fill=True)


z = sns.FacetGrid(dtG3, col="Subject", col_wrap=3, height=3, aspect=1.4)
z.map_dataframe(sns.kdeplot, x='Belief', bw_adjust=0.7,
                hue='During/Post', fill=True)

plt.show()

# Just to see what color is During and Post
# sns.scatterplot(x='PerAllo', y='Belief', hue='During/Post', data=DataFrameDict[56])
# sns.kdeplot(x='PerAllo', y='Belief', hue='During/Post', fill=True, data=DataFrameDict[56])
# sns.kdeplot(x='PerAllo', hue='During/Post', fill=True, data=DataFrameDict[56])
# sns.regplot(x='PerAllo', y='Belief', data=DataFrameDict[112])
# plt.show()

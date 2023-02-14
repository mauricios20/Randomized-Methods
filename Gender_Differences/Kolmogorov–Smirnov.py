import os
import pandas as pd
import stata_setup
stata_setup.config('/Applications/Stata', 'be')
from pystata import stata
from sfi import Scalar, Matrix

path = '/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/Data'
os.chdir(path)


def split(fname, sex):
    # Get Data Frame
    dtf = pd.read_csv(fname, header=0,
                      dtype={'Treatment (D)': int, 'Subject': int, 'Year': int})
    # st = calc_sum_stats(dtf[col])

    dtfMale = dtf[dtf[sex] == 'Male']

    dtfFemale = dtf[dtf[sex] == 'Female']

    return dtf, dtfMale, dtfFemale


# Get data and split it
dtf40, dtf40Male, dtf40Female = split('40PerSubjectData.csv', 'Sex')
dtf20, dt20Male, dt20Female = split('20PerSubjectData.csv', 'Sex')

# Fruther split
dtf40DC = dtf40[dtf40['Condition'] == 'DC']
dtf40PC = dtf40[dtf40['Condition'] == 'PC']

# Further Split Data
dtf40FemaleDC = dtf40Female[dtf40Female['Condition'] == 'DC']
dtf40FemalePC = dtf40Female[dtf40Female['Condition'] == 'PC']

dtf40MaleDC = dtf40Male[dtf40Male['Condition'] == 'DC']
dtf40MalePC = dtf40Male[dtf40Male['Condition'] == 'PC']

dtf40_Group = dtf40.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
dtf40DC_Group = dtf40DC.groupby(
    ['Blocks', 'Subject', 'Sex']).mean().reset_index()
dtf40PC_Group = dtf40PC.groupby(
    ['Blocks', 'Subject', 'Sex']).mean().reset_index()

# ~~~~~~~~~~ Kolmogorov–Smirnov test By Sex ~~~~~~~~~~~~~~~~~~~~
# Overall
stata.pdataframe_to_data(dtf40_Group, force=True)
stata.run('ksmirnov Belief, by(Sex)')

# During Crash
stata.pdataframe_to_data(dtf40DC, force=True)
stata.run('ksmirnov Belief, by(Sex)')

# Post Crash
stata.pdataframe_to_data(dtf40PC, force=True)
stata.run('ksmirnov Belief, by(Sex)')

# By Blocks
blocks = dtf40_Group.Blocks.unique()
BlockDict = {elem: pd.DataFrame for elem in blocks}

for key in BlockDict.keys():
    BlockDict[key] = dtf40_Group[dtf40_Group['Blocks'] == key]

for i in range(1, 11):
    dtf = BlockDict[i].append(BlockDict[i], ignore_index=True)
    stata.pdataframe_to_data(dtf, force=True)
    stata.run('ksmirnov Belief, by(Sex) exact')

# ~~~~~~~~~~ Kolmogorov–Smirnov test By Blocks ~~~~~~~~~~~~~~~~~~~~


for key in BlockDict.keys():
    BlockDict[key] = dtf40_Group[dtf40_Group['Blocks'] == key]

for i in range(2, 11):
    dtf = BlockDict[1].append(BlockDict[i], ignore_index=True)
    stata.pdataframe_to_data(dtf, force=True)
    stata.run('ksmirnov Belief, by(Blocks)')

# By Blocks Per Gender - Female
for key in BlockDict.keys():
    BlockDict[key] = dtf40Female[dtf40Female['Blocks'] == key]

for i in range(2, 11):
    dtf = BlockDict[1].append(BlockDict[i], ignore_index=True)
    stata.pdataframe_to_data(dtf, force=True)
    stata.run('ksmirnov Belief, by(Blocks)')

# By Blocks Per Gender - Male
for key in BlockDict.keys():
    BlockDict[key] = dtf40Male[dtf40Male['Blocks'] == key]

for i in range(2, 11):
    dtf = BlockDict[1].append(BlockDict[i], ignore_index=True)
    stata.pdataframe_to_data(dtf, force=True)
    stata.run('ksmirnov Belief, by(Blocks) exact')

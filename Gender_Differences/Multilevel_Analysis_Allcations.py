import os
import pandas as pd
import stata_setup
stata_setup.config('/Applications/Stata', 'be')
from sfi import Scalar, Matrix
from pystata import stata

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

#Fruther split
dtf40DC = dtf40[dtf40['Condition'] == 'DC']
dtf40PC = dtf40[dtf40['Condition'] == 'PC']

# Further Split Data
dtf40FemaleDC = dtf40Female[dtf40Female['Condition'] == 'DC']
dtf40FemalePC = dtf40Female[dtf40Female['Condition'] == 'PC']

dtf40MaleDC = dtf40Male[dtf40Male['Condition'] == 'DC']
dtf40MalePC = dtf40Male[dtf40Male['Condition'] == 'PC']

dtf40_Group = dtf40.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
dtf40DC_Group = dtf40DC.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
dtf40PC_Group = dtf40PC.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Overall Allocations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# No Distinction between gender
stata.pdataframe_to_data(dtf40_Group, force=True)
stata.run('mixed PerAllo i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot, noci')
stata.run('contrast r.Blocks, cieffects')

stata.run('encode Sex, generate(gender)')
stata.run('mixed PerAllo i.gender##i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks#gender, nopvalue')
stata.run('marginsplot, noci')
stata.run('contrast Blocks#gender')
stata.run('contrast r.Blocks#gender, cieffects')

stata.run('correlate Belief PerAllo')
stata.run('scatter Belief PerAllo')

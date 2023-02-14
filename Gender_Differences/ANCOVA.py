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

# Further Split Data
dtf40_Group = dtf40.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
# dtf40DC_Group = dtf40DC.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
# dtf40PC_Group = dtf40PC.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()

dtf40_Group = dtf40_Group[['Blocks', 'Subject', 'Sex', 'Belief']]

stata.pdataframe_to_data(dtf40_Group, force=True)
stata.run('reshape wide Belief, i(Subject) j(Blocks)')
stata.run('list in 1/5')
stata.run('encode Sex, generate(gender)')
stata.run('list in 1/5')
stata.run('anova Belief7 i.gender c.Belief6')
stata.run('contrast gender')

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
# dtf40_Group = dtf40.groupby(['Blocks']).mean().reset_index()
# print(dtf40_Group.Belief)

dtf40_Group = dtf40.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
dtf40DC_Group = dtf40DC.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
dtf40PC_Group = dtf40PC.groupby(['Blocks', 'Subject', 'Sex']).mean().reset_index()
# ~~~~~~~~~~~~~~~~~~~~~~~~~ Overall Beliefs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dtf40_Group.to_stata('GroupCrash.dta')

# No Distinction between gender
stata.run('clear')
stata.pdataframe_to_data(dtf40_Group, force=True)
stata.run('cd "/Users/mau/Dropbox/Mac/Documents/Dissertation/Safford2018/StataData"')
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
# stata.run('putdocx begin')
# stata.run('putdocx table reg=etable, title("Linear Regression of Belief")')
stata.run('margins Blocks, nopvalue')
# stata.run('putdocx table margins=etable, title("Margins Belief")')
stata.run('marginsplot, noci')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')
# stata.run('putdocx table contrast=etable, title("Contrasts of marginal linear predictions")')
# stata.run('putdocx save GeneralBelief, replace')

# Difference Between Females and Males Overall
stata.run('encode Sex, generate(gender)')
stata.run('mixed Belief i.gender##i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
# stata.run('putdocx begin')
# stata.run('putdocx table reg2=etable, title("Linear Regression of Belief#Gender")')
stata.run('margins Blocks#gender, nopvalue')
# stata.run('putdocx table margins2=etable, title("Liner Predicitions Margins Belief")')
stata.run('marginsplot, noci')
stata.run('contrast Blocks#gender')
# stata.run('putdocx table contrast12=etable, title("Contrasts of marginal linear predictions")')
stata.run('contrast r.Blocks#gender, cieffects')
# stata.run('putdocx table contrast2=etable, title("Contrasts of marginal linear predictions")')
# stata.run('putdocx save ByGenderBelief, replace')

stata.run('correlate Belief PerAllo')
# Difference Between Females and Males Overall During Crash
stata.pdataframe_to_data(dtf40DC_Group, force=True)
stata.run('encode Sex, generate(gender)')
stata.run('mixed Belief i.gender##i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks#gender, nopvalue')
stata.run('marginsplot, noci')
stata.run('contrast Blocks#gender')
stata.run('contrast r.Blocks#gender, cieffects')

# Difference Between Females and Males Overall Post Crash
stata.pdataframe_to_data(dtf40PC_Group, force=True)
stata.run('encode Sex, generate(gender)')
stata.run('mixed Belief i.gender##i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks#gender, nopvalue')
stata.run('marginsplot, noci')
stata.run('contrast Blocks#gender')
stata.run('contrast r.Blocks#gender, cieffects')

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Female Group ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dtFemale_Group = dtf40Female.groupby(['Blocks', 'Subject']).mean().reset_index()
dtf40FemaleDC_Group = dtf40FemaleDC.groupby(['Blocks', 'Subject']).mean().reset_index()
dtf40FemalePC_Group = dtf40FemalePC.groupby(['Blocks', 'Subject']).mean().reset_index()

# Mixed Analysis for overall Female Group
stata.pdataframe_to_data(dtFemale_Group, force=True)
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')

# Mixed Analysis for DC Female Groups
stata.pdataframe_to_data(dtf40FemaleDC_Group, force=True)
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')

# Mixed Analysis for PC Female Groups
stata.pdataframe_to_data(dtf40FemalePC_Group, force=True)
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Male Group ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dtfMale_Group = dtf40Male.groupby(['Blocks', 'Subject']).mean().reset_index()
dtf40MaleDC_Group = dtf40MaleDC.groupby(['Blocks', 'Subject']).mean().reset_index()
dtf40MalePC_Group = dtf40MalePC.groupby(['Blocks', 'Subject']).mean().reset_index()

# Mixed Analysis for overall Male Group
stata.pdataframe_to_data(dtfMale_Group, force=True)
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')

# Mixed Analysis for DC Male Groups
stata.pdataframe_to_data(dtf40MaleDC_Group, force=True)
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')

# Mixed Analysis for PC Male Groups
stata.pdataframe_to_data(dtf40MalePC_Group, force=True)
stata.run('mixed Belief i.Blocks || Subject:, nocons residuals(un, t(Blocks)) nolog')
stata.run('margins Blocks, nopvalue')
stata.run('marginsplot')
stata.run('contrast Blocks')
stata.run('contrast r.Blocks, cieffects')

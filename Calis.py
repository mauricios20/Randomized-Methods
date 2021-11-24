import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Description
# Analysis for Group in the 20 year cathegory
# Treatmet (D): Treatement Description (0 ST, 1 LT)

os.chdir("C:/Users/mauri/Dropbox/Family Room/1 Hi Lo Exp Data/Randomization Methods/Data")
df20 = pd.read_csv('20PeriodGroup.csv', header=0)

# # Overral Data Analysis for 20 Cohort
print(df20.shape)
print(df20.head(5))
st20 = df20[['InvExp', 'AveExp']].describe()
df20ST = df20[[df20['Treatment (D)'] == 0]]
df20LT = df20[[df20['Treatment (D)'] == 1]]
print(df20ST.describe())
print(df20LT.describe())
# Create Figures
fig1, axes = plt.subplots(2, sharex=True, sharey=True)
fig1.suptitle('20 Cohort - Kernel Density Estimation')

Sp = [0.2, 0.3, 0.4, 0.5]  # Smoothing Parameter
for s in Sp:
    sns.kdeplot(data=df20, x="AveExp", bw_adjust=s, ax=axes[0]).legend(labels=Sp)

axes[0].set_title('Smoothing Parameters')
# From the Fig 1, 0.3 will be the smooting Parameter, use it for following
# usage
sns.kdeplot(data=df20, x="AveExp", bw_adjust=0.2, ax=axes[1], cut=0)
axes[1].set_title('0.2 Smoothing without Extremes')
plt.close()

# #Obtain the KernelDensity for each Treatmet
fig2, ax = plt.subplots(2, sharex=True)
fig2.suptitle('20 Cohort - Treatmet Comparison')
sns.kdeplot(data=df20, x="AveExp", bw_adjust=0.2, cut=0, hue='Treatment (D)',
            ax=fig2.axes[0])
fig2.axes[0].set_title('Kernel Density Estimation')

sns.kdeplot(data=df20, x="AveExp", bw_adjust=0.2, cut=0, hue='Treatment (D)',
            cumulative=True, common_norm=False, common_grid=True, ax=fig2.axes[1])
fig2.axes[1].set_title('Cumulative Distribution Functions')
plt.close()

####################################################################
# # Overral Data Analysis for 40 Cohort
df40 = pd.read_csv('40PeriodGroup.csv', header=0)
print(df40.shape)
print(df40.head(5))
st40 = df40[['InvExp', 'AveExp']].describe()

fig3, axes = plt.subplots(2, sharex=True, sharey=True)
fig3.suptitle('40 Cohort - Kernel Density Estimation')

Sp = [0.2, 0.3, 0.4, 0.5]  # Smoothing Parameter
for s in Sp:
    sns.kdeplot(data=df40, x="AveExp", bw_adjust=s, ax=fig3.axes[0]).legend(labels=Sp)

axes[0].set_title('Smoothing Parameters')

# From the Fig 1, 0.3 will be the smooting Parameter, use it for following
# usage
sns.kdeplot(data=df40, x="AveExp", bw_adjust=0.2, ax=fig3.axes[1], cut=0)
axes[1].set_title('0.2 Smoothing without Extremes')
plt.close()

# #Obtain the KernelDensity for each Treatmet
fig4, ax = plt.subplots(2, sharex=True)
fig4.suptitle('40 Cohort - Treatmet Comparison')
sns.kdeplot(data=df40, x="AveExp", bw_adjust=0.2, hue='Treatment (D)',
            ax=fig4.axes[0])
fig4.axes[0].set_title('Kernel Density Estimation')

# Cumulative Distribution
sns.kdeplot(data=df40, x="AveExp", bw_adjust=0.2, hue='Treatment (D)',
            cumulative=True, common_norm=False, common_grid=True, ax=fig4.axes[1])
fig4.axes[1].set_title('Cumulative Distribution Functions')
plt.close()

#########################################################################
# # Lets compare the Distribution against the Objective One
dfOb = pd.read_csv('ObjDistribution.csv', header=0)
print(dfOb.shape)
print(dfOb.head(5))
stOb = dfOb.Rdecimal.describe()

dfObNC = dfOb[dfOb['Actual Year'] >= 1945]
print(dfObNC.shape)
print(dfObNC.head(5))
stObNC = dfObNC.Rdecimal.describe()


fig5, ax = plt.subplots(2,  sharex=True)
sns.kdeplot(data=dfOb, x="Rdecimal", bw_adjust=0.2, ax=fig5.axes[0],
            linestyle="--", color="r", legend=True)

fig5.axes[0].set_title('Objective Kernel Distribution')

# Cumulative Distribution
sns.kdeplot(data=dfOb, x="Rdecimal", bw_adjust=0.2,
            cumulative=True, common_norm=False, common_grid=True, ax=fig5.axes[1])
fig5.axes[1].set_title('Cumulative Distribution Functions')
plt.show()

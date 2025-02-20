#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
import sklearn
import seaborn as sns
#%%
df = pd.read_csv('HeightWeight.csv')
df.drop(columns='Index', inplace=True)
df.rename(columns={'Height(Inches)': 'Height (inch)', 'Weight(in pounds)': 'Weight (pound)'}, inplace=True)

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Height (inch)', y='Weight (pound)', data=df)
plt.title('Height vs Weight')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Height (inch)'])
plt.title('Height Distribution')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Weight (pound)'])
plt.title('Weight Distribution')
plt.show()
# %%

quant25 = df.quantile(0.25)
quant75 = df.quantile(0.75)
iqr = quant75 - quant25
lower_bound = quant25 - 1.5 * iqr
upper_bound = quant75 + 1.5 * iqr
num_datapoints = len(df)
df_clean = df[(df['Height (inch)'] >= lower_bound['Height (inch)']) & (df['Height (inch)'] <= upper_bound['Height (inch)']) & (df['Weight (pound)'] >= lower_bound['Weight (pound)']) & (df['Weight (pound)'] <= upper_bound['Weight (pound)'])]
num_datapoints_clean = len(df_clean)
print(f"Number of data points before cleaning: {num_datapoints}")
print(f"Number of data points after cleaning: {num_datapoints_clean}")
print(f"Number of data points removed: {num_datapoints - num_datapoints_clean}")
print(f"Percentage of data points removed: {100 * (num_datapoints - num_datapoints_clean) / num_datapoints}%")


plt.figure(figsize=(10, 6))
sns.scatterplot(x='Height (inch)', y='Weight (pound)', data=df)
plt.title('Height vs Weight')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Height (inch)'])
plt.title('Height Distribution')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Weight (pound)'])
plt.title('Weight Distribution')
plt.show()
# %%

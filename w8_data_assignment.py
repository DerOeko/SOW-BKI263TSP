#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
# %%
df = pd.read_csv('DataSet.csv')
df.drop(columns=["Index"], inplace=True)
before_removing_na = len(df)
print(f"# of df entries before removing NA: {len(df)}")
df.dropna(inplace=True)
print(f"# of df entries after removing NA: {len(df)}")
print(f"# of df entries removed: {before_removing_na - len(df)}")
print(f"% of df entries removed: {(before_removing_na - len(df)) / before_removing_na * 100:.2f}%")
df.rename(columns={'Height(Inches)': 'Height (inch)', 'Weight(in pounds)': 'Weight (pound)', 'Gender(0 - female)': 'Gender (0 - ♀)'}, inplace=True)


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
print(f"Percentage of data points removed: {100 * (num_datapoints - num_datapoints_clean) / num_datapoints:.2f}%")

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

df_clean.info()
# Height (inch): numerical datatype
# Weight (pound): numerical datatype
# Gender (0 - ♀): categorical datatype
# %%
# Can we predict gender from weight and height?
X, y = df_clean[['Height (inch)', 'Weight (pound)']], df_clean['Gender (0 - ♀)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression())])

pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print(f"Final accuracy on test set: {accuracy:.2f}")

# not really, as the accuracy is 52% on the test set.

# %%
# Can we predict weight from height and gender?
X, y = df_clean[['Height (inch)', 'Gender (0 - ♀)']], df_clean['Weight (pound)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([('scaler', StandardScaler()), ('reg', LinearRegression())])

pipe.fit(X_train, y_train)
y_pred_reg = pipe.predict(X_test)

mse = metrics.mean_squared_error(y_test, y_pred_reg)
sse = mse * len(y_test)
print(f"Mean Squared Error: {mse:.2f}")
print(f"Sum of Squared Errors: {sse:.2f}")

# mean squared error seems pretty high. can we predict weight solely from height?
#%%
# Plotting the regression line for predicting weight from height (for Gender 0)

# Filter data for gender == 0 (female)
df_female = df_clean[df_clean['Gender (0 - ♀)'] == 0]

# Sort by height for a smooth line plot
df_female_sorted = df_female.sort_values('Height (inch)')

X_female = df_female_sorted[['Height (inch)', 'Gender (0 - ♀)']]
y_female = df_female_sorted['Weight (pound)']
y_pred_line = pipe.predict(X_female)

plt.figure(figsize=(10, 6))
plt.scatter(df_female_sorted['Height (inch)'], y_female, color='blue', label='Actual Weight')
plt.plot(df_female_sorted['Height (inch)'], y_pred_line, color='red', label='Regression Line')
plt.xlabel('Height (inch)')
plt.ylabel('Weight (pound)')
plt.title('Regression Line for Weight vs Height (Gender=Female)')
plt.legend()
plt.show()

# Filter data for gender == 0 (female)
df_male = df_clean[df_clean['Gender (0 - ♀)'] == 1]

# Sort by height for a smooth line plot
df_male_sorted = df_male.sort_values('Height (inch)')

X_male = df_male_sorted[['Height (inch)', 'Gender (0 - ♀)']]
y_male = df_male_sorted['Weight (pound)']
y_pred_line = pipe.predict(X_male)

plt.figure(figsize=(10, 6))
plt.scatter(df_male_sorted['Height (inch)'], y_male, color='blue', label='Actual Weight')
plt.plot(df_male_sorted['Height (inch)'], y_pred_line, color='red', label='Regression Line')
plt.xlabel('Height (inch)')
plt.ylabel('Weight (pound)')
plt.title('Regression Line for Weight vs Height (Gender=Male)')
plt.legend()
plt.show()
# %%

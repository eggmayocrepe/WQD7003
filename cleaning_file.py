import pandas as pd
from functions_clean_data import safe_float, find_continents, replace_none
# import the data here from the main dataset
FAOSTAT = pd.read_csv("FAOSTAT_data_2025.csv")
# convert the values of the Value feature while
# taking into consideration interval data(took the min)
FAOSTAT['Value'] = FAOSTAT['Value'].apply(
    lambda x: safe_float(x) if not isinstance(
        x, (float, int)
        ) else x)
# drop irrelevalant columns or redundant columns
df = FAOSTAT.drop(['Domain Code', 'Domain', 'Element Code',
                   'Element', 'Item Code',
                   'Year Code', 'Note', 'Flag'], axis=1)
# convert Values to float once again, to be safe
df['Value'] = df['Value'].apply(lambda x: float(x))
# create a new column that we call continenet
# that categorize the country and
# on which continent it is located
df['continents'] = df['Area'].apply(lambda x: find_continents(x))
# Some units are in None and they represent index
# create a new unit called index to categorize it
df['Unit'] = df['Unit'].apply(replace_none)
# group the data by year,Item'continents and area
# this will be used to imputate our missing values
df_1 = df.groupby(['Year', 'Item', 'continents', 'Area']).agg({
    "Flag Description": "first",
    'Unit': 'first',
    'Value': 'mean'
})
# Create empty list or dict to store results
# this list will store dataframes
results = []
df_1.reset_index(inplace=True)
# Loop over each unique item with missing 'Value'
# btw, there are 29 Items
for i in df_1.loc[df_1['Value'].isna(), 'Item'].unique():
    filtered = df_1[df_1['Item'] == i]
    grouped = filtered.groupby(['Year', 'continents']).agg({
        'Flag Description': 'first',
        'Unit': 'first',
        'Value': 'mean',
        'Item': 'first'
    }).reset_index()
    results.append(grouped)
# Combine all group results if needed:
# this will concatinate the dataframes row wise
means_value_item_one_year = pd.concat(results, ignore_index=True)
# create a new dataframe that will merge out two datasets
# it will merge based on 'Year', 'Item' and 'continents'
# data will be saved in a new column called Value_patch
df_test = df_1.merge(
    means_value_item_one_year[['Year', 'Item', 'continents', 'Value']],
    on=['Year', 'Item', 'continents'],
    how='left',
    suffixes=('', '_patch')
)
# copy elements of Value_patch into the missing data values
df_test['Value'] = df_test['Value'].fillna(df_test['Value_patch'])
# drop the Value patch
df_test.drop('Value_patch', axis=1, inplace=True)
# repeat the previous step with data based on country across the years
# Create empty list or dict to store results
results = []
# Loop over each unique item with missing 'Value'
for i in df_1.loc[df_1['Value'].isna(), 'Item'].unique():
    filtered = df_1[df_1['Item'] == i]
    grouped = filtered.groupby(['Year', 'Area']).agg({
        'Flag Description': 'first',
        'Unit': 'first',
        'Value': 'mean',
        'Item': 'first'
    }).reset_index()
    results.append(grouped)
# Combine all group results if needed:
means_value_item_one_year = pd.concat(results, ignore_index=True)
df_test = df_test.merge(
    means_value_item_one_year[['Year', 'Item', 'Value', 'Area']],
    on=['Year', 'Item', 'Area'],
    how='left',
    suffixes=('', '_patch')
)
df_test['Value'] = df_test['Value'].fillna(df_test['Value_patch'])
df_test.drop('Value_patch', axis=1, inplace=True)
# save the data into a csv file
df_test.to_csv('FAOSTAT_data_2025_clean.csv')

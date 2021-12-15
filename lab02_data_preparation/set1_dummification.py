# Dummy encode the symbolic variables. The selection of symbolic variables is hardcoded 
# since selecting does not work. 

# Change columns to dummify here:
symbolic_vars = ['BODILY_INJURY', 'SAFETY_EQUIPMENT', 'PERSON_TYPE', 'POSITION_IN_VEHICLE']

from pandas import read_csv
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
#file = 'set1_NYC_collisions_tabular'
file = 'set1_mv'
#filename = 'lab02_data_preparation\data\new_data\set1_mv.csv'
#filename = 'lab01_data_profiling\data\set1_NYC_collisions_tabular.csv'
filename = 'lab02_data_preparation\ew_data\set1_mv.csv'

data = read_csv(filename, index_col='CRASH_TIME', na_values='', parse_dates=True, infer_datetime_format=True)

print(data.head())
# Drop out all records with missing values
# This leaves no records at all. First drop columns with lot of empty cells. 
# data = data.drop(['PED_LOCATION', 'CONTRIBUTING_FACTOR_2', 'CONTRIBUTING_FACTOR_1', 'PED_ACTION'], axis=1)
data = data.drop(['PERSON_ID', 'UNIQUE_ID', 'VEHICLE_ID', 'PED_ROLE'], axis=1)

# Columns to do: 'PERSON_SEX','EJECTION', PED_ROLE

# drop U columns
data = data[data.PERSON_SEX != 'U']

person_sex_status_encode = { # personsex
    'F':1,
    'M': 0
}
data["PERSON_SEX"].replace(person_sex_status_encode, inplace=True)

ejection_status_encode = { # ejection
    'Ejected':1,
    'Not Ejected': 0, 
    'Partially Ejected' : 0.5
}
data["EJECTION"].replace(ejection_status_encode, inplace=True)

data.dropna(inplace=True)

from pandas import DataFrame, concat
from ds_charts import get_variable_types
from sklearn.preprocessing import OneHotEncoder
from numpy import number

def dummify(df, vars_to_dummify):
    other_vars = [c for c in df.columns if not c in vars_to_dummify]
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False, dtype=bool)
    X = df[vars_to_dummify]
    encoder.fit(X)
    new_vars = encoder.get_feature_names(vars_to_dummify)
    trans_X = encoder.transform(X)
    dummy = DataFrame(trans_X, columns=new_vars, index=X.index)
    dummy = dummy.convert_dtypes(convert_boolean=True)

    final_df = concat([df[other_vars], dummy], axis=1)
    return final_df

variables = get_variable_types(data)
#symbolic_vars = variables['Symbolic']

print(data.info())

#symbolic_vars = ['BODILY_INJURY', 'SAFETY_EQUIPMENT', 'PERSON_SEX', 'PERSON_TYPE', 'EJECTION', 'COMPLAINT', 'EMOTIONAL_STATUS', 'POSITION_IN_VEHICLE', 'PED_ROLE', 'PERSON_INJURY']


print(symbolic_vars)
df = dummify(data, symbolic_vars)
df.to_csv(f'lab02_data_preparation\ew_data\{file}_dummified.csv', index=False)

df.describe(include=[bool])
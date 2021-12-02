from pandas import read_csv
from pandas.plotting import register_matplotlib_converters
from matplotlib.pyplot import subplots, savefig, show
from ds_charts import get_variable_types, HEIGHT
from matplotlib.pyplot import figure, savefig, show, title
from seaborn import heatmap

register_matplotlib_converters()
filename = "lab01_data_profiling/data/set2_air_quality_tabular.csv"
data = read_csv(filename, index_col='date', parse_dates=True, infer_datetime_format=True)

corr_mtx = data.corr()
print(corr_mtx)

fig = figure(figsize=[15, 15])

heatmap(abs(corr_mtx), xticklabels=corr_mtx.columns, yticklabels=corr_mtx.columns, annot=True, cmap='Blues', fmt='.2f')
title('Correlation analysis Set 2')
savefig(f'lab01_data_profiling/images/correlation_analysis_set2.png')
show()
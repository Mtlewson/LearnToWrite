import pandas as pd
import numpy
filename = 'bw_imageTinyExcel.xls'
df = pd.read_excel(filename, index_col=0)
array = df.to_numpy()
print(type(array))
print(array[0])

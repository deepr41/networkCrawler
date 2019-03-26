import pandas as pd
data = pd.read_csv('finale.csv', error_bad_lines = False)
df = data.sort_values('slno')
df2 = df.drop_duplicates(subset = 'slno', keep = False)
df2.to_csv('finale1.csv',index = False)
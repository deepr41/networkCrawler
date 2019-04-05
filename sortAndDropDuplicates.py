import pandas as pd
data = pd.read_csv('finale.csv', error_bad_lines = False)
data = data.sort_values('slno')
data = data.drop_duplicates(subset = 'slno', keep = False)
data.to_csv('finaleClean.csv',index = False)

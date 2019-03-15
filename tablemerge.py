import numpy as np
import pandas as  pd
import sys

def main(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    print(df1.head())
    print(df2.head())
    
    df3 = pd.merge(df2,df1,on='slno',how='inner')
    # df4 = df3['slno','websiteName','hostname','alias','ipaddress']

    df3.to_csv('dataMerged.csv',index=False)
    

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    else:
        file1 = './data.csv'
        file2 = './top-1m-websites.csv'
    main(file1,file2)

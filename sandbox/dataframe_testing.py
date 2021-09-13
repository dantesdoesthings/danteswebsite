import numpy as np
import pandas as pd


def main():
    df1 = pd.DataFrame()
    print(df1)
    time_vals = np.arange(1628610738, 1628611738)
    data_vals = np.ones(1000)
    s1 = pd.Series(data_vals, time_vals)
    df1['S1'] = s1
    print(df1)
    dv2 = np.random.uniform(10, 20, 1000)
    s2 = pd.Series(dv2, time_vals)
    df1['S2'] = s2
    df1.to_csv('df1.csv', index_label='timestamp')
    print(df1)
    tv2 = np.arange(1628611738, 1628611838)
    s3 = pd.Series(np.ones(100)*2, tv2)
    df2 = pd.DataFrame({'S1': s3, 'S2': pd.Series(np.array(np.random.poisson(10, 100), dtype=float), tv2)})
    print(df2)
    df3 = df1.merge(df2, 'outer')
    print(df3)
    df4 = pd.DataFrame({'S1': data_vals, 'S2': dv2}, time_vals)
    print(df4)


if __name__ == '__main__':
    main()

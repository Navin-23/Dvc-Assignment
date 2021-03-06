## read params
## process
### return dataframe
import os
import yaml
import pandas as pd
import argparse
import numpy as np

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_data(config_path):
    config = read_params(config_path)
    data_path = config["data_source"]["s3_source"]
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    def remove_outliers(data):
        arr=[]
        #print(max(list(data)))
        q1=np.percentile(data,25)
        q3=np.percentile(data,75)
        iqr=q3-q1
        mi=q1-(1.5*iqr)
        ma=q3+(1.5*iqr)
        #print(mi,ma)
        for i in list(data):
            if i<mi:
                i=mi
                arr.append(i)
            elif i>ma:
                i=ma
                arr.append(i)
            else:
                arr.append(i)
        #print(max(arr))
        return arr
    df['bmi'] = remove_outliers(df['bmi'])
    df['complication_rsi'] = remove_outliers(df['complication_rsi'])
    df['Age'] = remove_outliers(df['Age'])
    df['hour'] = remove_outliers(df['hour'])
    df['ahrq_ccs'] = remove_outliers(df['ahrq_ccs'])
    df['mortality_rsi'] = remove_outliers(df['mortality_rsi'])
    df['ccsComplicationRate'] = remove_outliers(df['ccsComplicationRate'])
    df['ccsMort30Rate'] = remove_outliers(df['ccsMort30Rate'])
    return df

###

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = get_data(config_path = parsed_args.config)
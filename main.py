import os
import csv
import numpy as np
import pandas as pd
from sklearn.metrics import (mean_absolute_percentage_error as mape)
data_header = ['target','evja_temp','timestamp_normalizzato']
DIR_ESITI = 'esiti'
DIR_DATI = 'dati'
CSV_BASE_NAME='Dataset_sens_'
data_header_index = 'timestamp_normalizzato'
CSV_EXTENSION = '.csv'

def __createMultiDimArray(dataframe,data_header,data_header_index):
    index = data_header.index(data_header_index)
    data = dataframe[data_header].values
    for i in range(len(data)):
        data[i][index] = data[i][index][len(data[i][index]) - 1]
    data = np.asarray(data).astype(np.float32)

    return data

def compare(sensore):
    filename = DIR_DATI + os.path.sep + CSV_BASE_NAME + str(sensore) + CSV_EXTENSION
    df = pd.read_csv(filename)
    data = __createMultiDimArray(df,data_header,data_header_index)
    target = []
    evja = []
    for i in range(len(data)):
        val_target = data[i,0]
        val_evia = data[i, 1]
        target.append(val_target)
        evja.append(val_evia)
    sklearn_metrics_mape = mape(target,evja)
    return sklearn_metrics_mape

def writeToCsvFile(to_csv):
    outFile = DIR_ESITI + os.path.sep + 'esitiCfrEvja' + CSV_EXTENSION
    keys = to_csv[0].keys()
    with open(outFile, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('iniziato')
    to_csv = []

    for sensore in range(1,8):
        out = {}
        sklearn_metrics_mape = compare(sensore)
        print('sklearn.metrics.mape ',str(sensore), sklearn_metrics_mape)
        out['sensore'] = sensore
        out['mape_vs_evja'] = sklearn_metrics_mape
        to_csv.append(out)
        writeToCsvFile(to_csv)
    writeToCsvFile(to_csv)
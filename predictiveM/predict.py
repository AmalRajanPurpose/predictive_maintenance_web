# -*- coding: utf-8 -*-
"""Untitled52.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Tl55xOwXGJc7x1FdSmptxt-GjSCnRtc
"""

import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import MinMaxScaler  # to normalize data

import tensorflow as tf

min_max_scaler = MinMaxScaler(feature_range=(-1, 1))


def gen_test(id_df, seq_length, seq_cols, mask_value):
    """
        function to prepare test data into (samples, time steps, features)
        function only returns last sequence of data for every unit
        id_df = test dataframe
        seq_length = look back period
        seq_cols = feature columns
    """
    df_mask = pd.DataFrame(np.zeros((seq_length - 1, id_df.shape[1])), columns=id_df.columns)
    df_mask[:] = mask_value

    id_df = df_mask.append(id_df, ignore_index=True)

    data_array = id_df[seq_cols].values
    num_elements = data_array.shape[0]
    lstm_array = []

    start = num_elements - seq_length
    stop = num_elements

    lstm_array.append(data_array[start:stop, :])

    return np.array(lstm_array)


def predict_on_test(csv_path):
    rul = []
    df_test = pd.read_csv(csv_path, sep=" ", header=None)
    df_test.columns = ["unit_number", "cycle", "os_1", "os_2", 'os_3', "s_1", "s_2", "s_3", "s_4", "s_5", "s_6", "s_7",
                       "s_8", "s_9", "s_10", "s_11", "s_12", "s_13", "s_14", "s_15", "s_16", "s_17", "s_18", "s_19",
                       "s_20", "s_21", "s_22", "s_23"]
    cols_to_drop = ['os_3', 's_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19', 's_22', 's_23']
    df_test = df_test.drop(cols_to_drop, axis=1)
    feats = ['unit_number', 'os_1', 'os_2', 's_2', 's_3', 's_4', 's_7', 's_8', 's_9', 's_11', 's_12', 's_13', 's_14',
             's_15', 's_17', 's_20', 's_21']
    df_test[feats] = min_max_scaler.fit_transform(df_test[feats])
    sequence_length = 50
    mask_value = 0
    x_test = np.concatenate(list(
        list(gen_test(df_test[df_test['unit_number'] == unit], sequence_length, feats, mask_value)) for unit in
        df_test['unit_number'].unique()))
    model_l = tf.keras.models.load_model('../pred_maintenance_final.h5')
    y_pred = model_l.predict(x_test)
    for pred in y_pred:
        rul.append(np.round(pred)[0])

    return rul

#
# rul = predict_on_test('test_FD001.txt')
# print(rul)
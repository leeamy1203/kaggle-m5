import os
import logging

import pandas as pd
import numpy as np

from src.data import DATA_DIR

logger = logging.getLogger(__name__)


def clean() -> None:
    calendar = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'calendar.csv'))
    sales = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'sell_prices.csv'))
    train = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'sales_train_validation.csv'))
    
    calendar_mb = calendar.memory_usage(deep=True).sum() / 1e6
    logger.info(f"Memory size of calendar.csv before down casting is = {calendar_mb:<5.2f}MB")
    sales_mb = sales.memory_usage(deep=True).sum() / 1e6
    logger.info(f"Memory size of sell_prices.csv before down casting is = {sales_mb:<5.2f}MB")
    train_mb = train.memory_usage(deep=True).sum() / 1e6
    logger.info(f"Memory size of sales_train_validation.csv before down casting is = {train_mb:<5.2f}MB")
    
    calendar_downcasted = downcast(calendar)
    calendar_mb = calendar_downcasted.memory_usage(deep=True).sum() / 1e6
    logger.info(f"Memory size of calendar.csv after down casting is = {calendar_mb:<5.2f}MB")
    calendar_downcasted.to_pickle(os.path.join(DATA_DIR, 'interim', 'calendar.pkl'))

    sales_downcasted = downcast(sales)
    sales_mb = sales_downcasted.memory_usage(deep=True).sum() / 1e6
    logger.info(f"Memory size of sell_prices.csv after down casting is = {sales_mb:<5.2f}MB")
    sales_downcasted.to_pickle(os.path.join(DATA_DIR, 'interim', 'sell_prices.pkl'))

    train_downcasted = downcast(train)
    train_mb = train_downcasted.memory_usage(deep=True).sum() / 1e6
    logger.info(f"Memory size of sales_train_validation.csv after down casting is = {train_mb:<5.2f}MB")
    train_downcasted.to_pickle(os.path.join(DATA_DIR, 'interim', 'sales_train_validation.pkl'))

    # melt train data
    per_day = pd.melt(train_downcasted,
                      id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'], var_name='d',
                      value_name='sold').dropna()
    per_day.d = per_day.d.astype('category')
    logger.info("Reformatted training data to be per day")

    training_calendar = pd.merge(per_day, calendar_downcasted, on=["d"])
    merged_df = pd.merge(training_calendar, sales_downcasted, on=["wm_yr_wk", 'item_id'])
    
    merged_df.to_pickle(os.path.join(DATA_DIR, 'interim', 'trainable.pkl'))
   
    
def downcast(df: pd.DataFrame) -> pd.DataFrame:
    """
    Downcast the dataframe to reduce the amount of storage. This should improve upon operation time,
    Obtained from: https://www.kaggle.com/anshuls235/m5-forecasting-extensive-eda see Downcasting
    """
    cols = df.dtypes.index.tolist()
    types = df.dtypes.values.tolist()
    for i, t in enumerate(types):
        if 'int' in str(t):
            if df[cols[i]].min() > np.iinfo(np.int8).min and df[cols[i]].max() < np.iinfo(np.int8).max:
                df[cols[i]] = df[cols[i]].astype(np.int8)
            elif df[cols[i]].min() > np.iinfo(np.int16).min and df[cols[i]].max() < np.iinfo(np.int16).max:
                df[cols[i]] = df[cols[i]].astype(np.int16)
            elif df[cols[i]].min() > np.iinfo(np.int32).min and df[cols[i]].max() < np.iinfo(np.int32).max:
                df[cols[i]] = df[cols[i]].astype(np.int32)
            else:
                df[cols[i]] = df[cols[i]].astype(np.int64)
        elif 'float' in str(t):
            if df[cols[i]].min() > np.finfo(np.float16).min and df[cols[i]].max() < np.finfo(np.float16).max:
                df[cols[i]] = df[cols[i]].astype(np.float16)
            elif df[cols[i]].min() > np.finfo(np.float32).min and df[cols[i]].max() < np.finfo(np.float32).max:
                df[cols[i]] = df[cols[i]].astype(np.float32)
            else:
                df[cols[i]] = df[cols[i]].astype(np.float64)
        elif t == np.object:
            if cols[i] == 'date':
                df[cols[i]] = pd.to_datetime(df[cols[i]], format='%Y-%m-%d')
            else:
                df[cols[i]] = df[cols[i]].astype('category')
    return df


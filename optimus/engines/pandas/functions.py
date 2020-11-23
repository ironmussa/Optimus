# DataFrame = pd.DataFrame
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from optimus.engines.base.commons.functions import to_string, to_integer, to_float
from optimus.engines.base.functions import Functions
from optimus.helpers.core import val_to_list


class PandasFunctions(Functions):
    def __init__(self, df):
        super(PandasFunctions, self).__init__(df)

    def _to_float(self, value):
        return value.map(to_float)

    def to_float(self, series):
        return to_float(series)

    def _to_integer(self, value):
        return value.map(to_integer)

    def to_integer(self, series):
        return to_integer(series)

    def count_zeros(self, series, *args):
        return int((series.to_float().values == 0).sum())

    def kurtosis(self, series):
        return series.kurtosis(series.to_float())

    def skew(self, series):
        return series.skew(series.to_float())

    def exp(self, series):
        return np.exp(series.to_float())

    def sqrt(self, series):
        return np.sqrt(series.to_float())

    def radians(self, series):
        return np.radians(series.to_float())

    def degrees(self, series):
        return np.degrees(series.to_float())

    def ln(self, series):
        return np.log(series.to_float())

    def log(self, series):
        return np.log10(series.to_float())

    def ceil(self, series):
        return np.ceil(series.to_float())

    def sin(self, series):
        return np.sin(series.to_float())

    def cos(self, series):
        return np.cos(series.to_float())

    def tan(self, series):
        return np.tan(series.to_float())

    def asin(self, series):
        return np.arcsin(series.to_float())

    def acos(self, series):
        return np.arccos(series.to_float())

    def atan(self, series):
        return np.arctan(series.to_float())

    def sinh(self, series):
        return np.arcsinh(series.to_float())

    def cosh(self, series):
        return np.cosh(series.to_float())

    def tanh(self, series):
        return np.tanh(series.to_float())

    def asinh(self, series):
        return np.arcsinh(series.to_float())

    def acosh(self, series):
        return np.arccosh(series.to_float())

    def atanh(self, series):
        return np.arctanh(series.to_float())

    def clip(self, series, lower_bound, upper_bound):
        return series.clip(lower_bound, upper_bound)

    def cut(self, series, bins):
        return series.to_float(series).cut(bins, include_lowest=True, labels=list(range(bins)))

    def replace_chars(self, series, search, replace_by):
        # if ignore_case is True:
        #     # Cudf do not accept re.compile as argument for replace
        #     # regex = re.compile(str_regex, re.IGNORECASE)
        #     regex = str_regex
        # else:
        #     regex = str_regex
        replace_by = val_to_list(replace_by)
        for i, j in zip(search, replace_by):
            series = series.astype(str).str.replace(i, j)
        return series

    def remove_special_chars(self, series):
        return series.astype(str).str.replace('[^A-Za-z0-9]+', '')

    def remove_accents(self, series):
        return series.str.normalize("NFKD").str.encode('ascii', errors='ignore').str.decode('utf8')

    def date_format(self, series, current_format=None, output_format=None):
        return pd.to_datetime(series, format=current_format, errors="coerce").dt.strftime(output_format)

    def years_between(self, series, date_format=None):
        return (pd.to_datetime(series, format=date_format,
                               errors="coerce").dt.date - datetime.now().date()) / timedelta(days=365)

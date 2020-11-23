# DataFrame = pd.DataFrame
import re
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from optimus.engines.base.functions import Functions
from optimus.helpers.core import val_to_list, one_list_to_val


class IbisFunctions(Functions):
    def __init__(self, df):
        super(IbisFunctions, self).__init__(df)

    def lower(self, series, *args):
        return series.cast("string").lower()

    def upper(self, series, *args):
        return series.cast("string").upper()

    #
    # def replace(self, series, *args):
    #     return series.cast("string").upper()

    def replace_chars(self, series, search, replace_by):
        # print("search, replace_by", search, replace_by)
        search = one_list_to_val(search)
        replace_by = one_list_to_val(replace_by)
        return series.cast("string").replace(search, replace_by)

    def replace_words(self, series, search, replace_by):
        search = val_to_list(search)
        str_regex = (r'\b%s\b' % r'\b|\b'.join(map(re.escape, search)))
        return series.cast("string").replace(str_regex, replace_by)

    def replace_full(self, series, search, replace_by):
        search = val_to_list(search)
        str_regex = (r'\b%s\b' % r'\b|\b'.join(map(re.escape, search)))
        return series.cast("string").replace(str_regex, replace_by)

    def count_zeros(self, *args):
        series = self.series
        return int((series.to_float().values == 0).sum())

    def kurtosis(self):
        series = self.series
        return series.kurtosis(series.to_float())

    def skew(self):
        series = self.series
        return series.skew(series.to_float())

    def exp(self):
        series = self.series
        return np.exp(series.to_float())

    def sqrt(self):
        series = self.series
        return np.sqrt(series.to_float())

    def radians(self):
        series = self.series
        return np.radians(series.to_float())

    def degrees(self):
        series = self.series
        return np.degrees(series.to_float())

    def ln(self):
        series = self.series
        return np.log(series.to_float())

    def log(self):
        series = self.series
        return np.log10(series.to_float())

    def ceil(self):
        series = self.series
        return np.ceil(series.to_float())

    def sin(self):
        series = self.series
        return np.sin(series.to_float())

    def cos(self):
        series = self.series
        return np.cos(series.to_float())

    def tan(self):
        series = self.series
        return np.tan(series.to_float())

    def asin(self):
        series = self.series
        return np.arcsin(series.to_float())

    def acos(self):
        series = self.series
        return np.arccos(series.to_float())

    def atan(self):
        series = self.series
        return np.arctan(series.to_float())

    def sinh(self):
        series = self.series
        return np.arcsinh(series.to_float())

    def cosh(self):
        series = self.series
        return np.cosh(series.to_float())

    def tanh(self):
        series = self.series
        return np.tanh(series.to_float())

    def asinh(self):
        series = self.series
        return np.arcsinh(series.to_float())

    def acosh(self):
        series = self.series
        return np.arccosh(series.to_float())

    def atanh(self):
        series = self.series
        return np.arctanh(series.to_float())

    def clip(self, lower_bound, upper_bound):
        series = self.series
        return series.clip(lower_bound, upper_bound)

    def cut(self, bins):
        series = self.series
        return series.to_float(series).cut(bins, include_lowest=True, labels=list(range(bins)))

    def replace_chars(self, search, replace_by):
        series = self.series
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

    def remove_special_chars(self):
        series = self.series
        return series.astype(str).str.replace('[^A-Za-z0-9]+', '')

    def remove_accents(self):
        series = self.series
        return series.str.normalize("NFKD").str.encode('ascii', errors='ignore').str.decode('utf8')

    def date_format(self, current_format=None, output_format=None):
        series = self.series
        return pd.to_datetime(series, format=current_format, errors="coerce").dt.strftime(output_format)

    def years_between(self, date_format=None):
        series = self.series
        return (pd.to_datetime(series, format=date_format,
                               errors="coerce").dt.date - datetime.now().date()) / timedelta(days=365)

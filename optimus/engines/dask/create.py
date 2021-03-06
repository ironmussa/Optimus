import pandas as pd

from optimus.engines.dask.dataframe import DaskDataFrame
from optimus.helpers.check import is_pandas_dataframe
from optimus.helpers.converter import pandas_to_dask_dataframe
from optimus.infer import is_dict


class Create:
    def __init__(self, root):
        self.root = root

    def dataframe(self, data, cols=None, rows=None, pdf=None, n_partitions=1, *args, **kwargs):
        """
        Helper to create dataframe:
        :param cols: List of Tuple with name, data type and a flag to accept null
        :param rows: List of Tuples with the same number and types that cols
        :param pdf: a pandas dataframe
        :param n_partitions:
        :return: Dataframe
        """

        if is_dict(data):
            data = pd.DataFrame(data)
        # elif is_pandas_dataframe(data):
        data = pandas_to_dask_dataframe(data, n_partitions)
        df = DaskDataFrame(data)
        return df

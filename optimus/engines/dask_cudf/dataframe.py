from optimus.engines.base.dask.dataframe import DaskBaseDataFrame
from optimus.engines.cudf.dataframe import CUDFDataFrame
from optimus.engines.dask_cudf.io.save import Save
from optimus.engines.pandas.dataframe import PandasDataFrame
from optimus.helpers.columns import parse_columns
from optimus.helpers.converter import cudf_to_dask_cudf


class DaskCUDFDataFrame(DaskBaseDataFrame):

    def __init__(self, data):
        super().__init__(self, data)

    def _base_to_dfd(self, pdf, n_partitions):
        return cudf_to_dask_cudf(pdf, n_partitions)

    @property
    def rows(self):
        from optimus.engines.dask_cudf.rows import Rows
        return Rows(self)

    @property
    def cols(self):
        from optimus.engines.dask_cudf.columns import Cols
        return Cols(self)

    @property
    def functions(self):
        from optimus.engines.dask_cudf.functions import DaskCUDFFunctions
        return DaskCUDFFunctions()

    @property
    def save(self):
        return Save(self)

    @property
    def mask(self):
        from optimus.engines.dask_cudf.mask import DaskCUDFMask
        return DaskCUDFMask(self)

    @property
    def constants(self):
        from optimus.engines.base.dask.constants import constants
        return constants(self)

    def _buffer_window(self, input_cols, lower_bound, upper_bound):
        return PandasDataFrame(self.get_buffer().data[input_cols][lower_bound: upper_bound].to_pandas())


    @staticmethod
    def pivot(index, column, values):
        pass

    @staticmethod
    def melt(id_vars, value_vars, var_name="variable", value_name="value", data_type="str"):
        pass

    @staticmethod
    def query(sql_expression):
        pass

    @staticmethod
    def debug():
        pass

    @staticmethod
    def create_id(column="id"):
        pass

    def to_pandas(self):
        return self.data.compute().to_pandas()

    def to_optimus_pandas(self):
        return PandasDataFrame(self.root.to_pandas())

    def to_optimus_cudf(self):
        return CUDFDataFrame(self.root.to_pandas())

    def to_dict(self, orient="records", limit=None):
        """
        Create a dict
        :param orient:
        :param limit:
        :return:
        """
        series = self.root
        return series.compute().to_pandas().to_dict(orient)

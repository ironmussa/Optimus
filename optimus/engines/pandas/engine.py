import pandas as pd

from optimus.engines.base.engine import BaseEngine
from optimus.engines.pandas.create import Create
from optimus.engines.pandas.io.extract import Extract
from optimus.engines.pandas.io.load import Load
from optimus.engines.pandas.pandas import Pandas
from optimus.helpers.exceptions import UnsupportedOperationError
from optimus.version import __version__

Pandas.instance = None


class PandasEngine(BaseEngine):
    __version__ = __version__

    def __init__(self, verbose=False, *args, **kwargs):
        self.extract = Extract()

        self.verbose(verbose)

        Pandas.instance = pd

        self.client = pd

    @property
    def create(self):
        return Create(self)

    @property
    def load(self):
        return Load(self)

    @property
    def engine(self):
        return "pandas"

    def remote_run(self, callback, *args, **kwargs):
        if kwargs.get("client_timeout"):
            del kwargs["client_timeout"]

        callback(op=self, *args, **kwargs)

    def remote_submit(self, callback, *args, **kwargs):
        return self.submit(callback, op=self, *args, **kwargs)

    def submit(self, func, *args, **kwargs):
        import uuid
        def _func():
            return func(*args, **kwargs)

        return {"result": _func, "key": str(uuid.uuid4()), "status": "finished"}

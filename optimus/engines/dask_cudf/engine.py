import dask
from dask.distributed import Client, get_client

from optimus.engines.base.engine import BaseEngine
from optimus.engines.base.remote import ClientActor, RemoteDummyVariable, RemoteDummyDataFrame
from optimus.engines.dask_cudf.io.load import Load
from optimus.helpers.logger import logger
from optimus.optimus import Engine

BIG_NUMBER = 100000


class DaskCUDFEngine(BaseEngine):
    def __init__(self, session=None, address=None, n_workers=1, threads_per_worker=8, processes=False,
                 memory_limit='4GB', verbose=False, coiled_token=None, *args, **kwargs):

        """

        :param session:
        :param n_workers:
        :param threads_per_worker:
        :param memory_limit:
        :param verbose:
        :param comm:
        :param args:
        :param kwargs:
        """

        self.engine = Engine.DASK_CUDF.value

        self.verbose(verbose)

        use_remote = kwargs.get("use_remote", coiled_token is not None)

        if coiled_token:
            import coiled
            dask.config.set({"coiled.token": coiled_token})
            try:
                coiled.Cloud()
            except Exception as error:
                raise error

            idle_timeout = kwargs.get("idle_timeout", None)

            cluster = coiled.Cluster(
                name=kwargs.get("name"),
                worker_options={
                    **({"nthreads": threads_per_worker} if threads_per_worker else {}),
                    **({"memory_limit": memory_limit} if memory_limit else {})
                },
                worker_gpu=1,
                worker_class='dask_cuda.CUDAWorker',
                n_workers=n_workers,
                worker_memory='15GiB',
                backend_options={
                    "region": kwargs.get("backend_region", "us-east-1")
                },
                scheduler_options={
                    **({"idle_timeout": idle_timeout} if idle_timeout else {})
                },
                software="optimus/gpu"
            )

            self.cluster_name = cluster.name
            self.client = Client(cluster)

        elif address:
            self.client = Client(address=address)

        elif session and session != "local":
            self.client = session

        else:
            try:
                self.client = get_client()
            except ValueError:
                from dask_cuda import LocalCUDACluster
                from GPUtil import GPUtil
                n_gpus = len(GPUtil.getAvailable(order='first', limit=BIG_NUMBER))

                if n_workers > n_gpus:
                    logger.print(
                        f"n_workers should be equal or less than the number of GPUs. n_workers is now {n_gpus}")
                    n_workers = n_gpus
                    # n_gpus = 1

                cluster = LocalCUDACluster(rmm_pool_size=GPUtil.memoryTotal,
                                           device_memory_limit=GPUtil.memoryTotal * 0.8
                                           # Spill to RAM when 80% memory is full
                                           )
                self.client = Client(cluster, *args, **kwargs)
            use_remote = False

        if use_remote:
            self.remote = self.client.submit(ClientActor, Engine.DASK_CUDF.value, actor=True).result(10)

        else:
            self.remote = False

    @property
    def create(self):
        if self.remote:
            return RemoteDummyVariable(self, "_create")

        else:
            from optimus.engines.dask_cudf.create import Create
            return Create(self)

    @property
    def load(self):
        if self.remote:
            return RemoteDummyVariable(self, "_load")

        else:
            return Load(self)

    def dataframe(self, cdf, n_partitions=1, *args, **kwargs):
        import dask_cudf
        from optimus.engines.dask_cudf.dataframe import DaskCUDFDataFrame
        return DaskCUDFDataFrame(dask_cudf.from_cudf(cdf, npartitions=n_partitions, *args, **kwargs))

    def remote_run(self, callback, *args, **kwargs):
        if kwargs.get("client_timeout"):
            client_timeout = kwargs.get("client_timeout")
            del kwargs["client_timeout"]
        else:
            client_timeout = 600

        return self.remote_submit(callback, *args, **kwargs).result(client_timeout)

    def remote_submit(self, callback, *args, **kwargs):

        if not self.remote:
            fut = self.submit(callback, op=self, *args, **kwargs)
        else:
            fut = self.remote.submit(callback, *args, **kwargs)

        fut.__result = fut.result
        _op = self

        def _result(self, *args, **kwargs):
            result = self.__result(*args, **kwargs)
            if isinstance(result, dict):
                if result.get("status") == "error" and result.get("error"):
                    raise Exception(result.get("error"))
                elif result.get("dummy"):
                    if result.get("dataframe"):
                        return RemoteDummyDataFrame(_op, result.get("dummy"))
                    else:
                        return RemoteDummyVariable(_op, result.get("dummy"))
            return result

        import types
        fut.result = types.MethodType(_result, fut)

        return fut

    def submit(self, func, *args, **kwargs):
        from optimus.engines.base.remote import RemoteDummyAttribute
        if isinstance(func, (RemoteDummyAttribute,)):
            return func(client_submit=True, *args, **kwargs)
        return dask.distributed.get_client().submit(func, *args, **kwargs)

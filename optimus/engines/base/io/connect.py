import re

from optimus.engines.base.dask.io.jdbc import DaskBaseJDBC
from optimus.engines.spark.io.properties import DriverProperties
from optimus.helpers.constants import Schemas
from optimus.helpers.raiseit import RaiseIt
from optimus.infer import regex_full_url


class Connection:
    """
    Generic
    """

    def __init__(self, config=None, **kwargs):
        if not kwargs["base_url"].endswith("/"):
            kwargs["base_url"] = kwargs["base_url"] + "/"
        self._storage_options = kwargs
        self.options = config if config else kwargs

    def path(self, path):
        if self._storage_options["base_url"] and not path.startswith(
                (self._storage_options["base_url"], *Schemas.list())):
            path = self._storage_options["base_url"] + path

        return path

    @property
    def storage_options(self):
        storage_options = self._storage_options.copy()
        storage_options.pop("base_url")

        if not len(storage_options.keys()):
            storage_options = None
        else:
            storage_options = {k: storage_options[k] for k in storage_options.keys() if not k.startswith("_")}

        return storage_options

    def boto(self):
        return self.options


class S3(Connection):
    """
    Amazon S3
    """

    type = "s3"

    def __init__(self, endpoint_url=None, bucket=None, **kwargs):
        """
        endpoint_url: http(s)://<...>
        bucket
        anon: Whether access should be anonymous (default False)
        key, secret: For user authentication
        token: If authentication has been done with some other S3 client
        use_ssl: Whether connections are encrypted and secure (default True)
        client_kwargs: Dict passed to the boto3 client, with keys such as region_name or endpoint_url.
            Notice: do not pass the config option here, please pass it’s content to config_kwargs instead.
        config_kwargs: Dict passed to the s3fs.S3FileSystem, which passes it to the boto3 client’s config option.
        requester_pays: Set True if the authenticated user will assume transfer costs,
            which is required by some providers of bulk data
        default_block_size, default_fill_cache: These are not of particular interest to Dask users,
            as they concern the behaviour of the buffer between successive reads
        kwargs: Other parameters are passed to the boto3 Session object, such as profile_name,
            to pick one of the authentication sections from the configuration files referred to above (see here)


        """
        config = kwargs.copy()
        config["endpoint_url"] = endpoint_url
        config["bucket"] = bucket

        if endpoint_url is None:
            RaiseIt.value_error(endpoint_url, "")

        schema_result = re.search(regex_full_url, endpoint_url)

        if schema_result is not None:
            schema = schema_result[2]
            endpoint_url = endpoint_url[len(schema + "://"):]  # removes schema from endpoint_url

        schema = schema if schema else "https"

        kwargs["client_kwargs"] = kwargs.get("client_kwargs", {})
        kwargs["client_kwargs"]["endpoint_url"] = kwargs["client_kwargs"].get("endpoint_url",
                                                                              schema + "://" + endpoint_url)

        if not kwargs.get("base_url", False):
            if bucket:
                kwargs["base_url"] = Schemas.S3.value + bucket
            elif endpoint_url:
                kwargs["base_url"] = Schemas.S3.value + endpoint_url

        super().__init__(config, **kwargs)

    @property
    def boto(self):
        return {
            # "region_name": S3_REGION,
            "endpoint_url": self.options['endpoint_url'],
            "aws_access_key_id": self.options.get("key"),
            "aws_secret_access_key": self.options.get("secret")}


class Local(Connection):
    """
    Local file system
    """

    def __init__(self, **kwargs):
        """
        supports base_url
        :param kwargs:
        """
        super().__init__(**kwargs)


class MAS(Connection):
    """
    Microsoft Azure Storage
    """

    def __init__(self, **kwargs):
        """
        Authentication for adl requires tenant_id, client_id and client_secret in the storage_options dictionary.
        Authentication for abfs requires account_name and account_key in storage_options.
        :param kwargs:
        """
        super().__init__(**kwargs)


class GCS(Connection):
    def __init__(self, host, port, user, kerb_ticket):
        config["host"] = host
        config["port"] = port
        config["user"] = user
        config["kerb_ticket"] = kerb_ticket
        super().__init__(config, host, port, user, kerb_ticket)


class HDFS(Connection):
    def __init__(self, **kwargs):

        config = kwargs.copy()

        if not kwargs.get("url", False):
            kwargs["url"] = "hdfs://" + kwargs["user"]

            if kwargs.get("password", False):
                kwargs["url"] += ":" + kwargs["password"]

            kwargs["url"] += "@" + kwargs["host"]

            if kwargs.get("port", False):
                kwargs["url"] += ":" + kwargs["port"]

        elif not kwargs["url"].startswith("hdfs://"):
            kwargs["url"] = "hdfs://" + kwargs["url"]

        kwargs["base_url"] = kwargs["url"]
        kwargs.pop("url")

        super().__init__(config, **kwargs)


class Connect:
    @staticmethod
    def mysql(host=None, database=None, user=None, password=None, port=None, schema="public"):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.MYSQL.value["name"],
                            schema=schema)

    @staticmethod
    def postgres(host=None, database=None, user=None, password=None, port=None, schema="public"):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.POSTGRESQL.value["name"],
                            schema=schema)

    @staticmethod
    def mssql(host=None, database=None, user=None, password=None, port=None, schema="public"):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.MSSQL.value["name"],
                            schema=schema)

    @staticmethod
    def redshift(host=None, database=None, user=None, password=None, port=None, schema="public"):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.REDSHIFT.value["name"],
                            schema=schema)

    @staticmethod
    def sqlite(host=None, database=None, user=None, password=None, port=None, schema="public"):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.SQLITE.value["name"],
                            schema=schema)

    @staticmethod
    def bigquery(host=None, database=None, user=None, password=None, port=None, schema="public", project=None,
                 dataset=None):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.BIGQUERY.value["name"],
                            schema=schema, bigquery_project=project, bigquery_dataset=dataset)

    @staticmethod
    def presto(host=None, database=None, user=None, password=None, port=None, schema="public", catalog=None):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.PRESTO.value["name"],
                            schema=schema, presto_catalog=catalog, )

    @staticmethod
    def cassandra(host=None, database=None, user=None, password=None, port=None, schema="public", keyspace=None,
                  table=None):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.CASSANDRA.value["name"],
                            schema=schema, cassandra_keyspace=keyspace,
                            cassandra_table=table)

    @staticmethod
    def redis(host=None, database=None, user=None, password=None, port=None, schema="public"):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.REDIS.value["name"],
                            schema=schema)

    @staticmethod
    def oracle(host=None, database=None, user=None, password=None, port=None, schema="public",
               tns=None, service_name=None, sid=None):
        return DaskBaseJDBC(host, database, user, password, port=port, driver=DriverProperties.ORACLE.value["name"],
                            schema=schema, oracle_tns=tns, oracle_service_name=service_name, oracle_sid=sid)

    @staticmethod
    def s3(**kwargs):
        return S3(**kwargs)

    @staticmethod
    def local(**kwargs):
        return Local(**kwargs)

    @staticmethod
    def hdfs(**kwargs):
        return HDFS(**kwargs)

    @staticmethod
    def gcs(**kwargs):
        """
        Google Cloud Storage
        :param kwargs:
        :return:
        """
        return GCS(**kwargs)

    @staticmethod
    def mas(**kwargs):
        """
        Microsoft Azure Storage
        :param kwargs:
        :return:
        """
        return MAS(**kwargs)

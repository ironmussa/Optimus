from enum import Enum

from optimus.helpers.logger import logger


# Python to PySpark reference
#
# type(None): NullType,
# bool: BooleanType,
# int: LongType,
# float: DoubleType,
# str: StringType,
# bytearray: BinaryType,
# decimal.Decimal: DecimalType,
# datetime.date: DateType,
# datetime.datetime: TimestampType,
# datetime.time: TimestampType,
# Profiler


class Actions(Enum):
    """
    Actions that modify a columns/rows.
    """
    # COLUMNS
    PROFILER_DTYPE = "profiler_dtype"
    MATCH = "match"
    LOWER = "lower"
    UPPER = "upper"
    PROPER = "proper"
    PAD = "pad"
    TRIM = "trim"
    REVERSE = "reverse"
    REMOVE_ACCENTS = "remove"
    REMOVE_SPECIAL_CHARS = "remove"
    REMOVE_WHITE_SPACES = "remove"
    LEFT = "left"
    RIGHT = "right"
    MID = "mid"
    REPLACE = "replace"
    REPLACE_REGEX = "replace"
    FILL_NA = "fill_na"
    CAST = "cast"
    IS_NA = "is_na"
    Z_SCORE = "z_score"
    NEST = "nest"
    UNNEST = "unnest"
    SET = "set"
    STRING_TO_INDEX = "string_to_index"
    DATE_FORMAT = "date_format"
    INDEX_TO_STRING = "index_to_string"
    MIN_MAX_SCALER = "min_max_scaler"
    MAX_ABS_SCALER = "max_abs_scaler"
    STANDARD_SCALER = "standard_scaler"
    APPLY_COLS = "apply_cols"
    YEARS_BETWEEN = "apply_cols"
    IMPUTE = "impute"
    EXTRACT = "extract"
    ABS = "abs"
    MATH = "math"
    VARIANCE = "variance"
    SLICE = "slice"
    CLIP = "clip"
    DROP = "drop"
    KEEP = "keep"
    CUT = "cut"
    TO_FLOAT = "to_float"
    TO_INTEGER = "to_integer"
    TO_BOOLEAN = "to_boolean"
    TO_STRING = "to_string"
    YEAR = "years"
    APPEND = "append"
    PORT = "port"
    COPY = "copy"
    RENAME = "rename"
    UNIQUE = "unique"
    INFER = "infer"
    WORD_TOKENIZE = "word_tokenize"
    LENGTH = "length"
    GET = "get"
    ITEM = "item"

    # URL Example	http://search.somedb.com:8080/history?era=darkages
    # scheme	http
    # hostname	search.somedb.com
    # port	    8080
    # origin	http://search.somedb.com:8080
    # path	    /history
    # query	    ?era=darkages
    DOMAIN = "domain"
    DOMAIN_SCHEME = "domain_scheme"
    SUBDOMAIN = "subdomain"
    HOST = "host"
    DOMAIN_PARAMS = "domain_params"
    DOMAIN_PATH = "domain_path"

    EMAIL_DOMAIN = "email_domain"
    EMAIL_USER = "email_user"

    # ROWS
    SELECT_ROW = "select_row"
    DROP_ROW = "drop_row"
    BETWEEN_ROW = "between_drop"
    SORT_ROW = "sort_row"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Actions))


class ProfilerDataTypesQuality(Enum):
    MISMATCH = 0
    MISSING = 1
    MATCH = 2


class ProfilerDataTypes(Enum):
    INT = "int"
    DECIMAL = "decimal"
    STRING = "str"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    ARRAY = "array"
    OBJECT = "object"
    GENDER = "gender"
    IP = "ip"
    URL = "url"
    EMAIL = "email"
    CREDIT_CARD_NUMBER = "credit_card_number"
    ZIP_CODE = "zip_code"
    MISSING = "missing"
    CATEGORICAL = "categorical"
    PHONE_NUMBER = "phone_number"
    SOCIAL_SECURITY_NUMBER = "social_security_number"
    HTTP_CODE = "http_code"
    US_STATE = "us_state"
    NULL = "null"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ProfilerDataTypes))

    # NULL = "null"
    # MISSING = "missing"


class Schemas(Enum):
    S3 = 's3://'
    GCS = 'gcs://'
    GC = 'gc://'
    HTTP = 'http://'
    HTTPS = 'https://'
    FTP = 'ftp://'
    FILE = 'file://'
    AZ = 'az://'
    ADL = 'adl://'
    ABFS = 'abfs://'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Schemas))


PROFILER_NUMERIC_DTYPES = [ProfilerDataTypes.INT.value, ProfilerDataTypes.DECIMAL.value]
PROFILER_STRING_DTYPES = [ProfilerDataTypes.STRING.value, ProfilerDataTypes.BOOLEAN.value,
                          ProfilerDataTypes.DATETIME.value, ProfilerDataTypes.ARRAY.value,
                          ProfilerDataTypes.OBJECT.value, ProfilerDataTypes.GENDER.value,
                          ProfilerDataTypes.IP.value, ProfilerDataTypes.URL.value,
                          ProfilerDataTypes.EMAIL.value, ProfilerDataTypes.CREDIT_CARD_NUMBER.value,
                          ProfilerDataTypes.ZIP_CODE.value, ProfilerDataTypes.PHONE_NUMBER,
                          ProfilerDataTypes.SOCIAL_SECURITY_NUMBER.value,
                          ProfilerDataTypes.HTTP_CODE.value, ProfilerDataTypes.US_STATE.value]

# Strings and Function Messages
JUST_CHECKING = "Just check that all necessary environments vars are present..."
STARTING_OPTIMUS = "Transform and Roll out..."

SUCCESS = "Optimus successfully imported. Have fun :)."

CONFIDENCE_LEVEL_CONSTANT = [50, .67], [68, .99], [90, 1.64], [95, 1.96], [99, 2.57]


def print_check_point_config(filesystem):
    logger.print(
        "Setting checkpoint folder %s. If you are in a cluster initialize Optimus with master='your_ip' as param",
        filesystem)


# For Google Colab
JAVA_PATH_COLAB = "/usr/lib/jvm/java-8-openjdk-amd64"
RELATIVE_ERROR = 10000

# Buffer size in rows
BUFFER_SIZE = 500000
US_STATES_NAMES = ["alabama",
                   "alaska",
                   "american samoa",
                   "arizona",
                   "arkansas",
                   "california",
                   "colorado",
                   "connecticut",
                   "delaware",
                   "district of columbia",
                   "federated states of micronesia",
                   "florida",
                   "georgia",
                   "guam",
                   "hawaii",
                   "idaho",
                   "illinois",
                   "indiana",
                   "iowa",
                   "kansas",
                   "kentucky",
                   "louisiana",
                   "maine",
                   "marshall islands",
                   "maryland",
                   "massachusetts",
                   "michigan",
                   "minnesota",
                   "mississippi",
                   "missouri",
                   "montana",
                   "nebraska",
                   "nevada",
                   "new hampshire",
                   "new jersey",
                   "new mexico",
                   "new york",
                   "north carolina",
                   "north dakota",
                   "northern mariana islands",
                   "ohio",
                   "oklahoma",
                   "oregon",
                   "palau",
                   "pennsylvania",
                   "puerto rico",
                   "rhode island",
                   "south carolina",
                   "south dakota",
                   "tennessee",
                   "texas",
                   "utah",
                   "vermont",
                   "virgin islands",
                   "virginia",
                   "washington",
                   "west virginia",
                   "wisconsin",
                   "wyoming"
                   ]
US_STATES_CODE = [
    "al",
    "ak",
    "as",
    "az",
    "ar",
    "ca",
    "co",
    "ct",
    "de",
    "dc",
    "fm",
    "fl",
    "ga",
    "gu",
    "hi",
    "id",
    "il",
    "in",
    "ia",
    "ks",
    "ky",
    "la",
    "me",
    "mh",
    "md",
    "ma",
    "mi",
    "mn",
    "ms",
    "mo",
    "mt",
    "ne",
    "nv",
    "nh",
    "nj",
    "nm",
    "ny",
    "nc",
    "nd",
    "mp",
    "oh",
    "ok",
    "or",
    "pw",
    "pa",
    "pr",
    "ri",
    "sc",
    "sd",
    "tn",
    "tx",
    "ut",
    "vt",
    "vi",
    "va",
    "wa",
    "wv",
    "wi",
    "wy"
]
CURRENCIES = {"$": "dollar",
              "¢": "cent",
              "£": "point",
              "€": "euro",
              "¥": "yen",
              "₹": "indian rupee",
              "₽": "ruble",
              "元": "yuan",
              "¤": "currency",
              "₠": "euro-currency",
              "₡": "colon",
              "₢": "cruzeiro",
              "₣": "french franc",
              "₤": "lira",
              "₥": "mill",
              "₦": "naira",
              "₧": "peseta",
              "₨": "rupee",
              "₩": "won",
              "₪": "new shequel",
              "₫": "dong",
              "₭": "kip",
              "₮": "tugrik",
              "₯": "drachma",
              "₰": "german penny",
              "₱": "peso",
              "₲": "guarani",
              "₳": "austral",
              "₴": "hryvnia",
              "₵": "cedi",
              "₶": "livre tournois",
              "₸": "tenge",
              "₺": "turkish lira",
              "₼": "manat",
              "৲": "bengali rupee mark",
              "৳": "bengali rupee sign",
              "૱": "gujarati rupee sign",
              "௹": "tamil rupee sign",
              "฿": "thai currency bath",
              "៛": "khmer currency reil",
              "㍐": "square yuan",
              "円": "yen character",
              "圆": "yen/yuan character variant one",
              "圎": "yen/yuan character variant two",
              "圓": "yuan character, in hong kong and taiwan",
              "圜": "yen/yuan character variant three",
              "원": "won character",
              "﷼": "rial sign",
              "＄": "fullwidth dollar sign",
              "￠": "fullwidth cent sign",
              "￡": "fullwidth pound sign",
              "￥": "fullwidth yen sign",
              "￦": "fullwidth won sign"}
PYTHON_SHORT_TYPES = {"string": "string",
                      "str": "string",
                      "integer": "int",
                      "int": "int",
                      "float": "float",
                      "double": "double",
                      "bool": "boolean",
                      "boolean": "boolean",
                      "array": "array",
                      "null": "null"
                      }
PYTHON_TYPES = {"string": str, "int": int, "float": float, "boolean": bool}
PROFILER_COLUMN_TYPES = {"categorical", "numeric", "date", "null", "array", "binary"}
PYTHON_TO_PROFILER = {"string": "categorical", "boolean": "categorical", "int": "numeric", "float": "numeric",
                      "decimal": "numeric", "date": "date", "array": "array", "binary": "binary", "null": "null"}

PROFILER_CATEGORICAL_DTYPES = [ProfilerDataTypes.BOOLEAN.value, ProfilerDataTypes.ZIP_CODE.value,
                               ProfilerDataTypes.STRING.value, ProfilerDataTypes.HTTP_CODE.value,
                               ProfilerDataTypes.INT.value, ProfilerDataTypes.IP.value, ProfilerDataTypes.GENDER.value,
                               ProfilerDataTypes.PHONE_NUMBER.value, ProfilerDataTypes.US_STATE.value,
                               ProfilerDataTypes.SOCIAL_SECURITY_NUMBER.value
                               ]

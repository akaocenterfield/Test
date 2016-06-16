rom pydruid.client import *
from pydruid.utils.aggregators import *
from pydruid.utils.filters import *
from pylab import plt


query = PyDruid('http://amazonaws.com:8082', 'druid/v2/')

top_langs = query.topn(
    datasource = "clicks",
    granularity = "all",
    intervals = "2016-02-01T00:00:00/2016-02-02T00:00:00",
    dimension = "key",
    filter = Dimension("date_key") == "2016-02-01",
    aggregations = {"count": doublesum("count")},
    metric = "count",
    threshold = 5
)


top_langs = query.groupby(
    datasource = "ClickDataSource",
    granularity = "all",
    intervals = "2016-01-01T00:00/2020-01-01T00",
    aggregations={"count": doublesum("count")},

)


print top_langs

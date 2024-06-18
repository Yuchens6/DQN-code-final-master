from myenv import get_jaeger_data_
from myenv import get_prometheus_data_
from myenv import jaeger_finder_v2
from myenv import pro_datefinder
from myenv import memcached

def get_pro_data():
    # get_jaeger_data_.GetJaegerData()
    #get_prometheus_data_.GetPrometheusData()
    jaeger_finder_v2.JaegerData()
    memcached.GetMemcacehdState()

# jaeger_finder_v2.JaegerData()
# pro_datefinder.PrometheusData()


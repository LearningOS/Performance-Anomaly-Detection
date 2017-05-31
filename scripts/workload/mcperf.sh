mcperf \
    --server=172.17.0.3 \
    --linger=0 \
    --timeout=5 \
    --conn-rate=100 \
    --call-rate=1000 \
    --num-calls=10 \
    --num-conns=100000000 \
    --sizes=e5

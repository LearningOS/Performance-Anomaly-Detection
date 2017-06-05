sysbench \
    --test=oltp \
    --oltp-table-size=1000000 \
    --mysql-host=172.17.0.2 \
    --mysql-db=test \
    --mysql-user=root \
    --mysql-password=root \
    --max-time=0 \
    --max-requests=0 \
    --num-threads=4 \
    --oltp-reconnect-mode=random \
    run
bind = "127.0.0.1:9001"                   # Don't use port 80 becaue nginx occupied it already. 
errorlog = '/home/carlos/transcoding/logs/gunicorn-error.log'  # Make sure you have the log folder create
accesslog = '/home/carlos/transcoding/logs/gunicorn-access.log'
loglevel = 'debug'
workers = 10     # the number of recommended workers is '2 * number of CPUs + 1' 

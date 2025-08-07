# Gunicorn configuration file for production deployment

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000

# Request handling
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Application
preload_app = True

# Security
user = "app"
group = "app"
tmp_upload_dir = None

# Proxy settings
secure_scheme_headers = {
    'X-FORWARDED-PROTO': 'https',
}
forwarded_allow_ips = '*'

# Logging
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'

# Process naming
proc_name = 'phonetics-app'

# Restart workers after this many requests (helps with memory leaks)
max_requests = 1000
max_requests_jitter = 50

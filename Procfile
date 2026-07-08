web: gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 0 --graceful-timeout 30 --access-logfile - --error-logfile -

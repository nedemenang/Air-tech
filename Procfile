web: gunicorn run:app
worker: ./redis-5.0.4/src/redis-server
worker: celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid
worker: celery worker -A app.celery --loglevel=INFO
release: python run.py db upgrade 
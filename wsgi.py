from gpay_insights import create_app

server, dash_app = create_app()

# gunicorn example:
# gunicorn wsgi:server -b 0.0.0.0:8000 --workers 3

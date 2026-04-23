import os
import sys

from app import create_app


app = create_app()
application = app


def run_with_gunicorn():
    from gunicorn.app.wsgiapp import run

    port = os.environ.get("PORT", "5001")
    workers = os.environ.get("GUNICORN_WORKERS", "1")
    bind = os.environ.get("GUNICORN_BIND", f"0.0.0.0:{port}")
    argv = ["gunicorn", "-w", workers, "-b", bind]
    if os.environ.get("GUNICORN_RELOAD") == "1":
        argv.append("--reload")
    argv.append("app:create_app()")
    sys.argv = argv
    run()


if __name__ == "__main__":
    run_with_gunicorn()


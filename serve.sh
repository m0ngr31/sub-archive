#!/bin/sh

export FLASK_APP=server.py
exec gunicorn server:app -b 0.0.0.0:5000

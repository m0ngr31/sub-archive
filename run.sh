#!/bin/sh

exec gunicorn server:app -b 0.0.0.0:5000
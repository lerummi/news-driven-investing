#!/bin/bash

mlflow models serve -p $1 -m runs:/$2/model -h 0.0.0.0 --env-manager local
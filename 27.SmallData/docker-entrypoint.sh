#!/bin/bash

PYTHONPATH=$PYTHONPATH:/home/src jupyter notebook \
  --ip=0.0.0.0 \
  --port=8085 \
  --allow-root 
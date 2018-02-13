#!/usr/bin/env bash
conda create --name venv --yes
source activate venv
pip install -r requirements.txt

python ./run_total_crawl.py
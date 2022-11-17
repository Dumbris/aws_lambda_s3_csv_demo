# Processing data from S3 files using AWS Lambda and pandas

## Local run, development

```bash
git clone *this_repo*
cd *this_repo*
virtualenv -p python3 .pyenv
source .pyenv/bin/activate
pip install -e .
mkdir -p data
wget https://github.com/carVertical/data-engineering-homework/raw/master/data/Open_Data_RDW.csv data/Open_DataRDW.csv
python python voertuigen/main.py
```


## Run unittests
```
pytest -vv
```
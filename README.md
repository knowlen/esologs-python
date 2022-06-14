# eso-builds


# Quickstart
---
## Install
1. Clone the repo
2. Create a virtual environment
3. Install dependencies 
```Bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Download Data
```Bash
cd ./scripts
python pull_data.py --target-spec stamina --target-class nightblade --target-patch 34 --output-directory ./test --api-key my_esologs_api_key
```

# eso-builds


## Quickstart
---
### Install
1. Clone the repo
2. Create a virtual environment
3. Install dependencies 
```Bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Download Data
---
```Bash
cd ./scripts
python pull_data.py --target-spec stamina --target-class nightblade --target-patch 34 --output-directory ./test --api-key my_esologs_api_key
```
#### pull_data.py
```Bash
usage: pull_data.py [-h] [--api-key API_KEY] -s TARGET_SPEC -c TARGET_CLASS [-p TARGET_PATCH] [-o OUTPUT_DIRECTORY] [-n NUM_PAGES] [-d MIN_DPS]

optional arguments:
  -h, --help            show this help message and exit
  --api-key API_KEY     api key allocated by esologs.com
  -s TARGET_SPEC, --target-spec TARGET_SPEC
                        target spec: tank, magicka, stamina, werewolf, healer, or all
  -c TARGET_CLASS, --target-class TARGET_CLASS
                        target class: dragonknight, nightblade, necromancer, sorcerer, templar, warden, or all
  -p TARGET_PATCH, --target-patch TARGET_PATCH
                        patch number to consider: 22 to 34, or 'all' will pull data from every patch
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        path to output the data files
  -n NUM_PAGES, --num-pages NUM_PAGES
                        number of pages to consider (each page <= 20 characters)
  -d MIN_DPS, --min-dps MIN_DPS
                        ignore parses below this value
```


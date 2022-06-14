# eso-builds
Probably requires Python >= 3.6. Tested on MacOS, but should work on any operating system. 


# Quickstart
---
## Install
1. Clone this repo
2. Create a virtual environment (optional)
3. Install dependencies 
```Bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Obtain API Key
Set V1 Client Name and generate a key in the Web API section at the bottom of ![this page](https://www.esologs.com/profile).

## Download Data
Example
```Bash
$ cd ./scripts
$ python pull_data.py --target-spec stamina --target-class nightblade --target-patch 34 --output-directory ./test --api-key my_esologs_api_key
```
Output:
```Text
[update 34] stamina nightblade
 * found 6 parses over 40k dps
 * query: https://www.esologs.com:443/v1/rankings/encounter/3009?metric=dps&partition=13&class=2&spec=3&page=1&includeCombatantInfo=true&api_key=
```
![Output file](/examples/34-stamina-nightblade.json)

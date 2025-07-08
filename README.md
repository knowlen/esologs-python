# python-esologs
A Python frontend for the [https://www.esologs.com/](esologs) API. 

Note: This project is early. Eventually should have full converage of the [v2 API schema](https://www.esologs.com/v2-api-docs/eso/)

Requires at least Python >= 3.6. Tested on MacOS, but should work on all platforms.


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
1. Create a v2 client at [this page](https://www.esologs.com/api/clients/).
2. Export your Client Id and Client Secret as __ESOLOGS_ID__ and __ESOLOGS_SECRET__ environment variables
3. Client code should now connect to the API

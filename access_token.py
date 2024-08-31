import os
import requests
import base64
import requests

def get_access_token(client_id: str = None, client_secret: str = None) -> str:
    endpoint = 'https://www.esologs.com/oauth/token'
    if not client_id:
        client_id = os.environ.get('ESOLOGS_ID')
        print(client_id)
    if not client_secret:
        client_secret = os.environ.get('ESOLOGS_SECRET')
        print(client_secret)

    auth_str = f'{client_id}:{client_secret}'
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    response = requests.post(
        endpoint,
        headers={
            'Authorization': f'Basic {auth_base64}',
        },
        data={
            'grant_type': 'client_credentials'
        }
    )

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f'Response was not OK: {response.text}')

def download_remote_schema(url: str, headers: dict):
    # Define the GraphQL introspection query to fetch the schema
    introspection_query = {
        "query": """
        {
            __schema {
                types {
                    name
                    kind
                    fields {
                        name
                        type {
                            name
                            kind
                        }
                    }
                }
            }
        }
        """
    }
    
    # Make the request to the GraphQL API
    response = requests.post(url, json=introspection_query, headers=headers)
    
    if response.status_code == 200:
        # Assuming you want to save the schema to a file
        with open('schema.json', 'w') as file:
            file.write(response.text)
        print("Schema downloaded and saved to 'schema.json'")
    else:
        raise Exception(f'Failed to download schema: {response.text}')

def download_eso_logs_schema(client_id: str, client_secret: str):
    # Step 1: Get the access token
    access_token = get_access_token(
        'https://www.esologs.com/oauth/token',
        client_id,
        client_secret
    )

    # Step 2: Download the schema with a GraphQL query
    download_remote_schema(
        'https://www.esologs.com/api/v2/client',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
    )

if __name__ == "__main__":
    credentials = {
        'clientId': '',
        'clientSecret': ''  
        }
    access_token = get_access_token(client_id=credentials['clientId'], client_secret=credentials['clientSecret'])
    #access_token = get_access_token()
    print(access_token)


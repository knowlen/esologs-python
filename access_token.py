import os
import requests
import base64
import logging
from typing import Optional

def get_access_token(client_id: Optional[str] = None, client_secret: Optional[str] = None) -> str:
    """Get OAuth2 access token for ESO Logs API.
    
    Args:
        client_id: ESO Logs client ID (optional, will use ESOLOGS_ID env var if not provided)
        client_secret: ESO Logs client secret (optional, will use ESOLOGS_SECRET env var if not provided)
        
    Returns:
        Access token string
        
    Raises:
        ValueError: If credentials are missing
        Exception: If OAuth request fails
    """
    endpoint = 'https://www.esologs.com/oauth/token'
    
    if not client_id:
        client_id = os.environ.get('ESOLOGS_ID')
        if not client_id:
            raise ValueError("Client ID not provided and ESOLOGS_ID environment variable not set")
            
    if not client_secret:
        client_secret = os.environ.get('ESOLOGS_SECRET')
        if not client_secret:
            raise ValueError("Client secret not provided and ESOLOGS_SECRET environment variable not set")
    
    logging.debug("Requesting OAuth token from ESO Logs API")

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
        token_data = response.json()
        access_token = token_data.get('access_token')
        if not access_token:
            raise Exception("Access token not found in response")
        logging.debug("Successfully obtained access token")
        return access_token
    else:
        logging.error(f"OAuth request failed with status {response.status_code}")
        raise Exception(f'OAuth request failed with status {response.status_code}: {response.text}')

def download_remote_schema(url: str, headers: dict, output_file: str = 'schema.json') -> None:
    """Download GraphQL schema using introspection query.
    
    Args:
        url: GraphQL endpoint URL
        headers: Request headers including authorization
        output_file: Output file path for schema
        
    Raises:
        Exception: If schema download fails
    """
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
        with open(output_file, 'w') as file:
            file.write(response.text)
        logging.info(f"Schema downloaded and saved to '{output_file}'")
    else:
        logging.error(f"Failed to download schema: {response.status_code}")
        raise Exception(f'Failed to download schema: {response.status_code} - {response.text}')

def download_eso_logs_schema(client_id: str, client_secret: str, output_file: str = 'schema.json') -> None:
    """Download ESO Logs GraphQL schema.
    
    Args:
        client_id: ESO Logs client ID
        client_secret: ESO Logs client secret
        output_file: Output file path for schema
    """
    # Step 1: Get the access token
    access_token = get_access_token(client_id, client_secret)

    # Step 2: Download the schema with a GraphQL query
    download_remote_schema(
        'https://www.esologs.com/api/v2/client',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        },
        output_file=output_file
    )

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Get access token using environment variables
        access_token = get_access_token()
        print("Access token obtained successfully")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


"""
Constructs a URL string using the values of the environment variables "COGNITO_REGION" 
and "COGNITO_POOL_ID".

Returns:
    str: The constructed URL string.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Set the values of the environment variables
os.environ["COGNITO_REGION"] = "us-west-2"
os.environ["COGNITO_POOL_ID"] = "1234567890"

# Construct the URL string
region = os.environ.get("COGNITO_REGION")
pool_id = os.environ.get("COGNITO_POOL_ID")

jwks_url = f"https://cognito-idp.{region}.amazonaws.com/"
jwks_url += f"/{pool_id}/.well-known/"

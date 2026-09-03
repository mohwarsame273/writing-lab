try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import os
from dotenv import load_dotenv
load_dotenv("variables.env")

from google import genai
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    response = client.models.embed_content(
        model="text-embedding-004",
        contents="Hello world"
    )
    print("Success text-embedding-004")
except Exception as e:
    print(f"Error text-embedding-004: {e}")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello world"
    )
    print("Success gemini-2.5-flash")
except Exception as e:
    print(f"Error gemini-2.5-flash: {e}")

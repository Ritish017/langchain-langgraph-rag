# Import ChatGoogleGenerativeAI class for Google Gemini integration
from langchain_google_genai import ChatGoogleGenerativeAI
# Import load_dotenv function to load environment variables from .env file
from dotenv import load_dotenv
import os
# Load environment variables from .env file (contains API keys)
load_dotenv()

# Configure SSL for corporate networks
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH'
os.environ['GRPC_VERBOSITY'] = 'ERROR'

# Define function to create and configure Gemini LLM instance
def create_geminillm():
    # Create ChatGoogleGenerativeAI instance with specific configuration
    geminillm = ChatGoogleGenerativeAI(
        # Specify the Gemini model version to use
        model="gemini-2.5-flash",
        # Set temperature to 0 for deterministic responses
        temperature=0,
        # Limit maximum output tokens to 1024
        max_output_tokens=1024,
    )
    # Return the configured Gemini LLM instance
    return geminillm


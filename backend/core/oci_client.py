import oci
import logging
import oci.generative_ai_inference
from dotenv import load_dotenv
import os
load_dotenv()

# --- OCI Configuration ---
# The SDK will automatically load the configuration from ~/.oci/config
# Ensure your config file is set up correctly.
CONFIG_PROFILE = "DEFAULT"
COMPARTMENT_ID = os.getenv("COMPARTMENT_ID")  # <--- REPLACE THIS
ENDPOINT = os.getenv("ENDPOINT") # <-- REPLACE with your region's inference endpoint
LLAMA2_MODEL_OCID = os.getenv("LLAMA2_MODEL_OCID")  # <--- REPLACE THIS

def get_llama2_completion(prompt: str) -> dict:
    """Calls the OCI LLaMA2 completion API using the chat endpoint."""
    logging.info("Calling OCI LLaMA2 chat model...")
    
    try:
        config = oci.config.from_file(profile_name=CONFIG_PROFILE)
        generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=ENDPOINT, timeout=600)
        
        # Constructing the chat request
        content = oci.generative_ai_inference.models.TextContent()
        content.text = prompt
        
        message = oci.generative_ai_inference.models.Message()
        message.role = "USER"
        message.content = [content]
        
        chat_request = oci.generative_ai_inference.models.GenericChatRequest()
        chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
        chat_request.messages = [message]
        chat_request.max_tokens = 600
        chat_request.temperature = 1
        chat_request.frequency_penalty = 0
        chat_request.presence_penalty = 0
        chat_request.top_p = 0.75
        
        chat_detail = oci.generative_ai_inference.models.ChatDetails()
        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=LLAMA2_MODEL_OCID)
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = COMPARTMENT_ID

        chat_response = generative_ai_inference_client.chat(chat_detail)
        print(chat_response.data)

        # Extracting the response text
        text_response = chat_response.data.chat_response.choices[0].message.content[0].text
        if not text_response:
            raise ValueError("No text response received from the model.")
        logging.info("LLaMA2 chat model call successful.")
        
        return {"choices": [{"text": text_response}]}

    except Exception as e:
        logging.error(f"Error calling OCI LLaMA2 chat model: {e}")
        # Return a mock response on failure to avoid breaking the flow
        return {
            "choices": [
                {
                    "text": f"Error: Could not get response from OCI model. Details: {e}"
                }
            ]
        }
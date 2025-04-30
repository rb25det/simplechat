import json
import os
import requests

# FastAPIサーバーのURL
FASTAPI_URL = "https://a3e8-34-124-205-185.ngrok-free.app/generate"
def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        body = json.loads(event['body'])
        message = body['message']

        print("Processing message:", message)

        payload = {
            "prompt": message,
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9
        }

        print(f"Calling FastAPI: {FASTAPI_URL} with payload: {json.dumps(payload)}")

        response = requests.post(FASTAPI_URL, json=payload)
        response.raise_for_status()

        response_body = response.json()
        print("FastAPI response:", json.dumps(response_body))

        assistant_response = response_body["generated_text"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_response}
                ]
            })
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
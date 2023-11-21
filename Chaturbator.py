import requests
import subprocess

# API endpoint URL
api_url = "http://localhost:11434/api/generate"

# INSERT YOUR LLM MODEL HERE!!!
model = "wizardlm-uncensored:13b"

while True:
    # SET THE TOPIC TO CHATURBATE ABOUT!!!
    user_input = "Historic fun facts"

    # Form initial prompt
    initial_prompt = f"Generate an expert and focused prompt on the topic: {user_input}"
    print("\n\nInitial Prompt:", initial_prompt)

    # Use TTS to say the initial prompt
    subprocess.run(["say", initial_prompt])

    # Create the payload for the request with the initial prompt
    payload = {
        "model": model,
        "prompt": f"{initial_prompt}\nKeep your answer reasonably short, focused and concise!",
        "stream": False
    }

    # Make the POST request to the API with stream=False
    response = requests.post(api_url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Get the generated text from the response JSON
            response_json = response.json()
            generated_prompt = response_json.get("response", "")

            # Display the API generated prompt
            print("\n\nGenerated Prompt:", generated_prompt)

            # Use TTS to say the generated prompt
            subprocess.run(["say", generated_prompt])

            # Now, the generated prompt becomes the input for the next iteration
            user_input = generated_prompt

            # Create the payload for the request with the generated prompt
            new_prompt_payload = {
                "model": model,
                "prompt": f"{generated_prompt}\nKeep your answer reasonably short, focused and concise!",
                "stream": False
            }

            # Make the POST request to the API with stream=False for the generated prompt
            new_response = requests.post(api_url, json=new_prompt_payload)

            # Check if the request for the new prompt was successful (status code 200)
            if new_response.status_code == 200:
                try:
                    # Get the generated text from the response JSON for the new prompt
                    new_response_json = new_response.json()
                    new_generated_text = new_response_json.get("response", "")

                    # Display the API answer for the new prompt
                    print("\n\nAPI Answer for the New Prompt:", new_generated_text)

                    # Use TTS to say the API answer for the new prompt
                    subprocess.run(["say", new_generated_text])

                except requests.exceptions.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
            else:
                # Display an error message if the request for the new prompt was not successful
                print("Error for new prompt:", new_response.status_code, new_response.text)

        except requests.exceptions.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        # Display an error message if the request was not successful
        print("Error:", response.status_code, response.text)

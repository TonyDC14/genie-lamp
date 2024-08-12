import openai

class OpenAIClient:
    """
    Handles interactions with the OpenAI API.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = openai.ChatCompletion.create

    def openai_chat_request_prompt(self, system_prompt: str, usr_prompt: str, max_tokens=2048):
        """
        Sends a prompt to the OpenAI API and returns the response.
        """
        response = self.client(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": usr_prompt}
            ],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message['content']

    def send_prompts_in_chunks(self, prompts: list, max_tokens=2048):
        """
        Sends a list of prompts to OpenAI in chunks and returns a list of responses.
        """
        responses = []
        for prompt in prompts:
            response = self.openai_chat_request_prompt("This is a programming project", prompt, max_tokens)
            responses.append(response)
        return responses

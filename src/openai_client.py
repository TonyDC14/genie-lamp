import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt


class OpenAIClient:
    """ Handles interactions with the OpenAI API. """
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.ChatCompletion.create

    # @retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def openai_chat_request_prompt(self, system_prompt: str, usr_prompt: str, max_tokens=2000000):
        response = self.client(
            model="gpt-4o-2024-08-06",
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

    def send_chunks_with_context(self, chunks, final_prompt, max_tokens=2000000):
        messages = [{"role": "system", "content": "This is a programming project"}]
        for i, chunk in enumerate(chunks):
            messages.append({"role": "user", "content": chunk})
            if i < len(chunks) - 1:
                # Send the chunk without expecting a response
                self.client(
                    model="gpt-4o-2024-08-06",
                    messages=messages,
                    temperature=0
                )
            else:
                # For the last chunk, request a response
                messages.append({"role": "user", "content": final_prompt})
                response = self.client(
                    model="gpt-4",
                    messages=messages,
                    temperature=0
                )
                return response.choices[0].message['content']
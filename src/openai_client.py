import logging
import time
from typing import List

import openai

logger = logging.getLogger(__name__)


class OpenAIClient:

    def __init__(self, api_key: str, model):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)

    def ask_by_chunks(self, chunks: List):
        openai_assistant = self.client.beta.assistants.create(
            name="Code Reviewer",
            instructions="You are a professional SR developer. Write and fix code to solve user requirements.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )
        openai_thread = self.client.beta.threads.create()

        for index, chunk in enumerate(chunks):
            message = self.client.beta.threads.messages.create(
                thread_id=openai_thread.id,
                role="user",
                content=chunk,
            )

            logger.info(f"Sent fragment {index + 1}, waiting for 60 seconds to send the next one...")
            # time.sleep(60)

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=openai_thread.id,
            assistant_id=openai_assistant.id,
            instructions="Please provide detailed answer of the full given requirement.",
        )

        logger.info("Run completed with status: " + run.status)

        final_response = ""
        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=openai_thread.id)

            for message in messages:
                if message.role == "assistant":
                    assert message.content[0].type == "text"
                    final_response = message.content[0].text.value
                    logger.info("Assistant's response:")
                    logger.info(final_response)
                    break  # Stop after the first assistant message, assuming it's the relevant response.

        self.client.beta.assistants.delete(openai_assistant.id)
        return final_response

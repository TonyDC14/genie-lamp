import tiktoken


class PromptProcessor:
    def __init__(self, model_name: str, max_length: int):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.max_length = int(max_length)
        self.token_buffer = 30

    def split_prompt(self, prompt: str) -> list[str]:
        tokens = self.__encode_prompt(prompt)
        return self.__chunk_prompt(tokens)

    def __encode_prompt(self, prompt: str) -> list[int]:
        return self.encoding.encode(prompt)

    def __chunk_prompt(self, tokens: list[int]) -> list[str]:
        max_chunk_size = self.max_length - self.token_buffer
        chunks = []
        for i in range(0, len(tokens), max_chunk_size):
            chunk = self.encoding.decode(tokens[i:i + max_chunk_size])
            chunks.append(chunk)
        return chunks


class PromptBuilder:

    def __init__(self, project_content, requirements, documentation, prompt_processor: PromptProcessor):
        self.project_content = project_content
        self.requirements = requirements
        self.documentation = documentation
        self.prompt_processor = prompt_processor

        self.generated_prompts = []

    def build(self):
        prompts = ""
        prompts += self.__generate_main_prompt()
        prompts += self.__generate_requirements_prompt()
        prompts += self.__generate_documentation_prompt()
        prompts += self.__generate_final_prompt()
        self.generated_prompts = self.prompt_processor.split_prompt(prompts)
        return self

    def __generate_main_prompt(self):
        return (f"I have this current programming project, will pass you later a set of instructions involved "
                f"with < and > to solve, need you to generate a response of it given the project and "
                f"documentation as context with new requirements to perform:\n{self.project_content}")

    def __generate_requirements_prompt(self):
        if not self.requirements:
            return []
        return f" | New Requirements that I need you to solve are: <\n{self.requirements}>"

    def __generate_documentation_prompt(self):
        if not self.documentation:
            return []
        return f" | Additional documentation is:\n{self.documentation}"

    def __generate_final_prompt(self):
        return ("Now given all this context, I need you to solve the <requirements>, generate a full "
                "detailed explanation of how to solve the requirements with code snippets if possible if you"
                "edit any line of code and return and snippet of it comment each modified line with # m and if"
                "you need to add new code comment the new lines with # n")

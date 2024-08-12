class PromptGenerator:
    """
    Generates prompts from project content and user inputs.
    """
    def __init__(self, project_content, requirements, documentation):
        self.project_content = project_content
        self.requirements = requirements
        self.documentation = documentation

    def generate_prompts(self, max_length):
        """
        Generates prompts by concatenating project content, requirements, and documentation.
        Splits them into chunks if they exceed the maximum length.
        """
        prompts = []
        main_prompt = f"This is my current programming project:\n{self.project_content}"
        prompts.extend(self._split_prompt(main_prompt, max_length))

        if self.requirements:
            requirements_prompt = f"New Requirements:\n{self.requirements}"
            prompts.extend(self._split_prompt(requirements_prompt, max_length))

        if self.documentation:
            documentation_prompt = f"Documentation:\n{self.documentation}"
            prompts.extend(self._split_prompt(documentation_prompt, max_length))

        return prompts

    @staticmethod
    def _split_prompt(prompt, max_length):
        """
        Splits a prompt into chunks of a specified maximum length.
        """
        return [prompt[i:i + max_length] for i in range(0, len(prompt), max_length)]

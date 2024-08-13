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
        main_prompt = (f"I have this current programming project, will pass you later a set of instructions involved "
                       f"with < and > to solve, need you to generate a response of it given the project and "
                       f"documentation as context with "
                       f"new requirements to perform:\n{self.project_content}")
        prompts.extend(self._split_prompt(main_prompt, max_length))

        if self.requirements:
            requirements_prompt = f" | New Requirements that I need you to solve are: <\n{self.requirements}>"
            prompts.extend(self._split_prompt(requirements_prompt, max_length))

        if self.documentation:
            documentation_prompt = f" | Optional documentation is:\n{self.documentation}"
            prompts.extend(self._split_prompt(documentation_prompt, max_length))

        final_prompt = ("Now given all this context, I need you to solve the <requirements>, generate a full "
                        "detailed explanation of how to solve the requirements with code snippets if possible")
        prompts.extend(self._split_prompt(final_prompt, max_length))

        return prompts

    @staticmethod
    def _split_prompt(prompt, max_length):
        """
        Splits a prompt into chunks of a specified maximum length.
        """
        return [prompt[i:i + max_length] for i in range(0, len(prompt), max_length)]

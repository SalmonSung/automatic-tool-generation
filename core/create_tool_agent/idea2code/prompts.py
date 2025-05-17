prompt_generate_code4idea = """
You are a skilled programmers. Your task is to write a Python method to achieve the idea use to analyze the given file.

Please notice that since your colleague are all AI. Do not rely on any visualise graph to analyze the data.
Following is the columns name, and index, if applicable.

<columns_info>
{columns_info}
<\columns_info>


"""

prompt_idea_code_cross_check = """
You are an expert Python developer and data scientist. Your task is to evaluate whether the provided Python code accurately and correctly implements the stated idea.

Please follow this process:

1. **If the code accomplishes the idea but is not a valid Python function or method**, rewrite it into valid Python code.
2. **If the code does not achieve the intended idea**, explain why and clearly state that it should be rejected.
3. The method should take file_path as the way to load the file.

Respond with either a corrected code block or a clear rejection.

<idea>
{idea}
</idea>
"""
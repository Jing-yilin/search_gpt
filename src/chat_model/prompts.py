from langchain.prompts.prompt import PromptTemplate

_template = """Please repeat the following question in english language, make sure the words are totally the same:
```
{question}
```
"""
REPEAT_QUESTION_PROMPT = PromptTemplate.from_template(_template)

_mapping_prompt_template = """For the field analysis result in {candidate_fileds}, which field do you want to map to {field}?
You can reply "" if you don't want to map any field.
Response the field name only!
"""

MAPPING_FIELD_PROMPT = PromptTemplate.from_template(_mapping_prompt_template)
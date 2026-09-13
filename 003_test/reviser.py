# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reviser agent for correcting inaccuracies based on verified findings."""

import os
from google.adk import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, Gemini
from google.genai import types

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

import sys
sys.path.append("../..")
from callback_logging import log_query_to_model, log_model_response

from . import prompt

_END_OF_EDIT_MARK = '---END-OF-EDIT---'


def _remove_end_of_edit_mark(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> LlmResponse:
    del callback_context  # unused
    if not llm_response.content or not llm_response.content.parts:
        return llm_response
    for idx, part in enumerate(llm_response.content.parts):
        if _END_OF_EDIT_MARK in part.text:
            del llm_response.content.parts[idx + 1 :]
            part.text = part.text.split(_END_OF_EDIT_MARK, 1)[0]
    return llm_response


reviser_agent = Agent(
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    name='reviser_agent',
    instruction=prompt.REVISER_PROMPT,
    before_model_callback=log_query_to_model,
    after_model_callback=_remove_end_of_edit_mark,
)

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Prompt for the reviser agent."""

REVISER_PROMPT = """
You are a professional editor working for a highly-trustworthy publication.
In this task you are given a question-answer pair to be printed to the publication. The publication reviewer has double-checked the answer text and provided the findings.
Your task is to minimally revise the answer text to make it accurate, while maintaining the overall structure, style, and length similar to the original.

The reviewer has identified CLAIMs (including facts and logical arguments) made in the answer text, and has verified whether each CLAIM is accurate, using the following VERDICTs:

    * Accurate: The information presented in the CLAIM is correct, complete, and consistent with the provided context and reliable sources.
    * Inaccurate: The information presented in the CLAIM contains errors, omissions, or inconsistencies when compared to the provided context and reliable sources.
    * Disputed: Reliable and authoritative sources offer conflicting information regarding the CLAIM, indicating a lack of definitive agreement on the objective information.
    * Unsupported: Despite your search efforts, no reliable source can be found to substantiate the information presented in the CLAIM.
    * Not Applicable: The CLAIM expresses a subjective opinion, personal belief, or pertains to fictional content that does not require external verification.

Editing guidelines for each type of claim:

  * Accurate claims: There is no need to edit them.
  * Inaccurate claims: You should fix them following the reviewer's justification, if possible.
  * Disputed claims: You should try to present two (or more) sides of an argument, to make the answer more balanced.
  * Unsupported claims: You may omit unsupported claims if they are not central to the answer. Otherwise you may soften the claims or express that they are unsupported.
  * Not applicable claims: There is no need to edit them.

As a last resort, you may omit a claim if they are not central to the answer and impossible to fix. You should also make necessary edits to ensure that the revised answer is self-consistent and fluent. You should not introduce any new claims or make any new statements in the answer text. Your edit should be minimal and maintain overall structure and style unchanged.

Output format:

  * If the answer is accurate, you should output exactly the same answer text as you are given.
  * If the answer is inaccurate, disputed, or unsupported, then you should output your revised answer text.
  * After the answer, output a line of "---END-OF-EDIT---" and stop.

Here are some examples of the task:

=== Example 1 ===

Question: Who was the first president of the US?

Answer: George Washington was the first president of the United States.

Findings:

  * Claim 1: George Washington was the first president of the United States.
      * Verdict: Accurate
      * Justification: Multiple reliable sources confirm that George Washington was the first president of the United States.
  * Overall verdict: Accurate
  * Overall justification: The answer is accurate and completely answers the question.

Your expected response:

George Washington was the first president of the United States.
---END-OF-EDIT---

=== Example 2 ===

Question: What is the shape of the sun?

Answer: The sun is cube-shaped and very hot.

Findings:

  * Claim 1: The sun is cube-shaped.
      * Verdict: Inaccurate
      * Justification: NASA states that the sun is a sphere of hot plasma, so it is not cube-shaped. It is a sphere.
  * Claim 2: The sun is very hot.
      * Verdict: Accurate
      * Justification: Based on my knowledge and the search results, the sun is extremely hot.
  * Overall verdict: Inaccurate
  * Overall justification: The answer states that the sun is cube-shaped, which is incorrect.

Your expected response:

The sun is sphere-shaped and very hot.
---END-OF-EDIT---

Here are the question-answer pair and the reviewer-provided findings:
"""

"""
QA tests for gpt.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

from src import gpt

# // TODO: mock this api call, bad practice to actually make a call
# commenting out because this is breaking the ci/cd pipeline

# def test_simple_gpt():
#     """
#     Testing the simple_gpt function
#     Calls the simple gpt and asks it to output
#     the days of the week. If the output does not contain
#     any day of the week, we assume the gpt is non-fucntional
#     """

#     surf_summary = ""
#     gpt_prompt = """Please output the days of the week in English. What day
#         is your favorite?"""

#     gpt_response = gpt.simple_gpt(surf_summary, gpt_prompt).lower()
#     expected_response = set([
#         "monday",
#         "tuesday",
#         "wednesday",
#         "thursday",
#         "friday" "saturday",
#         "sunday",
#         "一",
#         "二",
#         "三",
#         "四",
#         "五",
#     ])

#     # Can case the "gpt_response" string into a list, and
#     # check for set intersection with the expected response set
#     gpt_response_set = set(gpt_response.split())

#     assert gpt_response_set.intersection(
#         expected_response
#     ), f"Expected '{expected_response}', but got: {gpt_response}"

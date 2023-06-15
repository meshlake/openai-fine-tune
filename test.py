import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  # model="davinci",
  # model="text-davinci-003",
  # model="davinci:ft-meshlake-inc-2023-06-13-04-49-07",
  # model="davinci:ft-meshlake-inc-2023-06-13-12-08-36",
  model="davinci:ft-meshlake-inc-2023-06-15-04-39-19",
  prompt="我需要统计订单退款表中所有退款成功的金额，请使用 mysql 的语法帮我写出SQL语句",
  # stop="\n",
  temperature=0.6,
  max_tokens=500,
)

print(response)
print(response.choices[0].text)

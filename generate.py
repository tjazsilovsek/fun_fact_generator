import openai


def parse_prompt(text: str) -> list[tuple[str, str]]:
    parsed_list = []
    data = text.split('\n\n')
    for d in data:
        lines = d.split('\n', 1)
        if len(lines) < 2:
            continue
        name = lines[0]
        content = lines[1].strip()
        parsed_list.append((name, content))
    return parsed_list


def generate_prompt(prompt: str) -> list[tuple[str, str]]:
    system_message = "You are content creator now.\n \
        Try to be humorous and creative.\n \
        You will recieve a prompt to generate a list of items with some properties.\n \
        For example, 5 biggest land animals.\n \
        You will return only important information, in animal example, you will return animal name and than in new line some info of it.\n \
        You must return items separated by empty lines and for item and its property must be in separate lines.\n \
        You should return only that and nothing more. Again, items must be separeted with new lines!\n \
        Here is your prompt:\n"

    prompt = system_message + prompt

    text = generate_text(prompt)
    print(text)
    return parse_prompt(text)


def generate_text(prompt) -> str:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


# prompt = "You are content creator now.\n \
# You will recieve a prompt to generate a list of items with some properties.\n \
# For example, 5 biggest land animals.\n \
# You will return only important information, in animal example, you will return animal name and than in new line some info of it.\n \
# You must return items separated by empty lines and for item and its property must be in separate lines.\n \
# You should return only that and nothing more. Again, items must be separeted with new lines!\n \
# Here is your prompt: "

# prompt += "6 longest rivers in the worl."
# generated_text = generate_text(prompt)
# print(generated_text)

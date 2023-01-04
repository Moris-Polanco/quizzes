import openai
import streamlit as st
import os

# Set up the OpenAI API client
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_questions(text):
    # Use the OpenAI API to generate questions based on the input text
    prompt = (f"Generate multiple choice questions based on the following text:\n{text}")
    model_engine = "text-davinci-003"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated questions and options from the API response
    questions = []
    for completion in completions.choices[0].text.split("\n"):
        if completion.startswith("Q: "):
            question = completion[3:]
            options = []
        elif completion.startswith("A: "):
            options.append(completion[3:])
        elif completion.startswith("Correct answer: "):
            correct_answer = completion[16:]
            questions.append({"question": question, "options": options, "correct_answer": correct_answer})

    return questions


def evaluate_answer(question, answer):
    return question["correct_answer"] == answer


text = "El año 2020 fue el año del COVID-19, una enfermedad respiratoria causada por el coronavirus SARS-CoV-2. Se estima que la enfermedad se originó en un mercado en la ciudad china de Wuhan a finales de 2019 y se extendió rápidamente a nivel mundial. Los síntomas incluyen fiebre, tos y dificultad para respirar, y pueden ser leves o graves. La enfermedad se propaga principalmente de persona a persona a través de gotas respiratorias producidas cuando una persona infectada habla, tose o estornuda."

questions = generate_questions(text)

for i, question in enumerate(questions):
    print(f"{i + 1}. {question['question']}")
    for j, option in enumerate(question["options"]):
        print(f"  {j + 1}. {option}")
    answer = input("Enter the number of the correct answer: ")
    if evaluate_answer(question, answer):
        print("Correct!")
    else:
        print("Incorrect. The correct answer was:", question["correct_answer"])

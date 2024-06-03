from utilities import *
import ollama

def question(name, questionText):
    config = getConfigYaml()
    model = config['ollama_model']
    ollama.pull(model)

    response = ollama.chat(
        model=model,
        messages= [
            {
                "role": "user",
                "content": f"Respond as if you are {name} in {config['max_response_words']} words or less to the following. {questionText}"
            }
        ],
    )
    return response["message"]["content"]

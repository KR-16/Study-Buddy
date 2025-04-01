from load_model import load_llm
import json

llm = load_llm()

def generate_qna(text, num_questions = 10):
    """
    Generate the Q&A pairs from the text
    """

    prompt = f"""Generate {num_questions} concise questions - answer pairs from your understanding of the text: 
    {text[:3000]} 
    Return as JSON with Keys: questions, answer, topic"""

    response = llm(
        prompt,
        max_tokens = 2000,
        temperature = 0.7
    )

    try:
        return json.loads(response["choices"][0]["text"])
    except json.JSONDecodeError:
        return {"error" : "Failed to parse response"}
if __name__ == "__main__":
    qna = generate_qna()
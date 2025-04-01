from llama_cpp import Llama
import time

def load_llm():
    """
    Load the Model from the model directory
    """
    print("Loading Model...")
    start = time.time()

    llm = Llama(
        model_path = ".\model\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        n_ctx = 2048,               # context window size
        n_thrreads = 8,             # CPU cores (set to your core count)
        n_gpu_layers = 20           # Offload layers to GPU (if available)
    )

    print(f"Model loaded in {time.time() - start:.2f}s | Max Tokens: {llm.context_params.n_ctx}")
    return llm

if __name__ == "__main__":
    llm = load_llm()
    test_response = llm("Explain the process in hydrations to a 5 year old kid")
    print(test_response["choice"][0]["text"])
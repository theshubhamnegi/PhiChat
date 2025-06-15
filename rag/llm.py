from llama_cpp import Llama

models_paths = "llm_model/Phi-3-mini-4k-instruct-q4.gguf"
llm = Llama(model_path=models_paths, n_ctx=4096, n_threads=4)

def query_phi(prompt: str) -> str:
    full_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
    output = llm(full_prompt, max_tokens=1024, stop=["<|user|>"], echo=False)
    return output["choices"][0]["text"].strip()
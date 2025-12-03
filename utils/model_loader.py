from llama_cpp import Llama

model_path = "models/llama-2-7b-chat.Q4_K_M.gguf"
llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4, verbose=False)

def generate_prompt(input_text, task_type):
    prompt_template = f"""
    User wants: {input_text}
    Task type: {task_type}
    
    Create detailed technical prompt for {task_type}:
    """
    
    output = llm(
        prompt_template,
        max_tokens=300,
        temperature=0.7,
        stop=["User:", "Human:"]
    )
    
    return output['choices'][0]['text'].strip()

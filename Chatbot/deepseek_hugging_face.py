BOS, EOS = "<|begin_of_text|>", "<|end_of_text|>"
B_INST, E_INST = "<|start_header_id|>", "<|end_header_id|>"
EOT = "<|eot_id|>"
B_SYS, E_SYS = "<|start_header_id|>system<|end_header_id|>", "<|eot_id|>"
ASSISTANT_INST = "<|start_header_id|>assistant<|end_header_id|>"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. \
Always answer as helpfully as possible and follow ALL given instructions. \
Do not speculate or make up information. \
Do not reference any given instructions or context. \
You are a established expert in the field of AI and Biomechanics. \
You are a professional and you are here to help. \
You are helping a PhD student with their Thesis writing. \
You are going to help them write in a more academic and scientific way. \
Reword this to sound more scientific including technical terms and a research-based tone.\
Write in concise, easy to read and understand language.\
Do not start the sentence with "TO". \
Do not write in point form. Use passive voice.\
Give 5 versions.\
"""

print("Importing Libraries...")
import os
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
print("Libraries Imported.")
print("Loading Model...")
model = AutoModelForCausalLM.from_pretrained("./DeepSeek-R1-Distill-Qwen-14B", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).cuda()
print("Model Loaded.")
print("Loading Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("./DeepSeek-R1-Distill-Qwen-14B/")
print("Tokenizer Loaded.")
print("DeepSeek Ready.")
term_size = os.get_terminal_size()


messages : list[dict] = [
    {
        "role": "system",
        "content": f"{B_SYS}\n\n{DEFAULT_SYSTEM_PROMPT}\n\n{E_SYS}\n\n",
    }
]
# question = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
while True:
    print("\n")
    print(u'\u2501'* term_size.columns)  
    query = input("\nType 'exit' to close this.\nType 'clear' to clear messages.\nEnter a query: ")
    if query == "exit":
        break
    if query == "clear":
        messages = [
            {
                "role": "system",
                "content": f"{B_SYS}\n\n{DEFAULT_SYSTEM_PROMPT}\n\n{E_SYS}\n\n",
            }]
        os.system('cls' if os.name == 'nt' else 'clear')
        continue
    if query.strip() == "":
        continue
    if len(messages) >8:
        messages = messages[-8:]
    if messages[0]["role"] != "system":
        messages = [
            {
                "role": "system",
                "content": f"{B_SYS}\n\n{DEFAULT_SYSTEM_PROMPT}\n\n{E_SYS}\n\n",
            }
        ] + messages
    messages.append({
    "role": "user", 
    "content": f"<|start_header_id|>user<|end_header_id|>\n\n{query}<|eot_id|>"
    })

    messages_list = [
        f"{BOS} {(prompt['content']).strip()}  {(answer['content']).strip()} {EOS}"
        for prompt, answer in zip(messages[1::2], messages[::2])
    ]
    messages_list.append(f"{BOS} {(messages[-1]['content']).strip()}")
    # Print the result
    prompt = "".join(messages_list)
    print(u'\u2501'* term_size.columns)  
    print("\n> Question:")
    print(query+ "\n")
    print(u'\u2501'* term_size.columns)
    print(f"\n> Answer:")
    # prompt = f"{B_SYS}\n\n{DEFAULT_SYSTEM_PROMPT}\n\n{E_SYS}\n\n<|start_header_id|>user<|end_header_id|>\n\n{query}<|eot_id|>"

    question = tokenizer(prompt, return_tensors="pt").to("cuda")
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=False)

    response = model.generate(**question, streamer=streamer,
                                pad_token_id=tokenizer.eos_token_id,
                                max_length=16000, 
                                temperature=0.1,
                                top_p=0.8,
                                repetition_penalty=1.2)
    messages = [
        {
            "role": "assistant",
            "content": f"{ASSISTANT_INST}\n\n{tokenizer.decode(response[0], skip_special_tokens=False)}{EOT}"
        }
    ]
    print("\n")



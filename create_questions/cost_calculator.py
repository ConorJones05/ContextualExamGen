from pydantic import BaseModel
import tiktoken 


class Model_Pricing(BaseModel):
    input: float
    output: float
    cached_input: float | None

CACHED_INPUT_TOKEN_CUTOFF = 1024
MILLION_TOKENS = 1000000
BATCH_DISCOUNT = 2
    
model_costs: dict[str, Model_Pricing] = {
    "gpt-4-turbo": Model_Pricing(input = 10, output = 30, cached_input = None),
    "gpt-4": Model_Pricing(input = 30.00, output = 60.00, cached_input = None),
    "gpt-3.5-turbo": Model_Pricing(input = 0.5, output = 1.5, cached_input = None),
    "gpt-4.1": Model_Pricing(input = 2.00, output = 8.0, cached_input = 0.5),
    "gpt-4.1-mini": Model_Pricing(input = 0.40, output = 1.6, cached_input = 0.1),
    "gpt-4.1-nano": Model_Pricing(input = 0.10, output = 0.4, cached_input = 0.025),
    "gpt-4o": Model_Pricing(input = 2.5, output = 10, cached_input = 1.25)
    #  TODO: add gemni and more models
}

def count_tokens_single_code(model: str, code: str) -> tuple[int, int] :
    """Find the amount of input tokens for a chunk of code"""
    if model[:2] in 'gpt':
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(code))
        if num_tokens > CACHED_INPUT_TOKEN_CUTOFF:
            return num_tokens, num_tokens - CACHED_INPUT_TOKEN_CUTOFF
        return num_tokens, 0
    
def calculate_estimated_cost(model: str, student_code_dict: dict[str, str], intital_prompt: str, batch: bool = True) -> float:
    if model not in model_costs.values():
        raise ValueError("model not in the list of availble models please enter a correct model")
    
    input_tokens: dict[int, int] = {"input_tokens": 0, "cached_input": 0}

    for student_code in student_code_dict.items():
        tokens, cached = count_tokens_single_code(model, student_code)
        input_tokens["input_tokens"] += tokens
        input_tokens["cached_input"] += cached
    
    pricing = model_costs[model]

    if not batch and pricing.cached_input is not None:
        cost = (
            input_tokens["input_tokens"] - input_tokens["cached_input"]
        ) * (pricing.input / MILLION_TOKENS) + input_tokens["cached_input"] * (pricing.cached_input / MILLION_TOKENS)
    elif batch:
        cost = (input_tokens["input_tokens"] * (pricing.input / MILLION_TOKENS))/BATCH_DISCOUNT

    else:
        cost = input_tokens["input_tokens"] * (pricing.input / MILLION_TOKENS)

    cost += intital_prompt * (pricing.input / MILLION_TOKENS)

    cost += OUTPUT_TOKEN_MAX * (pricing)

    return round(cost, 2)
        



    
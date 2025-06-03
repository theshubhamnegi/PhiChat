# Error Message
Model output is irrelevant or abruptly cut off

## Root Cause of the Error
Prompts sent to the language model were either too long and exceeded the model's context window or lacked structure, causing the model to generate poor or incomplete responses.

## Different Approaches Tried Out
**First Approach**:
- Increased the n_ctx value to allow for longer prompts but still observed erratic behavior with large inputs.

**Second Approach**:
- Introduced prompt truncation logic and better formatting, ensuring that the prompt fits within the model’s context size while providing the most relevant context.

## Selected Approach and Why?
Implemented prompt trimming and structured formatting to stay within the model's n_ctx limit.

**Reason for Selection**:
- Reduces the risk of cutoff outputs or broken completions by respecting token limits.

- Ensures that the language model receives the most useful information without being overloaded.

## Result
Prompt responses are now coherent, relevant, and complete. The LLM consistently provides high-quality answers with RAG context.
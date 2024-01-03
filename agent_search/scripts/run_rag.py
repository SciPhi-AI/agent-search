import json

import fire

PROMPT = """
### Instruction:

Query:
{query}

Search Results:
{rag_context}

Query:
{query}

### Response:
{{"response":
"""

PROMPT = """
### Instruction:

Query:
{query}

Search Results:
{rag_context}

Query:
{query}

### Response:
{{"response":
"""


class RagDemo:
    """A demonstration of Bing + synthesizer RAG pipeline."""

    def __init__(self):
        try:
            import synthesizer
        except ImportError as e:
            raise ImportError(
                f"Demo run_rag.py failed with {e}. Please run pip install sciphi-synthesizer before attempting to run this script."
            )

    def run(
        self,
        query="What is a quantum field theory in curved space time?",
        # Bing RAG provider settings
        rag_provider_name="bing",
        rag_api_base="https://api.bing.microsoft.com/v7.0/search",
        # llm parameters
        llm_provider_name="sciphi",
        llm_model_name="SciPhi/Sensei-7B-V1",
        llm_max_tokens_to_sample=1_024,
        llm_temperature=0.2,
        llm_top_p=0.90,
    ):
        from synthesizer.core import LLMProviderName, RAGProviderName
        from synthesizer.interface import (
            LLMInterfaceManager,
            RAGInterfaceManager,
        )
        from synthesizer.llm import GenerationConfig

        # Initialize Bing RAG Interface with its configuration
        rag_interface = RAGInterfaceManager.get_interface_from_args(
            provider_name=RAGProviderName(rag_provider_name),
            api_base=rag_api_base,
        )
        rag_result = rag_interface.get_rag_context(query)

        # LLM Provider Settings
        llm_interface = LLMInterfaceManager.get_interface_from_args(
            LLMProviderName(llm_provider_name),
        )

        generation_config = GenerationConfig(
            model_name=llm_model_name,
            max_tokens_to_sample=llm_max_tokens_to_sample,
            temperature=llm_temperature,
            top_p=llm_top_p,
            # other generation params here ...
        )

        formatted_prompt = PROMPT.format(
            rag_context=rag_result.context, query=query
        )
        completion = '{"response":' + llm_interface.get_completion(
            formatted_prompt, generation_config
        ).replace("</s>", "")

        print(
            f"Search Results:\n{rag_result.meta_data}"
            + f"\nPrompt:\n{formatted_prompt}\n\n"
            + "-" * 100
            + f"\nCompletion:\n{json.loads(completion)}"
        )


if __name__ == "__main__":
    fire.Fire(RagDemo)

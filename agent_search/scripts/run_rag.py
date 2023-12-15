import fire


class RagDemo:
    """A demonstration of agent-search + synthesizer RAG pipeline."""

    def __init__(self):
        try:
            import synthesizer
        except ImportError as e:
            raise ImportError(
                f"Demo run_rag.py failed with {e}. Please run pip install sciphi-synthesizer before attempting to run this script."
            )

    def run(
        self,
        query="What is Fermat's last theorem?",
        rag_prompt="Your task is to use the context which follows to answer the question with a two paragraph line-item cited response:\n{rag_context}\nBegin your two paragraph answer with line-item citations now:",
        # rag parameters
        rag_provider_name="agent-search",
        rag_api_base="https://api.sciphi.ai",
        rag_limit_hierarchical_url_results="25",
        rag_limit_final_pagerank_results="10",
        # llm parameters
        llm_provider_name="openai",
        llm_model_name="gpt-3.5-turbo",
        llm_max_tokens_to_sample=256,
        llm_temperature=0.1,
        llm_top_p=0.95,
    ):
        from synthesizer.core import LLMProviderName, RAGProviderName
        from synthesizer.interface import (
            LLMInterfaceManager,
            RAGInterfaceManager,
        )
        from synthesizer.llm import GenerationConfig

        # RAG Provider Settings
        rag_interface = RAGInterfaceManager.get_interface_from_args(
            RAGProviderName(rag_provider_name),
            api_base=rag_api_base,
            limit_hierarchical_url_results=rag_limit_hierarchical_url_results,
            limit_final_pagerank_results=rag_limit_final_pagerank_results,
        )
        rag_context = rag_interface.get_rag_context(query)

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

        formatted_prompt = rag_prompt.format(rag_context=rag_context)
        completion = llm_interface.get_completion(
            formatted_prompt, generation_config
        )
        print(completion)

        ### Output:
        # Fermat's Last Theorem was proven by British mathematician Andrew Wiles in 1994 (Wikipedia). Wiles's proof was based on a special case of the modularity theorem for elliptic curves, along with Ribet's theorem (Wikipedia). The modularity theorem and Fermat's Last Theorem were previously considered inaccessible to proof by contemporaneous mathematicians (Wikipedia). However, Wiles's proof provided a solution to Fermat's Last Theorem, which had remained unproved for over 300 years (PlanetMath). Wiles's proof is widely accepted and has been recognized with numerous awards, including the Abel Prize in 2016 (Wikipedia).

        # It is important to note that Wiles's proof of Fermat's Last Theorem is a mathematical proof and not related to the science fiction novel "The Last Theorem" by Arthur C. Clarke and Frederik Pohl (Wikipedia). The novel is a work of fiction and does not provide a real mathematical proof for Fermat's Last Theorem (Wikipedia). Additionally, there have been other attempts to prove Fermat's Last Theorem, such as Sophie Germain's approach, but Wiles's proof is the most widely accepted and recognized (Math Stack Exchange).


if __name__ == "__main__":
    fire.Fire(RagDemo)

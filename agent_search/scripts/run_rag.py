
if __name__ == "__main__":
    try:
        import synthesizer
    except ImportError as e:
        raise ImportError("run_rag.py failed with {e}. Please run pip install sciphi-synthesizer before attempting to run this script.")
    from synthesizer.core import LLMProviderName, RAGProviderName
    from synthesizer.interface import LLMInterfaceManager, RAGInterfaceManager
    from synthesizer.llm import GenerationConfig

    num_paragraphs = "two"
    prompt = f"Your task is to use the context which follows to answer the question with a {num_paragraphs} paragraph line-item cited response:\n{{rag_context}}\nBegin your {num_paragraphs} paragraph answer with line-item citations now:"
    # RAG Provider Settings
    rag_interface = RAGInterfaceManager.get_interface_from_args(
        RAGProviderName("agent-search"),
        api_base="http://localhost:8002",
        limit_hierarchical_url_results=25,
        limit_final_pagerank_results=10,
    )
    rag_context = rag_interface.get_rag_context("What is Fermat's last theorem?")

    # LLM Provider Settings
    llm_interface = LLMInterfaceManager.get_interface_from_args(
        LLMProviderName( "openai"),
    )

    generation_config = GenerationConfig(
        model_name="gpt-3.5-turbo",#-instruct",
        max_tokens_to_sample=256,
        temperature = 0.1,
        top_p = 0.95, 
        # other generation params here ...
    )

    formatted_prompt = prompt.format(rag_context=rag_context)
    completion = llm_interface.get_completion(
        formatted_prompt, generation_config
    )
    print(completion)
    ### Output:
    # Fermat's Last Theorem was proven by British mathematician Andrew Wiles in 1994 (Wikipedia). Wiles's proof was based on a special case of the modularity theorem for elliptic curves, along with Ribet's theorem (Wikipedia). The modularity theorem and Fermat's Last Theorem were previously considered inaccessible to proof by contemporaneous mathematicians (Wikipedia). However, Wiles's proof provided a solution to Fermat's Last Theorem, which had remained unproved for over 300 years (PlanetMath). Wiles's proof is widely accepted and has been recognized with numerous awards, including the Abel Prize in 2016 (Wikipedia).

    # It is important to note that Wiles's proof of Fermat's Last Theorem is a mathematical proof and not related to the science fiction novel "The Last Theorem" by Arthur C. Clarke and Frederik Pohl (Wikipedia). The novel is a work of fiction and does not provide a real mathematical proof for Fermat's Last Theorem (Wikipedia). Additionally, there have been other attempts to prove Fermat's Last Theorem, such as Sophie Germain's approach, but Wiles's proof is the most widely accepted and recognized (Math Stack Exchange).

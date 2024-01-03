# AgentSearch [ΨΦ]: A powerful search agent client and search engine.

![AgentSearch Banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713)

This framework facilitates seamless integration with the AgentSearch dataset or hosted search APIs (`e.g. Search Engines`) and with RAG-specialized LLM's (`e.g. Search Agents`).

## Features of AgentSearch
- **Search Agent**: Seamless integration with any RAG-specialized LLM, such as [Sensei-7B](https://huggingface.co/SciPhi/Sensei-7B-V1).
- **Customizable Search**: Deploy your own local search engine with the [AgentSearch dataset](https://huggingface.co/datasets/SciPhi/AgentSearch-V1). Or, introduce your own custom datasets to meet your specific needs.
- **API Endpoint**: Connect with SciPhi and other search provider APIs for easy deployment.

## Quickstart Guide for AgentSearch

### Install the AgentSearch Client

```shell
pip install agent-search
```

### Execute a Search

1. Register for a free API key at [SciPhi](https://www.sciphi.ai/).
2. Use the following bash command to run a search query:

```shell
export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
python -m agent_search.scripts.run_search run --query="What is Fermat's last theorem?"
```

This will output results like the following:

```output
1. URL: https://en.wikipedia.org/wiki/Fermat's_last_theorem (Score: 0.89)
--------------------------------------------------
Title: Fermat's Last Theorem
Text:
The case p = 3 was first stated by Abu-Mahmud Khojandi (10th century), but his attempted proof of the theorem was incorrect.[62] In 1770, Leonhard Euler gave a proof of p = 3,[63] but his proof by infinite descent[64] contained a major gap.[65] However, since Euler himself had proved the lemma necessary to complete the proof in other work, he is generally credited with the first proof.[66] Independent proofs were published[67] by Kausler (1802),[37] Legendre (1823, 1830),[39][68] Calzolari (1855),[69] Gabriel Lamé (1865),[70] Peter Guthrie Tait (1872),[71] Günther (1878),[72][full citation needed] Gambioli (1901),[48] Krey (1909),[73][full citation needed] Rychlík (1910),[53] Stockhaus (1910),[74] Carmichael (1915),[75] Johannes van der Corput (1915),[76] Axel Thue (1917),[77][full citation needed] and Duarte (1944).[78] The case p = 5 was proved[79] independently by Legendre and Peter Gustav Lejeune Dirichlet around 1825.[80] Alternative proofs were developed[81] by Carl Friedrich Gauss (1875,
...
```

For further information, you may refer to the [documentation](https://agent-search.readthedocs.io/en/latest/).

### Execute a RAG response

- To generate a rag response with the hosted AgentSearch API:

```shell
# Install SciPhi's synthesizer package -
pip install sciphi-synthesizer

# Setup environment
export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
# Use the SciPhi `Sensei-7B` for LLM RAG w/ Bing
python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?"

# Use OpenAI `gpt-3.5-turbo` for LLM RAG w/ AgentSearch
export OPENAI_API_KEY=MY_OPENAI_KEY
python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo --rag_provider_name="agent-search" --rag_api_base="https://api.sciphi.ai"
```

Resulting output:

```output
{'summary': "\nFermat's Last Theorem is a landmark statement in number theory, asserting that for any integer value of n greater than 2, the equation \\(x^n + y^n = z^n\\) has no solutions in positive integers x, y, and z [1][2]. This theorem has intrigued mathematicians for centuries, with the initial claim made by Pierre de Fermat in the 17th century. Fermat himself provided proofs for the cases n=4 and n=3, and partial proofs for other smaller values of n [16]. However, it was not until the late 20th century that the theorem was fully proven for all values of n greater than 2, thanks to the work of mathematician Andrew Wiles [7].\n\nThe proof of Fermat's Last Theorem has had a profound impact on mathematics, leading to significant advancements in the field. It has been described as one of the most difficult problems in the history of mathematics, and its resolution marked a major milestone in the understanding of number theory [10]. The proof itself has been recognized with prestigious awards, including the 2016 Abel Prize for Andrew Wiles, highlighting its importance and the depth of mathematical thought required to solve it [7].\n\nIn summary, Fermat's Last Theorem is a fundamental result in number theory, confirming a conjecture that had stumped mathematicians for over three centuries. The theorem's proof not only resolved a long-standing mathematical mystery but also catalyzed new developments within the discipline [1][2][7][10].\n\n", 'other_queries': ["Historical impact of Fermat's Last Theorem", "Explanation of Andrew Wiles' proof", "Significance of Fermat's Last Theorem in modern mathematics", 'The role of the modularity conjecture in the proof', "Advancements in number theory post-Fermat's Last Theorem"], ...SEARCH_RESULTS...}
```

This output is a JSON ready format which can be parsed in Python, for ex., by calling `json.loads(completion)`. The output will be a JSON object with keys `summary` and `other_queries`.


### Code your own search RAG workflow

```python
# Requires SCIPHI_API_KEY in env
from agent_search import SciPhi

client = SciPhi()
rag_response = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
print(rag_response)
# { 'response': '...', 'other_queries': '...', 'search_results': '...' }
```
---

### Community & Support

- Engage with the community on [Discord](https://discord.gg/j9GxfbxqAe).
- For tailored inquiries or feedback, please [email us](mailto:owen@sciphi.ai).

### Local AgentSearch Setup and Initialization

For self-hosting, follow the steps below.

#### Prerequisites

Ensure Docker and Postgres are installed on your system. 
- [Download Docker here](https://www.docker.com/).
- [Download Postgres here](https://www.postgresql.org/download/).

#### Steps:

1. **Launch Postgres Database**:
   - Start the Postgres service on your system:
     ```shell
     # Command to start Postgres, adjust based on your system's configuration
     sudo service postgresql start
     ```
   - This step ensures that the Postgres database is running and ready to be populated.

2. **Relational Database Population**:
   - Command to populate the Postgres database:
     ```shell
     python -m agent_search.scripts.populate_postgres_from_hf run
     ```
   - This script populates a postgres database with the parameters from `config.ini`, adaptable to custom datasets. For help directly istalling the full 4TB postgres database, contact [our team](mailto:owen@sciphi.ai).

3. **Start Qdrant Service with Docker**:
   - Run the Qdrant service in Docker:
     ```shell
     docker run -p 6333:6333 -p 6334:6334 \
         -v $(pwd)/qdrant_storage:/qdrant/storage:z \
         qdrant/qdrant
     ```
   - For Qdrant installation guidance, see [Qdrant Documentation](https://qdrant.tech/documentation/quick-start/).

4. **Vector Database Population**:
   - Populate the Vector database:
     ```shell
     python -m agent_search.scripts.populate_qdrant_from_postgres run --delete_existing=True
     ```
   - This step prepares a qdrant database with the parameters from `config.ini`. For direct installation assistance, contact [our team](mailto:owen@sciphi.ai).

5. **Run the Server**:
   - Launch the AgentSearch server:
     ```shell
     python -m agent_search.app.server
     ```

### Additional Notes

- Execute all commands from the root directory of the AgentSearch project.
- Replace `query` in the run command with your search query.
- Check back soon for our User Guide. 
<!-- [User Guide](link-to-user-guide). -->
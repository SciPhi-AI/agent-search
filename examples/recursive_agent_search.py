import os
from agent_search import SciPhi

client = SciPhi(api_key=os.environ.get("SCIPHI_API_KEY"))

breadth = 1
depth = 3
query = "Conservatism"

# Generate a completion
def generate_answer(query):
    completion = client.get_search_rag_response(query=query, search_provider='agent-search')
    return completion

def recursive_search(query, depth, breadth):
    initial_completion = generate_answer(query)
    responses = [(initial_completion['response'], initial_completion['related_queries'][:breadth])]

    for _ in range(depth - 1):
        new_related_queries = []
        for item in responses[-1][1]:
            further_completion = generate_answer(item)
            if isinstance(further_completion, dict) and 'response' in further_completion:
                new_related = further_completion['related_queries'][:breadth]
                responses.append((further_completion['response'], new_related))
                new_related_queries.extend(new_related)
            else:
                print(f"Unexpected format for further_completion: {further_completion}")
        responses[-1] = (responses[-1][0], new_related_queries)

    for response, related in responses:
        print(response)
        print("*" * 10)
        print("Related queries:", related)
        print("*" * 10)

# Run 3 iterations deep and use 1 related query per iteration
recursive_search(query=query, depth=depth, breadth=breadth) # Specify depth (3) and breadth (1) here

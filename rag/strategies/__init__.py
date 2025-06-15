from rag.strategies import basic, rerank, query_rewrite, multiquery, llm_only

strategy_map = {
    "llm_only": llm_only.run,
    "basic": basic.run,
    "rerank": rerank.run,
    "query_rewrite": query_rewrite.run,
    "multiquery": multiquery.run,
}

def run_rag_strategy(question, strategy, embedder, collection, request_id=None):
    strategy_fn = strategy_map.get(strategy.lower())
    if not strategy_fn:
        raise ValueError(f"Invalid strategy: {strategy}")
    return strategy_fn(question, embedder, collection, request_id)
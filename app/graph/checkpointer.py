from langgraph.checkpoint.sqlite import SqliteSaver


CHECKPOINT_DB = "langgraph_checkpoints.db"

checkpointer_context = SqliteSaver.from_conn_string(
    CHECKPOINT_DB
)

checkpointer = checkpointer_context.__enter__()
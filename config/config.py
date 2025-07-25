import json
from pathlib import Path

# Load JSON config file
def load_config(path="config/Config.json"):
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(config_path, "r") as f:
        return json.load(f)

# Load config
_config = load_config()

# Parse and expose values as constants
DB_USER = _config["db_params"]["db_username"]
DB_DSN = _config["db_params"]["db_dsn"]
DB_PASSWORD_PATH = _config["db_params"]["db_password_path"]

INDEX_PATH = _config["embedding_params"]["index_path"]
META_PATH = _config["embedding_params"]["meta_path"]
EMBEDDING = _config["embedding_params"]["model"]
TOPK = _config["embedding_params"]["top_k"]

LLM = _config["LLM_params"]["LLM"]
OPENAI_PATH = _config["LLM_params"]["openaiPath"]
DS_PATH = _config["LLM_params"]["dsPath"]

EVAL_RES = _config["eval_params"]["resultPath"]
SAMPLE_NUM = _config["eval_params"]["sample_number"]


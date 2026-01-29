from huggingface_hub import list_repo_files

# Exemplo para um repositório de dataset
repo_id = "megagonlabs/subjqa"
repo_type = "dataset" # Opções: "model", "dataset", "space"

# Lista todos os arquivos
files = list_repo_files(repo_id=repo_id, repo_type=repo_type)

for file in files:
    print(f"Arquivo: {file}, Tipo: {repo_type}")
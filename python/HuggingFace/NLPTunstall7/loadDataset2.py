from huggingface_hub import hf_hub_download

# Exemplo: Baixando um arquivo CSV específico de um repositório
file_path = hf_hub_download(
    repo_id="megagonlabs/subjqa",
    filename="data.zip",
    repo_type="dataset"
)
print(f"Arquivo baixado em: {file_path}")
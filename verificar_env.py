# verificar_env.py
import os

env_file_path = os.path.join("alembic", "env.py")
print(f"--- Verificando o arquivo: {os.path.abspath(env_file_path)} ---")

try:
    with open(env_file_path, "r", encoding="utf-8") as f:
        primeiras_linhas = f.readlines(5) # Ler as primeiras 5 linhas
        print(f"Primeiras {len(primeiras_linhas)} linhas do arquivo '{env_file_path}':")
        for i, linha in enumerate(primeiras_linhas):
            print(f"Linha {i+1}: {linha.strip()}") # .strip() para remover quebras de linha extras

        # Verifica se a nossa linha de debug específica está lá
        f.seek(0) # Volta ao início do arquivo para ler o conteúdo completo
        conteudo_completo = f.read()
        if "!!!! TOPO DO ENV.PY FOI ALCANÇADO !!!!" in conteudo_completo:
            print("\nCONFIRMADO: A linha de debug '!!!! TOPO DO ENV.PY FOI ALCANÇADO !!!!' está presente no arquivo.")
        else:
            print("\nALERTA: A linha de debug '!!!! TOPO DO ENV.PY FOI ALCANÇADO !!!!' NÃO FOI ENCONTRADA no arquivo.")

except FileNotFoundError:
    print(f"ERRO: O arquivo '{env_file_path}' não foi encontrado no caminho esperado.")
except Exception as e:
    print(f"ERRO ao ler o arquivo '{env_file_path}': {e}")

print("--- Fim da verificação ---")
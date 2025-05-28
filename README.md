# Dieta-Calorias

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-%5E0.95-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

## 🎯 Descrição

**Dieta-Calorias** é uma API RESTful construída com FastAPI e SQLAlchemy para gerenciar usuários, alimentos, refeições e calcular calorias diárias. Permite operações de CRUD completas e conta com uma calculadora de calorias por item, refeição e dia.

## 📹 Demonstração em Vídeo

* Link do vídeo (resolução máxima 1280×720): 

## ✅ Funcionalidades já implementadas

* **Usuários**: criação, leitura, atualização e remoção.
* **Alimentos**: cadastro, consulta, atualização e exclusão.
* **Itens de Refeição**: adicionar alimento à refeição, atualizar quantidade e remover.
* **Refeições**: criação, leitura, atualização e remoção, relacionando itens.
* **Calculadora de Calorias**:

  * Calcular calorias de um item (quantidade × calorias por 100g).
  * Calcular calorias totais de uma refeição.
  * Calcular calorias consumidas em um dia por usuário.
  * Validar consumo diário em relação à meta.
* **Testes**: suíte completa com pytest cobrindo CRUD e cálculos.

## 🚀 Tecnologias

* Python 3.13
* FastAPI
* SQLAlchemy
* SQLite (padrão)
* pytest

## 📦 Estrutura do Projeto

```text
dieta-calorias/
├── src/
│   ├── api/
│   │   └── routers/     # Endpoints FastAPI
│   ├── crud/            # Lógica de acesso a dados
│   ├── database.py      # Configuração do SQLAlchemy
│   ├── main.py          # Inicialização da aplicação
│   └── models.py        # Definições de tabelas
├── tests/               # Testes unitários e de integração
├── README.md            # Documentação do projeto
└── requirements.txt     # Dependências
```

## ⚙️ Instalação e Uso

1. Clone o repositório:

   ```bash
   git clone https://github.com/PatoCareca1/dieta-calorias.git
   cd dieta-calorias
   ```
2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
3. Rode a API:

   ```bash
   uvicorn src.main:app --reload
   ```
4. Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`

### Utilizando o Swagger UI

No Swagger você poderá visualizar, testar e interagir com todos os endpoints (rotas) disponíveis.

## Exemplo prático para CRUD de Usuários:

# Criar um Usuário

Procure pelo grupo /usuarios/.

Clique em POST /usuarios/

Clique em Try it out (Experimentar).

Preencha os campos do corpo da requisição (nome, email, senha, peso, altura, meta_calorica_diaria).

Clique em Execute.

# Consultar um Usuário

Clique em GET /usuarios/{user_id}.

Preencha o user_id do usuário que deseja consultar.

Clique em Execute.

# Atualizar um Usuário

Clique em PUT /usuarios/{user_id}.

Preencha o user_id do usuário.

No corpo, insira os dados que deseja atualizar.

Clique em Execute.

# Excluir um Usuário

Clique em DELETE /usuarios/{user_id}.

Insira o user_id do usuário a ser removido.

Clique em Execute.

## CRUD para outros recursos

O mesmo procedimento pode ser feito para Alimentos, Refeições e Itens de Refeição.
Basta localizar o grupo de endpoints correspondente no Swagger UI.

## Dicas

O Swagger mostra exemplos automáticos de entrada e saída dos dados.

Todas as rotas exibem possíveis códigos de resposta (sucesso, erro de validação, etc).

Ótimo para testar manualmente sem precisar de outra ferramenta (Postman, Thunder Client).

## 🧪 Testes

Execute a suíte de testes com:

```bash
pytest -v
```

## 📋 O que falta implementar (3ª unidade)

* Interface web (frontend) para interação visual.
* Autenticação e autorização (JWT).
* Deploy em nuvem (Heroku, AWS, etc.).
* Relatórios e gráficos de consumo.
* Otimizações de performance e documentação extendida.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch feature: `git checkout -b feature/nova-funcionalidade`
3. Faça commit das suas alterações: `git commit -m 'feat: descrição da alteração'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Contato

* **Autor**: Lucas Daniel Costa Souza([@PatoCareca1](https://github.com/Patocareca1/dieta-calorias))
* **Email**: [LucasDan16@outlook.com](mailto:LucasDan16@outlook.com)

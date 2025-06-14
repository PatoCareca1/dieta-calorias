# src/services/diet_calculator.py
from datetime import date
from src import models

# Fatores de atividade (padrão, baseados em Harris-Benedict)
FATORES_ATIVIDADE = {
    "sedentario": 1.2,
    "levemente_ativo": 1.375,
    "moderadamente_ativo": 1.55,
    "muito_ativo": 1.725,
    "extremamente_ativo": 1.9,
}

def calcular_plano_alimentar(user: models.Usuario) -> dict:
    """
    Calcula TMB (Taxa Metabólica Basal), calorias e macros para um usuário
    com base nos dados do seu perfil.
    Usa a fórmula de Harris-Benedict revisada.
    """
    # 1. Validar se temos os dados necessários
    if not all([user.data_nascimento, user.peso_kg, user.altura_cm, user.genero, user.nivel_atividade, user.objetivo]):
        raise ValueError("Dados de perfil insuficientes para o cálculo (requer: nascimento, peso, altura, gênero, nível de atividade, objetivo).")

    # 2. Calcular Idade
    hoje = date.today()
    idade = hoje.year - user.data_nascimento.year - ((hoje.month, hoje.day) < (user.data_nascimento.month, user.data_nascimento.day))

    # 3. Calcular TMB (Taxa Metabólica Basal) - Harris-Benedict Revisada
    if user.genero.value == "masculino":
        tmb = 88.362 + (13.397 * user.peso_kg) + (4.799 * user.altura_cm) - (5.677 * idade)
    elif user.genero.value == "feminino":
        tmb = 447.593 + (9.247 * user.peso_kg) + (3.098 * user.altura_cm) - (4.330 * idade)
    else: # Usa uma média como fallback para "outro" ou "prefiro_nao_dizer"
        tmb_masculino = 88.362 + (13.397 * user.peso_kg) + (4.799 * user.altura_cm) - (5.677 * idade)
        tmb_feminino = 447.593 + (9.247 * user.peso_kg) + (3.098 * user.altura_cm) - (4.330 * idade)
        tmb = (tmb_masculino + tmb_feminino) / 2
    
    # 4. Calcular Calorias de Manutenção (GET - Gasto Energético Total)
    fator_atividade = FATORES_ATIVIDADE.get(user.nivel_atividade.value, 1.2) # Usa 1.2 se o valor não for encontrado
    calorias_manutencao = tmb * fator_atividade

    # 5. Ajustar Calorias com base no Objetivo
    if user.objetivo.value == "perder_peso":
        calorias_objetivo = calorias_manutencao - 500 # Déficit de ~500 kcal/dia para perder ~0.5kg/semana
    elif user.objetivo.value == "ganhar_massa":
        calorias_objetivo = calorias_manutencao + 500 # Superávit de ~500 kcal/dia para ganhar ~0.5kg/semana
    else: # manter_peso
        calorias_objetivo = calorias_manutencao
        
    # 6. Calcular Macronutrientes (exemplo de distribuição: 2.0g/kg de proteína, 1.0g/kg de gordura, resto de carboidratos)
    proteinas_g = 2.0 * user.peso_kg
    calorias_proteinas = proteinas_g * 4 # 1g de proteína ~ 4 kcal
    
    gorduras_g = 1.0 * user.peso_kg
    calorias_gorduras = gorduras_g * 9 # 1g de gordura ~ 9 kcal
    
    calorias_carboidratos = calorias_objetivo - calorias_proteinas - calorias_gorduras
    # Garante que os carboidratos não fiquem negativos se a meta calórica for muito baixa
    if calorias_carboidratos < 0:
        calorias_carboidratos = 0
        
    carboidratos_g = calorias_carboidratos / 4 # 1g de carboidrato ~ 4 kcal
    
    # Retorna um dicionário com os resultados arredondados
    return {
        "tmb": round(tmb, 2),
        "calorias_manutencao": round(calorias_manutencao, 2),
        "calorias_objetivo": round(calorias_objetivo, 2),
        "proteinas_g": round(proteinas_g, 2),
        "carboidratos_g": round(carboidratos_g, 2),
        "gorduras_g": round(gorduras_g, 2),
    }

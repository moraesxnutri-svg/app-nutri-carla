import streamlit as st
import urllib.parse
import os

# --- CONFIGURAÇÃO DA NUTRI ---
NOME_NUTRI = "CARLA SANTOS"
WHATSAPP_NUMERO = "5524998498644" 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Anamnese | Carla Santos",
    page_icon="📋",
    layout="centered"
)

# --- ESTILO VISUAL PADRÃO CARLA SANTOS (VERDE/DOURADO) ---
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp {
        background-color: #f4f4f2;
        color: #1a1a1a;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #c2b280;
        border-radius: 5px;
    }
    .stSelectbox>div>div>div {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #c2b280;
    }

    /* Títulos */
    h1 {
        color: #384d21;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: -20px;
    }
    
    /* Subtítulos */
    h3 {
        color: #384d21;
        border-bottom: 2px solid #c2b280;
        padding-bottom: 5px;
        margin-top: 30px;
        font-size: 1.2rem;
    }
    
    /* Botão */
    .stButton>button {
        background-color: #384d21;
        color: white;
        border-radius: 8px;
        border: none;
        height: 55px;
        font-weight: bold;
        font-size: 16px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #c2b280;
        color: #384d21;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO E CABEÇALHO ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    # Tenta carregar a logo, se não existir, mostra apenas o título
    if os.path.exists("logo_carla.png"):
        st.image("logo_carla.png", use_container_width=True)

st.title("FICHA DE ANAMNESE")
st.markdown(f"<center><small>NUTRICIONISTA {NOME_NUTRI} | TRIAGEM INICIAL</small></center>", unsafe_allow_html=True)
st.write("---")

# --- FORMULÁRIO ---
with st.form("anamnese_form"):
    
    # 1. DADOS PESSOAIS
    st.markdown("### 1. DADOS PESSOAIS")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
        idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
        sexo = st.selectbox("Sexo Biológico", ["Masculino", "Feminino"])
    with col2:
        peso = st.number_input("Peso Atual (kg)", format="%.1f")
        altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
        objetivo = st.selectbox("Objetivo Principal", ["Emagrecimento", "Hipertrofia (Ganho de Massa)", "Saúde/Reeducação", "Performance Esportiva"])

    # 2. ROTINA
    st.markdown("### 2. ROTINA E SONO")
    profissao = st.text_input("Profissão (Descreva se é ativo ou sedentário)")
    col_rot1, col_rot2 = st.columns(2)
    with col_rot1:
        horario_acorda = st.text_input("Horário que acorda")
    with col_rot2:
        horario_dorme = st.text_input("Horário que dorme")
        
    qualidade_sono = st.selectbox("Qualidade do Sono", ["Bom / Reparador", "Regular / Acordo cansado", "Ruim / Insônia"])
    agua = st.slider("Ingestão de Água Diária (Litros)", 0.0, 5.0, 2.0, 0.5)

    # 3. HISTÓRICO CLÍNICO
    st.markdown("### 3. SAÚDE GERAL")
    patologias = st.text_area("Diagnósticos médicos (Diabetes, Hipertensão, Colesterol...)", placeholder="Se não houver, digite 'Nenhum'.")
    medicamentos = st.text_input("Uso de medicamentos contínuos (Quais?)")
    intestino = st.selectbox("Funcionamento Intestinal", ["Regular (Diário)", "Constipado (Preso)", "Acelerado/Solto", "Muitos gases/Estufamento"])
    alergias = st.text_input("Alergias ou Intolerâncias Alimentares")

    # 4. ALIMENTAÇÃO
    st.markdown("### 4. HÁBITOS ALIMENTARES")
    quem_cozinha = st.selectbox("Responsável pelas refeições", ["Eu mesmo", "Familiar/Cônjuge", "Restaurante/Marmita", "Outros"])
    nao_gosta = st.text_input("Aversões (Alimentos que NÃO consome)")
    gosta_muito = st.text_input("Preferências (Alimentos que gostaria de manter)")
    
    col_alim1, col_alim2 = st.columns(2)
    with col_alim1:
        fome_horario = st.text_input("Horário de maior fome")
    with col_alim2:
        doces = st.selectbox("Consumo de Doces", ["Baixo/Controlado", "Moderado", "Alto/Vício"])
        
    alcool = st.selectbox("Consumo de Álcool", ["Não bebo", "Socialmente (Fim de semana)", "Frequente (3x+ na semana)"])

    # 5. TREINO
    st.markdown("### 5. ATIVIDADE FÍSICA")
    pratica_exercicio = st.radio("Pratica exercícios físicos?", ["Sim", "Não"])
    
    # Variáveis vazias para não quebrar o código se for sedentário
    tipo_treino = "Sedentário"
    frequencia_treino = "Nenhuma"
    horario_treino = "-"
    
    if pratica_exercicio == "Sim":
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tipo_treino = st.text_input("Modalidade (Musculação, Crossfit...)")
            frequencia_treino = st.selectbox("Frequência Semanal", ["1-2x", "3-4x", "5-6x", "Todos os dias"])
        with col_t2:
            horario_treino = st.text_input("Horário do Treino")
            
    suplementos = st.text_input("Suplementação Atual (Whey, Creatina, Vitaminas...)")

    # 6. ESPECÍFICO (CONDICIONAL)
    st.markdown("### 6. SAÚDE HORMONAL")
    
    info_hormonal = ""
    if sexo == "Feminino":
        col_fem1, col_fem2 = st.columns(2)
        with col_fem1:
            ciclo = st.selectbox("Ciclo Menstrual", ["Regular", "Irregular", "Menopausa", "Uso Contínuo (Não menstruo)"])
            tpm = st.selectbox("Sintomas de TPM", ["Leves/Nenhum", "Inchaço/Fome", "Irritabilidade Intensa"])
        with col_fem2:
            anticoncepcional = st.text_input("Uso de Anticoncepcional (Qual?)")
        info_hormonal = f"Ciclo: {ciclo} | TPM: {tpm} | AC: {anticoncepcional}"
    else:
        # Perfil Masculino
        col_masc1, col_masc2 = st.columns(2)
        with col_masc1:
            disposicao = st.selectbox("Nível de Disposição/Libido", ["Normal/Alta", "Baixa/Cansaço constante"])
        with col_masc2:
            uso_hormonio = st.selectbox("Uso de Ergogênicos/Testosterona", ["Natural (Não uso)", "Em uso", "Já utilizei no passado"])
        info_hormonal = f"Disposição: {disposicao} | Hormônios: {uso_hormonio}"

    obs_finais = st.text_area("Observações Adicionais (Rotina específica, objetivos detalhados...):")

    st.write("")
    # --- BOTÃO DE ENVIO ---
    submitted = st.form_submit_button("GERAR FICHA E ENVIAR 📲")

    if submitted:
        if not nome:
            st.error("Por favor, preencha o Nome Completo para continuar.")
        else:
            # Montagem do Texto Profissional para o WhatsApp
            mensagem = f"""
📋 *ANAMNESE NUTRICIONAL - CARLA SANTOS*
----------------------------------
👤 *PACIENTE:* {nome}
📊 *DADOS:* {idade} anos | {peso}kg | {altura}cm
🧬 *SEXO:* {sexo}
🎯 *OBJETIVO:* {objetivo}
----------------------------------
⚙️ *ROTINA:*
- Trabalho: {profissao}
- Horários: Acorda {horario_acorda} | Dorme {horario_dorme}
- Sono: {qualidade_sono}
- Hidratação: {agua}L
----------------------------------
🏥 *CLÍNICO:*
- Patologias: {patologias}
- Meds: {medicamentos}
- Intestino: {intestino}
- Alergias: {alergias}
----------------------------------
🥗 *ALIMENTAÇÃO:*
- Preparo: {quem_cozinha}
- Aversões: {nao_gosta}
- Preferências: {gosta_muito}
- Pico de Fome: {fome_horario}
- Doces: {doces}
- Álcool: {alcool}
----------------------------------
💪 *TREINO:*
- Status: {pratica_exercicio}
- Detalhes: {tipo_treino} ({frequencia_treino}) às {horario_treino}
- Suplementos: {suplementos}
----------------------------------
⚖️ *HORMONAL:*
- {info_hormonal}
----------------------------------
📝 *OBS:* {obs_finais}
----------------------------------
✅ *Ficha enviada para análise.*
"""
            # Codifica a mensagem
            texto_codificado = urllib.parse.quote(mensagem)
            link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={texto_codificado}"

            # Exibe Sucesso e Botão Final Grande
            st.success("✅ Ficha gerada com sucesso! Clique abaixo para enviar.")
            
            st.markdown(f"""
                <a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
                    <div style="
                        background-color: #25D366; 
                        color: white; 
                        padding: 18px; 
                        border-radius: 12px; 
                        text-align: center; 
                        font-weight: bold; 
                        font-size: 20px; 
                        margin-top: 15px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                        font-family: sans-serif;
                    ">
                        📲 ENVIAR AGORA PELO WHATSAPP
                    </div>
                </a>
            """, unsafe_allow_html=True)
            
            st.info("O WhatsApp abrirá automaticamente com as respostas preenchidas.")

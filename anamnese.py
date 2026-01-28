import streamlit as st
import urllib.parse
import os

# ==============================================================================
# 1. CONFIGURAÇÕES DO PROFISSIONAL
# ==============================================================================
NOME_NUTRI = "CARLA SANTOS"
WHATSAPP_NUMERO = "5524998498644" 

# Configuração da Página
st.set_page_config(
    page_title="Anamnese | Carla Santos",
    page_icon="📋",
    layout="centered"
)

# ==============================================================================
# 2. ESTILO VISUAL - VACINA ANTI-MODO ESCURO (CORRIGIDO)
# ==============================================================================
st.markdown("""
    <style>
    /* --- 1. FUNDO GERAL (CREME) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f4f2;
    }
    .stApp {
        background-color: #f4f4f2;
        color: #000000;
    }

    /* --- 2. FORÇAR TEXTOS PRETOS (GERAL) --- */
    h1, h2, h3, h4, h5, h6, span, label, .stMarkdown, p, div {
        color: #000000 !important;
    }

    /* --- 3. CORREÇÃO DO MENU SUSPENSO (SELECTBOX) QUE ESTAVA PRETO --- */
    /* Fundo da caixa fechada: BRANCO */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #c2b280 !important;
        color: #000000 !important;
    }
    
    /* Fundo da lista quando ABRE (Onde estava preto na sua foto): BRANCO FORÇADO */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #c2b280 !important;
    }
    
    /* Cada opção da lista: FUNDO BRANCO e TEXTO PRETO */
    li[role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Texto dentro da opção: PRETO */
    li[role="option"] div {
        color: #000000 !important;
    }

    /* Quando passa o dedo em cima (Hover/Selecionado): CINZA CLARO */
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #f0f0f0 !important;
        color: #384d21 !important; /* Verde da marca */
    }

    /* --- 4. INPUTS (CAIXAS DE DIGITAR) --- */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #ffffff !important; /* Fundo Branco */
        color: #000000 !important; /* Letra Preta */
        border: 1px solid #c2b280 !important;
    }

    /* --- 5. TÍTULOS E LOGO --- */
    h1 {
        color: #384d21 !important;
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 24px !important;
        margin-top: -10px;
    }
    
    h3 {
        color: #384d21 !important;
        border-bottom: 2px solid #c2b280;
        padding-bottom: 5px;
        margin-top: 30px;
        font-size: 18px !important;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* --- 6. BOTÃO DE ENVIO (VERDE COM LETRA BRANCA) --- */
    .stButton > button {
        background-color: #384d21 !important;
        border: none;
        border-radius: 12px;
        height: 65px !important;
        width: 100%;
        margin-top: 20px;
    }
    
    /* Força especificamente o texto do botão a ser BRANCO (para não sumir) */
    .stButton > button p, .stButton > button div {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    .stButton > button:hover {
        background-color: #2e3f1c !important;
    }

    /* --- 7. LIMPEZA VISUAL --- */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. CABEÇALHO E LOGO (DIMINUÍDA)
# ==============================================================================
# Colunas [3, 1, 3] para deixar a logo pequena e centralizada
col_logo1, col_logo2, col_logo3 = st.columns([3, 1, 3])

with col_logo2:
    if os.path.exists("logo_carla.png"):
        st.image("logo_carla.png", use_container_width=True)

st.title("FICHA DE ANAMNESE")
st.markdown(f"<center><small style='font-size: 14px; color: #555 !important;'>NUTRICIONISTA {NOME_NUTRI}</small></center>", unsafe_allow_html=True)

# ==============================================================================
# 4. FORMULÁRIO
# ==============================================================================
with st.form("anamnese_form"):
    
    st.markdown("### 1. DADOS PESSOAIS")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
        idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
    with col2:
        peso = st.number_input("Peso (kg)", format="%.1f")
        altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
        objetivo = st.selectbox("Objetivo", ["Emagrecimento", "Hipertrofia", "Saúde", "Performance"])

    st.markdown("### 2. ROTINA")
    profissao = st.text_input("Profissão")
    col_rot1, col_rot2 = st.columns(2)
    with col_rot1:
        horario_acorda = st.text_input("Acorda às")
    with col_rot2:
        horario_dorme = st.text_input("Dorme às")
        
    qualidade_sono = st.selectbox("Sono", ["Bom", "Regular", "Ruim/Insônia"])
    agua = st.slider("Água (Litros/dia)", 0.0, 5.0, 2.0, 0.5)

    st.markdown("### 3. SAÚDE")
    patologias = st.text_area("Doenças Diagnosticadas", placeholder="Digite 'Nenhuma' se não houver.")
    medicamentos = st.text_input("Medicamentos Contínuos")
    intestino = st.selectbox("Intestino", ["Diário", "Preso", "Solto", "Gases/Estufamento"])
    alergias = st.text_input("Alergias Alimentares")

    st.markdown("### 4. ALIMENTAÇÃO")
    quem_cozinha = st.selectbox("Preparo das Refeições", ["Eu mesmo", "Familiar", "Restaurante", "Funcionária"])
    nao_gosta = st.text_input("Não come de jeito nenhum")
    gosta_muito = st.text_input("Gostaria de manter na dieta")
    
    col_alim1, col_alim2 = st.columns(2)
    with col_alim1:
        fome_horario = st.text_input("Maior fome às")
    with col_alim2:
        doces = st.selectbox("Doces", ["Pouco", "Moderado", "Muito"])
        
    alcool = st.selectbox("Álcool", ["Não bebo", "Socialmente", "Frequente"])

    st.markdown("### 5. TREINO")
    pratica_exercicio = st.radio("Pratica exercícios?", ["Sim", "Não"])
    
    tipo_treino = "Sedentário"
    frequencia_treino = "Nenhuma"
    horario_treino = "-"
    
    if pratica_exercicio == "Sim":
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tipo_treino = st.text_input("Modalidade")
            frequencia_treino = st.selectbox("Frequência", ["1-2x", "3-4x", "5-6x", "Todo dia"])
        with col_t2:
            horario_treino = st.text_input("Horário")
            
    suplementos = st.text_input("Suplementos (Whey, Creatina...)")

    st.markdown("### 6. HORMONAL")
    info_hormonal = ""
    if sexo == "Feminino":
        col_fem1, col_fem2 = st.columns(2)
        with col_fem1:
            ciclo = st.selectbox("Ciclo Menstrual", ["Regular", "Irregular", "Menopausa", "Uso Contínuo"])
            tpm = st.selectbox("TPM", ["Leve", "Média", "Forte"])
        with col_fem2:
            anticoncepcional = st.text_input("Anticoncepcional")
        info_hormonal = f"Ciclo: {ciclo} | TPM: {tpm} | AC: {anticoncepcional}"
    else:
        col_masc1, col_masc2 = st.columns(2)
        with col_masc1:
            disposicao = st.selectbox("Disposição/Libido", ["Boa", "Baixa"])
        with col_masc2:
            uso_hormonio = st.selectbox("Hormônios/Testo", ["Não uso", "Uso atualmente", "Já usei"])
        info_hormonal = f"Disposição: {disposicao} | Hormônios: {uso_hormonio}"

    obs_finais = st.text_area("Observações Finais")

    st.write("") 
    
    # BOTÃO VERDE COM LETRA BRANCA FORÇADA
    submitted = st.form_submit_button("FINALIZAR E ENVIAR 📲")

    if submitted:
        if not nome:
            st.error("⚠️ Preencha seu nome.")
        else:
            # TEXTO DO WHATSAPP
            mensagem = f"""
📋 *ANAMNESE - CARLA SANTOS*
👤 {nome} | {idade}a | {peso}kg | {altura}cm
🎯 Obj: {objetivo}
---------------------------
⚙️ *ROTINA*
💼 {profissao}
⏰ Acorda: {horario_acorda} | Dorme: {horario_dorme}
💤 Sono: {qualidade_sono} | 💧 {agua}L
---------------------------
🏥 *SAÚDE*
💊 Meds: {medicamentos}
🤢 Patol: {patologias}
💩 Intestino: {intestino}
🚫 Alergia: {alergias}
---------------------------
🥗 *DIETA*
🍳 Preparo: {quem_cozinha}
❌ Aversão: {nao_gosta}
❤️ Pref: {gosta_muito}
🕒 Fome: {fome_horario} | 🍬 Doces: {doces}
🍺 Álcool: {alcool}
---------------------------
💪 *TREINO*
🏋️ {tipo_treino} ({frequencia_treino}) às {horario_treino}
⚡ Supl: {suplementos}
---------------------------
⚖️ *HORMONAL*
{info_hormonal}
---------------------------
📝 {obs_finais}
"""
            texto_codificado = urllib.parse.quote(mensagem)
            link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={texto_codificado}"

            st.success("✅ Sucesso! Envie abaixo:")
            
            # Botão HTML Extra para garantir visualização
            st.markdown(f"""
                <a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
                    <div style="
                        background-color: #25D366; 
                        color: white !important; 
                        padding: 15px; 
                        border-radius: 10px; 
                        text-align: center; 
                        font-weight: bold; 
                        font-size: 18px; 
                        margin-top: 10px;
                        font-family: sans-serif;
                    ">
                        📲 ENVIAR NO WHATSAPP
                    </div>
                </a>
            """, unsafe_allow_html=True)

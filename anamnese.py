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
# 2. ESTILO VISUAL BLINDADO (V8 + MOBILE FIX)
# ==============================================================================
st.markdown("""
    <style>
    /* --- 1. FUNDO E CORES GERAIS (Força Modo Claro) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f4f2; /* Creme Suave */
    }
    .stApp {
        background-color: #f4f4f2;
        color: #1a1a1a;
    }
    
    /* Força cor do texto para preto/cinza escuro em tudo */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, .stMarkdown {
        color: #1a1a1a !important;
    }

    /* --- 2. TIPOGRAFIA OTIMIZADA --- */
    h1 {
        color: #384d21 !important; /* Verde Olívia */
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 26px !important;
        margin-top: -10px;
    }
    
    h3 {
        color: #384d21 !important;
        border-bottom: 2px solid #c2b280; /* Dourado */
        padding-bottom: 8px;
        margin-top: 35px;
        font-size: 20px !important;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* Aumenta letra dos rótulos para facilitar leitura no celular */
    label p {
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* --- 3. CAMPOS DE TEXTO (INPUTS) --- */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input, 
    .stTextArea>div>div>textarea {
        background-color: #ffffff !important;
        color: #000000 !important; /* Texto preto ao digitar */
        border: 1px solid #c2b280 !important;
        border-radius: 8px;
        font-size: 18px !important; /* Letra grande */
        padding: 15px !important; /* Espaço para o dedo */
    }
    
    /* --- 4. CAIXAS DE SELEÇÃO (SELECTBOX) --- */
    .stSelectbox>div>div>div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #c2b280 !important;
        border-radius: 8px;
        font-size: 18px !important;
    }

    /* --- 5. BOTÃO DE ENVIO (BIG BUTTON) --- */
    .stButton>button {
        background-color: #384d21 !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        height: 70px !important; /* Bem alto para clicar fácil */
        font-size: 20px !important;
        font-weight: bold;
        width: 100%;
        margin-top: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2e3f1c !important;
        transform: scale(1.02);
    }
    
    /* --- 6. AJUSTES FINAIS --- */
    /* Remove menu do Streamlit para parecer um App nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Margem para não cortar conteúdo no mobile */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. CABEÇALHO E LOGO
# ==============================================================================
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    if os.path.exists("logo_carla.png"):
        st.image("logo_carla.png", use_container_width=True)

st.title("FICHA DE ANAMNESE")
st.markdown(f"<center><small style='font-size: 16px; color: #555;'>NUTRICIONISTA {NOME_NUTRI} | TRIAGEM INICIAL</small></center>", unsafe_allow_html=True)

# ==============================================================================
# 4. FORMULÁRIO INTELIGENTE
# ==============================================================================
with st.form("anamnese_form"):
    
    # --- SEÇÃO 1: PESSOAL ---
    st.markdown("### 1. QUEM É VOCÊ?")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
        idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
        sexo = st.selectbox("Sexo Biológico", ["Masculino", "Feminino"])
    with col2:
        peso = st.number_input("Peso Atual (kg)", format="%.1f")
        altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
        objetivo = st.selectbox("Objetivo Principal", ["Emagrecimento", "Hipertrofia (Massa)", "Saúde/Reeducação", "Performance"])

    # --- SEÇÃO 2: ROTINA ---
    st.markdown("### 2. ROTINA E SONO")
    profissao = st.text_input("Profissão (Trabalha sentado ou em pé?)")
    
    col_rot1, col_rot2 = st.columns(2)
    with col_rot1:
        horario_acorda = st.text_input("Horário que acorda")
    with col_rot2:
        horario_dorme = st.text_input("Horário que dorme")
        
    qualidade_sono = st.selectbox("Como é seu sono?", ["Bom / Reparador", "Regular / Acordo cansado", "Ruim / Insônia"])
    agua = st.slider("Consumo de água (Litros/dia)", 0.0, 5.0, 2.0, 0.5)

    # --- SEÇÃO 3: SAÚDE ---
    st.markdown("### 3. SAÚDE CLÍNICA")
    patologias = st.text_area("Doenças diagnosticadas (Diabetes, Pressão, Tireoide...)", placeholder="Digite 'Nenhuma' se não houver.")
    medicamentos = st.text_input("Usa algum medicamento contínuo? Qual?")
    intestino = st.selectbox("Funcionamento do Intestino", ["Diário (Normal)", "Preso (2-3 dias sem ir)", "Solto/Urgência", "Muitos gases/Estufamento"])
    alergias = st.text_input("Alergias ou Intolerâncias (Glúten, Lactose, Camarão...)")

    # --- SEÇÃO 4: ALIMENTAÇÃO ---
    st.markdown("### 4. HÁBITOS ALIMENTARES")
    quem_cozinha = st.selectbox("Quem prepara as refeições?", ["Eu mesmo", "Familiar/Cônjuge", "Restaurante/Marmita", "Funcionária"])
    nao_gosta = st.text_input("O que você NÃO come de jeito nenhum?")
    gosta_muito = st.text_input("O que você GOSTARIA de manter na dieta?")
    
    col_alim1, col_alim2 = st.columns(2)
    with col_alim1:
        fome_horario = st.text_input("Horário de maior fome")
    with col_alim2:
        doces = st.selectbox("Consumo de Doces", ["Baixo", "Moderado", "Alto/Vício"])
        
    alcool = st.selectbox("Bebida Alcoólica", ["Não bebo", "Socialmente (Fim de semana)", "Frequente (3x+ na semana)"])

    # --- SEÇÃO 5: TREINO ---
    st.markdown("### 5. ATIVIDADE FÍSICA")
    pratica_exercicio = st.radio("Pratica exercícios?", ["Sim", "Não"])
    
    tipo_treino = "Sedentário"
    frequencia_treino = "Nenhuma"
    horario_treino = "-"
    
    if pratica_exercicio == "Sim":
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tipo_treino = st.text_input("Modalidade (Musculação, Crossfit...)")
            frequencia_treino = st.selectbox("Frequência", ["1-2x semana", "3-4x semana", "5-6x semana", "Todo dia"])
        with col_t2:
            horario_treino = st.text_input("Horário do treino")
            
    suplementos = st.text_input("Suplementos atuais (Whey, Creatina...)")

    # --- SEÇÃO 6: HORMONAL (INTELIGENTE) ---
    st.markdown("### 6. SAÚDE HORMONAL")
    
    info_hormonal = ""
    if sexo == "Feminino":
        col_fem1, col_fem2 = st.columns(2)
        with col_fem1:
            ciclo = st.selectbox("Ciclo Menstrual", ["Regular", "Irregular", "Menopausa", "Uso Contínuo (Sem menstruar)"])
            tpm = st.selectbox("Sintomas de TPM", ["Leves/Nenhum", "Inchaço/Fome", "Irritabilidade/Choro"])
        with col_fem2:
            anticoncepcional = st.text_input("Anticoncepcional (Qual?)")
        info_hormonal = f"Ciclo: {ciclo} | TPM: {tpm} | AC: {anticoncepcional}"
    else:
        # Perfil Masculino
        col_masc1, col_masc2 = st.columns(2)
        with col_masc1:
            disposicao = st.selectbox("Disposição / Libido", ["Normal/Alta", "Baixa/Cansaço constante"])
        with col_masc2:
            uso_hormonio = st.selectbox("Uso de Testosterona/Ergogênicos", ["Natural (Nunca usei)", "Em uso atual", "Já usei no passado"])
        info_hormonal = f"Disposição: {disposicao} | Hormônios: {uso_hormonio}"

    obs_finais = st.text_area("Observações Finais ou Dúvidas:")

    st.write("") # Espaço
    
    # --- BOTÃO FINAL ---
    submitted = st.form_submit_button("✅ FINALIZAR E ENVIAR FICHA")

    if submitted:
        if not nome:
            st.error("⚠️ Por favor, preencha seu Nome Completo no início.")
        else:
            # Montagem da Mensagem do WhatsApp
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
- Acorda: {horario_acorda} | Dorme: {horario_dorme}
- Sono: {qualidade_sono}
- Água: {agua}L
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
- Fome maior às: {fome_horario}
- Doces: {doces}
- Álcool: {alcool}
----------------------------------
💪 *TREINO:*
- Pratica: {pratica_exercicio}
- Detalhes: {tipo_treino} ({frequencia_treino}) às {horario_treino}
- Suplementos: {suplementos}
----------------------------------
⚖️ *HORMONAL:*
- {info_hormonal}
----------------------------------
📝 *OBSERVAÇÕES:* {obs_finais}
----------------------------------
✅ *Ficha enviada. Aguardo orientações!*
"""
            # Codifica a mensagem
            texto_codificado = urllib.parse.quote(mensagem)
            link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={texto_codificado}"

            # Feedback Visual de Sucesso
            st.success("✅ Ficha gerada com sucesso! Clique no botão abaixo para enviar.")
            
            # Botão de Redirecionamento (Visual Verde Zap)
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
                        margin-top: 10px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                        font-family: sans-serif;
                    ">
                        📲 ENVIAR AGORA PELO WHATSAPP
                    </div>
                </a>
            """, unsafe_allow_html=True)
            
            st.info("O WhatsApp abrirá automaticamente com suas respostas preenchidas.")

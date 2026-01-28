import streamlit as st
import urllib.parse

# --- CONFIGURAÇÃO DA NUTRI ---
NOME_NUTRI = "CARLA SANTOS"
WHATSAPP_NUMERO = "5524998498644" 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Anamnese Digital | Carla Santos",
    page_icon="🥗",
    layout="centered"
)

# --- ESTILO VISUAL PADRÃO CARLA SANTOS (VERDE/DOURADO) ---
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp {
        background-color: #f4f4f2; /* Fundo Creme Suave */
        color: #1a1a1a;
    }
    
    /* Inputs (Caixas de Texto) */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #c2b280; /* Borda Dourada */
        border-radius: 5px;
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #c2b280;
    }

    /* Títulos Principais */
    h1 {
        color: #384d21; /* Verde Olívia Forte */
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    /* Subtítulos */
    h2, h3 {
        color: #384d21;
        border-bottom: 2px solid #c2b280; /* Linha Dourada */
        padding-bottom: 5px;
        margin-top: 20px;
    }
    
    /* Botão de Enviar (Streamlit) */
    .stButton>button {
        background-color: #384d21; /* Verde */
        color: white;
        border-radius: 8px;
        border: none;
        height: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #c2b280; /* Dourado no Hover */
        color: #384d21;
    }
    
    /* Texto de Aviso */
    .stAlert {
        background-color: #e8f5e9;
        color: #384d21;
        border: 1px solid #384d21;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🥗 ANAMNESE DIGITAL")
st.markdown(f"<center><b>NUTRICIONISTA:</b> {NOME_NUTRI} | <b>FASE:</b> Coleta de Dados</center>", unsafe_allow_html=True)
st.info("Olá! Preencha este formulário com atenção. Suas respostas vão guiar a montagem do seu protocolo personalizado.")

# --- FORMULÁRIO ---
with st.form("anamnese_form"):
    
    # 1. DADOS PESSOAIS
    st.header("1. QUEM É VOCÊ?")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
        idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
        sexo = st.selectbox("Sexo Biológico", ["Feminino", "Masculino"])
    with col2:
        peso = st.number_input("Peso Atual (kg)", format="%.1f")
        altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
        objetivo = st.selectbox("Objetivo Principal", ["Emagrecimento (Secar)", "Hipertrofia (Ganhar Massa)", "Saúde/Reeducação", "Performance Esportiva"])

    # 2. ROTINA E ESTILO DE VIDA
    st.header("2. SUA ROTINA")
    profissao = st.text_input("Profissão / Ocupação (Fica muito tempo sentado ou em pé?)")
    horario_acorda = st.text_input("Que horas costuma acordar?")
    horario_dorme = st.text_input("Que horas costuma dormir?")
    qualidade_sono = st.selectbox("Como é seu sono?", ["Durmo bem e acordo descansado", "Acordo cansado", "Tenho insônia/Acordo muito"])
    agua = st.slider("Consumo de água diário (Litros)", 0.0, 5.0, 1.5, 0.5)

    # 3. HISTÓRICO DE SAÚDE
    st.header("3. SAÚDE CLÍNICA")
    patologias = st.text_area("Tem alguma doença diagnosticada? (Diabetes, Tireoide, Gastrite...)", placeholder="Não tenho ou descreva...")
    medicamentos = st.text_input("Toma algum remédio de uso contínuo? Qual?")
    intestino = st.selectbox("Como funciona seu intestino?", ["Todo dia (Normal)", "Preso (2-3 dias sem ir)", "Solto/Diarréia frequente", "Muitos gases/Estufamento"])
    alergias = st.text_input("Tem alergia ou intolerância a algum alimento? (Glúten, Lactose...)")

    # 4. ALIMENTAÇÃO
    st.header("4. HÁBITOS ALIMENTARES")
    quem_cozinha = st.selectbox("Quem prepara suas refeições?", ["Eu mesmo(a)", "Familiar/Cônjuge", "Como em restaurante/Marmita", "Empregada"])
    nao_gosta = st.text_input("Alimentos que você NÃO COME de jeito nenhum (Aversões)")
    gosta_muito = st.text_input("Alimentos que você GOSTARIA MUITO de ter na dieta (Preferências)")
    fome_horario = st.text_input("Em qual horário sente mais fome?")
    doces = st.selectbox("Sente muita vontade de doces?", ["Não, tranquilo", "Sim, principalmente à tarde/noite", "Sim, após as refeições", "Sou viciado(a)"])
    alcool = st.selectbox("Consumo de Álcool", ["Não bebo", "Socialmente (Fim de semana)", "Algumas vezes na semana", "Todo dia"])

    # 5. TREINO E ATIVIDADE
    st.header("5. ATIVIDADE FÍSICA")
    pratica_exercicio = st.radio("Pratica exercícios?", ["Sim", "Não (Sedentário)"])
    tipo_treino = ""
    frequencia_treino = ""
    horario_treino = ""
    
    if pratica_exercicio == "Sim":
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tipo_treino = st.text_input("Qual modalidade? (Musculação, Crossfit, Corrida...)")
            frequencia_treino = st.selectbox("Quantas vezes na semana?", ["1-2x", "3-4x", "5-6x", "Todo dia"])
        with col_t2:
            horario_treino = st.text_input("Qual horário do treino?")
            
    suplementos = st.text_input("Usa algum suplemento atualmente? (Whey, Creatina...)")

    # 6. ESPECÍFICO (HOMEM/MULHER)
    st.header("6. SAÚDE HORMONAL")
    
    info_hormonal = ""
    if sexo == "Feminino":
        ciclo = st.selectbox("Ciclo Menstrual", ["Regular", "Irregular", "Menopausa", "Uso Contínuo (Não menstruo)"])
        anticoncepcional = st.text_input("Usa anticoncepcional? Qual?")
        tpm = st.selectbox("Sente muita TPM?", ["Não/Leve", "Sim, inchaço e fome", "Sim, muita irritabilidade"])
        info_hormonal = f"Ciclo: {ciclo} | AC: {anticoncepcional} | TPM: {tpm}"
    else:
        disposicao = st.selectbox("Como está sua disposição/libido?", ["Normal/Alta", "Baixa/Cansado"])
        uso_hormonio = st.selectbox("Uso de testosterona/ergogênicos?", ["Não, natural", "Sim, faço uso", "Já usei no passado"])
        info_hormonal = f"Disposição: {disposicao} | Ergogênicos: {uso_hormonio}"

    obs_finais = st.text_area("Observações Finais (Algo mais que eu deva saber?):")

    # --- BOTÃO DE ENVIO DO FORMULÁRIO ---
    submitted = st.form_submit_button("FINALIZAR E GERAR MENSAGEM 🥗")

    if submitted:
        if not nome:
            st.error("Por favor, preencha pelo menos o seu Nome.")
        else:
            # Montagem do Texto para o WhatsApp
            mensagem = f"""
🌿 *ANAMNESE DIGITAL - CARLA SANTOS* 🌿
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
🏥 *SAÚDE:*
- Patologias: {patologias}
- Meds: {medicamentos}
- Intestino: {intestino}
- Alergias: {alergias}
----------------------------------
🥗 *ALIMENTAÇÃO:*
- Cozinheiro: {quem_cozinha}
- Aversões (Não come): {nao_gosta}
- Preferências (Gosta): {gosta_muito}
- Fome maior às: {fome_horario}
- Doces: {doces}
- Álcool: {alcool}
----------------------------------
💪 *TREINO:*
- Pratica: {pratica_exercicio}
- Modalidade: {tipo_treino} ({frequencia_treino})
- Horário: {horario_treino}
- Suplementos: {suplementos}
----------------------------------
⚖️ *HORMONAL:*
- {info_hormonal}
----------------------------------
📝 *OBSERVAÇÕES:* {obs_finais}
----------------------------------
✅ *Ficha preenchida. Aguardo orientações!*
"""
            # Codifica a mensagem para URL
            texto_codificado = urllib.parse.quote(mensagem)
            link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={texto_codificado}"

            # Exibe Sucesso e Botão Final
            st.success("✅ Ficha gerada com sucesso!")
            
            st.markdown(f"""
                <a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
                    <div style="
                        background-color: #25D366; 
                        color: white; 
                        padding: 15px; 
                        border-radius: 10px; 
                        text-align: center; 
                        font-weight: bold; 
                        font-size: 18px; 
                        margin-top: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    ">
                        📲 ENVIAR FICHA PELO WHATSAPP AGORA
                    </div>
                </a>
            """, unsafe_allow_html=True)
            
            st.caption("Ao clicar, seu WhatsApp abrirá automaticamente com todas as respostas preenchidas para você enviar para a Carla.")

import streamlit as st
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
import os

# ==============================================================================
# CONFIGURAÇÕES DO SISTEMA (PADRÃO V8)
# ==============================================================================
COLOR_PRIMARY = colors.Color(0.22, 0.30, 0.13)  # Verde Olívia
COLOR_ACCENT = colors.Color(0.77, 0.62, 0.20)   # Dourado
COLOR_HEADER_BG = colors.Color(0.96, 0.96, 0.94) 
COLOR_LINE = colors.Color(0.85, 0.85, 0.85)
COLOR_ALERT = colors.Color(0.75, 0.22, 0.17)

# Links Fixos
LINK_CALCULADORA = "https://carlasantos-calc.tiiny.site/index.html"
LINK_WHATSAPP = "https://wa.me/5524998498644"

# ==============================================================================
# FUNÇÕES AUXILIARES DE PDF
# ==============================================================================

def create_pie_chart(p, c, f):
    d = Drawing(200, 100)
    pc = Pie()
    pc.x = 0; pc.y = 10; pc.width = 60; pc.height = 60
    pc.data = [p, c, f]
    pc.labels = None; pc.simpleLabels = 0
    pc.slices.strokeWidth = 1; pc.slices.strokeColor = colors.white
    pc.slices[0].fillColor = COLOR_PRIMARY; pc.slices[1].fillColor = COLOR_ACCENT; pc.slices[2].fillColor = colors.Color(0.6, 0.6, 0.5)
    return d

def gerar_pdf_v8(nome_paciente, tipo_protocolo, dados_dieta, lista_compras, alertas, macros):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    
    # Estilos Personalizados
    style_title = ParagraphStyle('Title', parent=styles['Normal'], fontSize=20, leading=24, textColor=COLOR_PRIMARY, fontName='Helvetica-Bold', alignment=TA_RIGHT, spaceAfter=4)
    style_pro = ParagraphStyle('Pro', parent=styles['Normal'], fontSize=14, textColor=COLOR_ACCENT, fontName='Helvetica-Bold', alignment=TA_RIGHT)
    style_sub = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=11, textColor=colors.gray, alignment=TA_RIGHT)
    style_section = ParagraphStyle('Sec', parent=styles['Normal'], fontSize=14, textColor=COLOR_PRIMARY, fontName='Helvetica-Bold', spaceAfter=10)
    style_warn = ParagraphStyle('Warn', parent=styles['Normal'], fontSize=10, backColor=COLOR_ALERT, textColor=colors.white, borderPadding=10, leading=14, fontName='Helvetica-Bold')
    style_cell_left = ParagraphStyle('CL', parent=styles['Normal'], fontSize=10, textColor=colors.black, leading=12)
    style_cell_right = ParagraphStyle('CR', parent=styles['Normal'], fontSize=10, textColor=colors.black, leading=12, alignment=TA_RIGHT)
    style_btn = ParagraphStyle('Btn', parent=styles['Normal'], fontSize=12, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)

    story = []

    # --- CABEÇALHO ---
    # Tenta carregar logo, se não tiver, usa texto
    logo_path = "logo_carla.png"
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=5.5*cm, height=4*cm, kind='proportional')
        header_content = [[logo_img, [
            Paragraph(tipo_protocolo.upper(), style_title),
            Spacer(1, 6),
            Paragraph("CARLA SANTOS", style_pro),
            Paragraph("Nutricionista Formanda", style_sub),
            Spacer(1, 10),
            Paragraph(f"PACIENTE: <b>{nome_paciente.upper()}</b>", ParagraphStyle('P', alignment=TA_RIGHT, textColor=COLOR_PRIMARY))
        ]]]
    else:
        header_content = [[Paragraph("<b>CARLA SANTOS</b>", style_section), [
            Paragraph(tipo_protocolo.upper(), style_title),
            Paragraph(f"PACIENTE: {nome_paciente.upper()}", style_sub)
        ]]]

    t_header = Table(header_content, colWidths=[6*cm, 11*cm])
    t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'CENTER'), ('ALIGN', (1,0), (1,0), 'RIGHT')]))
    story.append(t_header)
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("_" * 78, ParagraphStyle('L', textColor=COLOR_ACCENT, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.8*cm))

    # --- ALERTAS / REGRAS ---
    if alertas:
        story.append(Paragraph(alertas.replace("\n", "<br/>"), style_warn))
        story.append(Spacer(1, 0.8*cm))

    # --- DASHBOARD MACROS ---
    if macros:
        p, c, f, k = macros
        chart = create_pie_chart(p, c, f)
        txt_macro = f"""<font size=10><b>ESTIMATIVA DIÁRIA:</b><br/>~ {int(k)} kcal<br/>Prot: {int(p)}g | Carb: {int(c)}g | Gord: {int(f)}g</font>"""
        t_meta = Table([[chart, Paragraph(f"<b>RESUMO NUTRICIONAL</b>", style_section), Paragraph(txt_macro, ParagraphStyle('M', alignment=TA_RIGHT))]], colWidths=[3*cm, 8*cm, 6*cm])
        t_meta.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(t_meta)
        story.append(Spacer(1, 0.5*cm))

    # --- DIETA / MENUS ---
    for section in dados_dieta:
        story.append(Paragraph(section['title'], style_section))
        
        # Se tiver subtitulo/descrição
        if 'desc' in section:
            story.append(Paragraph(f"<i>{section['desc']}</i>", ParagraphStyle('I', fontSize=10, textColor=colors.grey)))
            story.append(Spacer(1, 0.2*cm))

        for meal in section['meals']:
            # Título da Refeição
            story.append(Paragraph(f"• {meal['name']}", ParagraphStyle('MT', fontSize=11, textColor=COLOR_PRIMARY, fontName='Helvetica-Bold', spaceAfter=4)))
            
            # Tabela de Alimentos
            data = []
            for food in meal['foods']:
                # Se for destaque (Carboidrato no Ciclo)
                style_curr = style_cell_left
                if "TABELA" in str(food[1]) or "CONSULTAR" in str(food[1]):
                     style_curr = ParagraphStyle('H', parent=style_cell_left, textColor=COLOR_ACCENT, fontName='Helvetica-Bold')
                
                data.append([Paragraph(str(food[0]), style_curr), Paragraph(str(food[1]), style_cell_right)])
            
            t = Table(data, colWidths=[11*cm, 6*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), COLOR_HEADER_BG),
                ('GRID', (0,0), (-1,-1), 0.5, COLOR_LINE),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 0.4*cm))
        
        story.append(PageBreak())

    # --- LISTA DE COMPRAS ---
    if lista_compras:
        story.append(Paragraph("LISTA DE COMPRAS SUGERIDA", style_section))
        t_shop = Table(lista_compras, colWidths=[10*cm, 7*cm])
        t_shop.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,0), (-1,0), COLOR_PRIMARY),
            ('LINEBELOW', (0,0), (-1,0), 1, COLOR_PRIMARY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_HEADER_BG]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8)
        ]))
        story.append(t_shop)
        story.append(Spacer(1, 1*cm))

    # --- BOTÕES FINAIS ---
    story.append(Paragraph("PAINEL DO PACIENTE", style_section))
    story.append(Spacer(1, 0.5*cm))
    
    # Botão Calc
    btn_c = Table([[Paragraph(f'<a href="{LINK_CALCULADORA}"><font color="white">ACESSAR CALCULADORA DE SUBSTITUIÇÕES</font></a>', style_btn)]], colWidths=[14*cm], rowHeights=[1.2*cm])
    btn_c.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ROUNDEDCORNERS', [8,8,8,8])]))
    story.append(btn_c)
    story.append(Spacer(1, 0.5*cm))

    # Botão Whats
    btn_w = Table([[Paragraph(f'<a href="{LINK_WHATSAPP}"><font color="white">FALAR DIRETAMENTE COM A CARLA</font></a>', style_btn)]], colWidths=[14*cm], rowHeights=[1.2*cm])
    btn_w.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), COLOR_ACCENT), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ROUNDEDCORNERS', [8,8,8,8])]))
    story.append(btn_w)

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==============================================================================
# DADOS DOS PROTOCOLOS (BASEDOS NAS SUAS MENSAGENS ANTERIORES)
# ==============================================================================

def get_stephanie_data():
    # Dados extraídos do Ciclo de Carbos / Anti-Cândida
    alertas = """
    PILARES FUNDAMENTAIS (ANTI-CANDIDA):
    1. BLINDAGEM: ZERO Acucar, Trigo, Leite, Amendoim e Alcool.
    2. HIDRATACAO: 4.0 a 4.5 Litros/dia (Obrigatorio).
    3. ACIDIFICACAO: Agua + Limao todo dia em jejum.
    """
    
    # Estrutura unificada: Base Fixa + Tabela de Ciclo
    dieta = [
        {
            "title": "PLANO ALIMENTAR BASE (Diário)",
            "meals": [
                {"name": "DESJEJUM (Pré-Treino)", "foods": [("Ovos", "2 un"), ("Café + Óleo de Coco", "1 col. sopa"), ("CARBO EXTRA", "VER TABELA CICLO")]},
                {"name": "ALMOÇO", "foods": [("Proteína Limpa", "140g"), ("Vegetais", "À vontade"), ("Azeite", "1 fio"), ("CARBO EXTRA", "VER TABELA CICLO")]},
                {"name": "LANCHE DA TARDE", "foods": [("Whey Isolado", "30g"), ("CARBO EXTRA", "VER TABELA CICLO")]},
                {"name": "JANTAR", "foods": [("Proteína Magra", "130g"), ("Salada", "À vontade"), ("Azeite", "1 col. sopa"), ("CARBO EXTRA", "VER TABELA CICLO")]},
                {"name": "CEIA", "foods": [("Chá Calmante", "1 xícara"), ("Opcional", "2 ovos ou Abacate")]}
            ]
        },
        {
            "title": "TABELA DO CICLO DE CARBOIDRATOS",
            "desc": "Adicione estes itens às refeições acima conforme o dia da semana.",
            "meals": [
                {"name": "DIAS ALTOS (Perna/Glúteo)", "foods": [("Café", "+ 2 fat. Pão s/ Glúten"), ("Almoço", "+ 150g Arroz/Batata"), ("Lanche", "+ 1 Banana + Aveia"), ("Jantar", "+ 100g Arroz")]},
                {"name": "DIAS MÉDIOS (Superiores)", "foods": [("Café", "+ 1 fat. Pão"), ("Almoço", "+ 100g Arroz"), ("Lanche", "+ 1/2 Banana"), ("Jantar", "+ 50g Arroz")]},
                {"name": "DIAS BAIXOS (Cardio/Off)", "foods": [("Café", "ZERO (Só ovos/coco)"), ("Almoço", "ZERO (Só prot/veg)"), ("Lanche", "ZERO (Add gordura boa)"), ("Jantar", "ZERO (Só prot/salada)")]}
            ]
        }
    ]
    
    lista = [["PROTEÍNAS", "Peito de Frango, Ovos, Whey"], ["CARBOS", "Arroz, Batata, Aveia, Fruta"], ["GORDURAS", "Azeite, Óleo de Coco, Abacate"]]
    macros = (140, 150, 60, 1700) # Estimativa média
    return "Stephanie Vitória", "Protocolo Ciclo de Carbos + Anti-Fungo", dieta, lista, alertas, macros

def get_gabriel_data():
    # Dados extraídos do Hipertrofia V8
    alertas = """
    DIRETRIZES DE HIPERTROFIA:
    • Hidratação: 3.5L a 4.5L por dia.
    • Constância: Não pule refeições. Volume calculado para ganho.
    """
    dieta = [
        {
            "title": "PLANO ALIMENTAR (Fixo)",
            "meals": [
                {"name": "CAFÉ DA MANHÃ", "foods": [("Tapioca", "40g"), ("Ovos", "2 un"), ("Queijo", "20g"), ("Mamão", "1 fatia"), ("Semente Girassol", "15g")]},
                {"name": "ALMOÇO", "foods": [("Arroz Branco", "250g"), ("Frango", "120g"), ("Azeite", "1 col."), ("Vegetais", "100g")]},
                {"name": "LANCHE", "foods": [("Whey", "30g"), ("Aveia", "20g"), ("Uva", "15 un"), ("Banana", "1 un")]},
                {"name": "JANTAR", "foods": [("Arroz Branco", "230g"), ("Frango", "120g"), ("Vegetais", "100g")]},
                {"name": "CEIA", "foods": [("Abacaxi", "100g")]}
            ]
        }
    ]
    lista = [["PROTEÍNAS", "Frango (2kg), Ovos (30), Whey"], ["CARBOS", "Arroz (1.5kg), Tapioca, Aveia"], ["FRUTAS", "Mamão, Uva, Banana, Abacaxi"]]
    macros = (136, 254, 49, 2018) # Exatos da imagem
    return "Gabriel Almeida", "Protocolo de Hipertrofia", dieta, lista, alertas, macros

def get_maria_data():
    # Dados extraídos do Renal Conservador
    alertas = """
    PREPARO OBRIGATORIO (LIXIVIACAO):
    Descascar, picar e ferver vegetais por 15min.
    Descartar a agua e cozinhar em agua limpa.
    Fundamental para controle do Potassio.
    """
    dieta = [
        {
            "title": "CONTROLE RENAL CONSERVADOR",
            "meals": [
                {"name": "CAFÉ DA MANHÃ", "foods": [("Pão Francês s/ miolo", "1 un"), ("Manteiga", "Ponta faca"), ("Ovo ou Queijo Minas", "1 un/fatia")]},
                {"name": "LANCHE MANHÃ", "foods": [("Maçã ou Pera (s/ casca)", "1 un"), ("Cozida", "Com canela")]},
                {"name": "ALMOÇO", "foods": [("Arroz Branco", "100g"), ("Feijão (s/ caldo)", "50g"), ("Proteína", "80g"), ("Legumes Lixiviados", "80g"), ("Azeite", "1 col.")]},
                {"name": "LANCHE TARDE", "foods": [("Torrada Magic Toast", "2 un"), ("Requeijão", "1 col.")]},
                {"name": "JANTAR", "foods": [("Purê Batata (Lixiviada)", "60g"), ("Carne/Frango", "60g"), ("Azeite", "1 col.")]}
            ]
        }
    ]
    lista = [["PROTEÍNAS", "Frango, Carne Moída, Ovos"], ["CARBOS", "Arroz Branco, Pão, Torrada"], ["LEGUMES", "Cenoura, Chuchu (Lixiviar)"]]
    macros = (55, 200, 50, 1500)
    return "Maria Jacinta", "Controle Renal Conservador", dieta, lista, alertas, macros

# ==============================================================================
# INTERFACE STREAMLIT
# ==============================================================================

st.set_page_config(page_title="Gerador Carla Santos", page_icon="🥗")

# Estilo visual da página (Verde/Dourado)
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f4f2;
    }
    .main-header {
        font-family: 'Helvetica';
        color: #384d21; /* Verde Oliva */
        text-align: center;
    }
    .stButton>button {
        background-color: #384d21;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>GERADOR DE PROTOCOLOS V8</h1>", unsafe_allow_html=True)
st.write("---")

# Seleção do Paciente
opcao = st.selectbox(
    "Selecione o Protocolo Modelo:",
    ["Stephanie (Ciclo de Carbos)", "Gabriel (Hipertrofia)", "Maria (Renal Conservador)"]
)

# Inputs Personalizáveis (Caso queira mudar o nome na hora)
st.subheader("Personalização")
novo_nome = st.text_input("Nome do Paciente (Deixe em branco para usar o padrão):")

# Carregar Dados
if "Stephanie" in opcao:
    nome_padrao, tipo, dieta, lista, alertas, macros = get_stephanie_data()
elif "Gabriel" in opcao:
    nome_padrao, tipo, dieta, lista, alertas, macros = get_gabriel_data()
elif "Maria" in opcao:
    nome_padrao, tipo, dieta, lista, alertas, macros = get_maria_data()

nome_final = novo_nome if novo_nome else nome_padrao

# Botão de Geração
if st.button("GERAR PDF AGORA"):
    with st.spinner('Gerando protocolo no Padrão V8...'):
        pdf_bytes = gerar_pdf_v8(nome_final, tipo, dieta, lista, alertas, macros)
        
        st.success("PDF Gerado com Sucesso!")
        st.download_button(
            label="⬇️ BAIXAR PDF PRONTO",
            data=pdf_bytes,
            file_name=f"PROTOCOLO_{nome_final.replace(' ', '_').upper()}.pdf",
            mime="application/pdf"
        )

# Rodapé
st.markdown("<br><br><center><small>Desenvolvido para Carla Santos Nutrição</small></center>", unsafe_allow_html=True)

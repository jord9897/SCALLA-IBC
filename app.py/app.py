import datetime
import pandas as pd
import streamlit as st

# Configuração da página com layout largo e ícone moderno
st.set_page_config(
    page_title="SCALLA - Gestão de Cultos", page_icon="🎵", layout="wide"
)

# Estilo visual moderno com CSS customizado (deixa os botões e caixas mais bonitos)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Banco de dados temporário na sessão
if "disponibilidades" not in st.session_state:
  st.session_state.disponibilidades = pd.DataFrame(
      columns=["Nome", "Instrumento/Função", "Data", "Observação"]
  )

if "cultos" not in st.session_state:
  st.session_state.cultos = {}

# Título Principal do App
st.title("🎵 SCALLA - Gestão de Cultos & Escalas")
st.markdown("Plataforma oficial da base de adoração para alinhamento e escalas.")
st.markdown("---")

# Abas Modernas no Topo (substitui a setinha lateral)
aba1, aba2, aba3 = st.tabs([
    "📝 Enviar Disponibilidade", 
    "⚙️ Painel do Líder", 
    "🎼 Ordem & Repertório"
])

# ---------------------------------------------------------
# 1. ENVIAR DISPONIBILIDADE
# ---------------------------------------------------------
with aba1:
  st.subheader("Informe sua Disponibilidade")
  st.write("Preencha os campos abaixo para informar em quais cultos você poderá servir.")

  with st.form("form_disponibilidade", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
      nome = st.text_input("Seu Nome Completo")
      instrumento = st.selectbox(
          "Instrumento / Função",
          [
              "Violão",
              "Guitarra",
              "Baixo",
              "Bateria",
              "Teclado",
              "Vocal / Backing",
              "Multimídia / Projeção",
              "Recepção / Áudio",
          ],
      )
    
    with col2:
      data_culto = st.date_input(
          "Data do Culto", min_value=datetime.date.today()
      )
      obs = st.text_area("Observação (ex: Posso apenas no culto da noite)")

    enviado = st.form_submit_button("Enviar Minha Disponibilidade 🚀")

    if enviado:
      if nome.strip() == "":
        st.warning("Por favor, preencha o seu nome antes de enviar.")
      else:
        nova_linha = pd.DataFrame(
            [[nome, instrumento, data_culto, obs]],
            columns=["Nome", "Instrumento/Função", "Data", "Observação"],
        )
        st.session_state.disponibilidades = pd.concat(
            [st.session_state.disponibilidades, nova_linha], ignore_index=True
        )
        st.success(
            f"Obrigado, {nome}! Sua disponibilidade foi registrada com sucesso."
        )

# ---------------------------------------------------------
# 2. PAINEL DO LÍDER (Com senha de proteção)
# ---------------------------------------------------------
with aba2:
  st.subheader("Painel de Controle Exclusivo do Líder")
  
  # Sistema simples de senha para proteger o painel
  senha_digitada = st.text_input("Digite a senha do líder para acessar:", type="password")
  
  # Defina a sua senha aqui (ex: "scalla2026")
  SENHA_MESTRE = "scalla2026" 

  if senha_digitada == SENHA_MESTRE:
    st.success("Acesso autorizado, líder! 🔓")
    
    df = st.session_state.disponibilidades

    if df.empty:
      st.info("Ainda não há disponibilidades cadastradas pela equipe.")
    else:
      st.markdown("### 📋 Respostas Recebidas")
      st.dataframe(df, use_container_width=True)

      st.markdown("---")
      st.markdown("### 📱 Gerar Escala para o WhatsApp")

      df["Data_Str"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")
      datas_disponiveis = df["Data_Str"].unique()

      data_escolhida = st.selectbox(
          "Selecione a data do culto",
          datas_disponiveis,
      )

      df_filtrado = df[df["Data_Str"] == data_escolhida]

      texto_whatsapp = f"*ESCALA DE CULTO - {data_escolhida}* 🎵\n\n"
      texto_whatsapp += "Olá equipe! Segue a nossa escala confirmada para este domingo:\n\n"

      for _, row in df_filtrado.iterrows():
        texto_whatsapp += f"▪ *{row['Instrumento/Função']}:* {row['Nome']}\n"
        if pd.notna(row["Observação"]) and row["Observação"].strip() != "":
          texto_whatsapp += f"  *(Obs: {row['Observação']})*\n"

      texto_whatsapp += "\nDeus abençoe a todos! 🙏"

      st.text_area(
          "Copie o texto abaixo e cole no grupo do WhatsApp:",
          value=texto_whatsapp,
          height=200,
      )

      st.markdown("---")
      if st.button("Limpar Todos os Registros de Disponibilidade"):
        st.session_state.disponibilidades = pd.DataFrame(
            columns=["Nome", "Instrumento/Função", "Data", "Observação"]
        )
        st.rerun()
  elif senha_digitada != "":
    st.error("Senha incorreta. Apenas o líder tem acesso a este painel.")
  else:
    st.info("Digite a senha acima para visualizar as disponibilidades da equipe.")

# ---------------------------------------------------------
# 3. ORDEM DE CULTO & REPERTÓRIO
# ---------------------------------------------------------
with aba3:
  st.subheader("Montagem da Liturgia e Repertório")

  data_selecionada = st.date_input(
      "Selecione a data do culto para montar o repertório",
      min_value=datetime.date.today(),
      key="data_culto_rep",
  )

  data_str = str(data_selecionada)

  if data_str not in st.session_state.cultos:
    st.session_state.cultos[data_str] = {
        "ordem": "1. Boas-vindas\n2. Louvor (3 músicas)\n3. Oração\n4. Palavra\n5. Ceia/Encerramento",
        "repertorio": "- Nome da Música 1 (Tom: C)\n- Nome da Música 2 (Tom: G)",
    }

  culto_atual = st.session_state.cultos[data_str]

  with st.form("form_culto"):
    ordem_culto = st.text_area(
        "Ordem do Culto (Passo a passo)",
    ...

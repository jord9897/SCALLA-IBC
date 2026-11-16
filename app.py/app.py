import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestão de Cultos e Escalas", page_icon="🎵", layout="wide"
)

if "disponibilidades" not in st.session_state:
  st.session_state.disponibilidades = pd.DataFrame(
      columns=["Nome", "Instrumento/Função", "Data", "Observação"]
  )

if "cultos" not in st.session_state:
  st.session_state.cultos = {}

st.title("🎵 Gerenciamento de Cultos & Escalas")
st.write(
    "Plataforma centralizada para envio de disponibilidades, montagem de"
    " repertório e escalas."
)

menu = st.sidebar.selectbox(
    "Menu",
    [
        "📝 Enviar Disponibilidade",
        "⚙️ Painel do Líder (Escalas)",
        "🎼 Ordem de Culto & Repertório",
    ],
)

if menu == "📝 Enviar Disponibilidade":
  st.subheader("Informe sua Disponibilidade para os Próximos Cultos")

  with st.form("form_disponibilidade"):
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
    data_culto = st.date_input(
        "Data do Culto", min_value=datetime.date.today()
    )
    obs = st.text_area("Observação (ex: Posso apenas no culto da noite)")

    enviado = st.form_submit_button("Enviar Disponibilidade")

    if enviado:
      if nome.strip() == "":
        st.warning("Por favor, preencha o seu nome.")
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

elif menu == "⚙️ Painel do Líder (Escalas)":
  st.subheader("Painel de Controle - Disponibilidades Recebidas")

  df = st.session_state.disponibilidades

  if df.empty:
    st.info("Ainda não há disponibilidades cadastradas.")
  else:
    st.dataframe(df, use_container_width=True)

    if st.button("Limpar Todos os Registros"):
      st.session_state.disponibilidades = pd.DataFrame(
          columns=["Nome", "Instrumento/Função", "Data", "Observação"]
      )
      st.rerun()

elif menu == "🎼 Ordem de Culto & Repertório":
  st.subheader("Montagem da Liturgia e Repertório")

  data_selecionada = st.date_input(
      "Selecione a data do culto",
      min_value=datetime.date.today(),
      key="data_culto",
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
        value=culto_atual["ordem"],
        height=150,
    )
    repertorio_culto = st.text_area(
        "Repertório de Louvor (Músicas e Tons)",
        value=culto_atual["repertorio"],
        height=150,
    )

    salvar_culto = st.form_submit_button("Salvar Culto e Repertório")

    if salvar_culto:
      st.session_state.cultos[data_str] = {
          "ordem": ordem_culto,
          "repertorio": repertorio_culto,
      }
      st.success(
          f"Ordem e repertório salvos com sucesso para a data {data_str}!"
      )

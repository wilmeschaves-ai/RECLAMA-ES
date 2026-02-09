import streamlit as st
import pandas as pd
import os

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


file_name = "reclamacoes.xlsx"


def carregar_dados():
    if os.path.exists(file_name):
        return pd.read_excel(file_name)
    else:
        return pd.DataFrame(
            columns=[
                "Matrícula",
                "Nome",
                "Telefone",
                "Secretaria",
                "Regime",
                "Data",
                "Situação",
                "Descrição",
            ]
        )


def salvar_dados(df):
    df.to_excel(file_name, index=False)


# Inicializar valores padrão para o formulário
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "matricula": "",
        "nome": "",
        "telefone": "",
        "secretaria": "",
        "regime": "",
        "data": pd.Timestamp.today().date(),
        "situacao": "",
        "descricao": "",
    }

# configuração da página
st.set_page_config(page_title="Reclamações", layout="centered")

st.image("logo.png", width=100)
st.title("SERVIDORES - RECLAMAÇÕES")

st.markdown(
    """ 
Preencher os dados corretamente para registrar uma reclamação.

**Todos os campos são obrigatórios.**             
    """
)

# formulário de reclamação
with st.form(key="form_reclamacao"):
    matricula = st.text_input(
        "Matrícula do servidor", value=st.session_state.form_data["matricula"]
    )

    nome = st.text_input("Nome do servidor", value=st.session_state.form_data["nome"])

    telefone = st.text_input(
        "Telefone do servidor", value=st.session_state.form_data["telefone"]
    )

    secretaria = st.text_input(
        "Secretaria do servidor", value=st.session_state.form_data["secretaria"]
    )

    regime = st.radio(
        "Regime do servidor",
        options=["Contrato", "Estatutário", "Comissionado"],
        index=(
            0
            if st.session_state.form_data["regime"] == "Contrato"
            else (1 if st.session_state.form_data["regime"] == "Estatutário" else 0)
        ),
    )

    data = st.date_input(
        "Data da reclamação",
        value=(
            pd.Timestamp(st.session_state.form_data["data"]).date()
            if st.session_state.form_data["data"]
            else pd.Timestamp.today().date()
        ),
    )

    situacao = st.radio(
        "Situação da reclamação",
        options=["Pendente", "Em andamento", "Concluída"],
        index=(
            0
            if st.session_state.form_data["situacao"] == "Pendente"
            else (1 if st.session_state.form_data["situacao"] == "Em andamento" else 0)
        ),
    )

    descricao = st.text_area(
        "Descrição da reclamação", value=st.session_state.form_data["descricao"]
    )

    submited = st.form_submit_button(label="Registrar Reclamação")

    if submited:

        if (
            not matricula.strip()
            or not nome.strip()
            or not telefone.strip()
            or not secretaria.strip()
            or not descricao.strip()
        ):
            st.warning("Por favor, preencha os campos")
        else:
            df = carregar_dados()

            nova_consulta = pd.DataFrame(
                [
                    [
                        matricula,
                        nome,
                        telefone,
                        secretaria,
                        regime,
                        data,
                        situacao,
                        descricao,
                    ]
                ],
                columns=[
                    "Matrícula",
                    "Nome",
                    "Telefone",
                    "Secretaria",
                    "Regime",
                    "Data",
                    "Situação",
                    "Descrição",
                ],
            )

            df = pd.concat([df, nova_consulta], ignore_index=True)
            salvar_dados(df)
            st.success("Reclamação registrada com sucesso!")

            # Resetar o formulário
            st.session_state.form_data = {
                "matricula": "",
                "nome": "",
                "telefone": "",
                "secretaria": "",
                "regime": "",
                "data": pd.Timestamp.today().date(),
                "situacao": "",
                "descricao": "",
            }
            st.rerun()
st.subheader("Reclamações Registradas")

df = carregar_dados()
if not df.empty:

    # opção de deletar reclamação

    nomes = df["Nome"].tolist()
    consulta_selecionada = st.selectbox(
        "Selecione a reclamação para deletar", options=nomes
    )

    if st.button("Deletar Reclamação"):
        df = df[df["Nome"] != consulta_selecionada]
        salvar_dados(df)
        st.success("Reclamação deletada com sucesso!")
        st.rerun()

    st.dataframe(df, use_container_width=True)

    # st.dataframe(df[["Matrícula", "Nome", "Telefone", "Secretaria", "Regime", "Data", "Situação"]])
else:
    st.info("Nenhuma reclamação registrada ainda.")

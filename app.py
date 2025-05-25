import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MINHA CASA PRE FABRICADA BAHIA - Simular Vendas",
    page_icon="favicon.png",
    layout="wide"
)

# Logo e título lado a lado
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    st.image('logo.png', width=100)  # Ajuste conforme tamanho do seu logo

with col_titulo:
    st.title("🏠 MINHA CASA PRE FABRICADA BAHIA - Simular Vendas")

# Função para formatar moeda brasileira
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Cache para carregar dados
@st.cache_data
def load_data(uploaded_file):
    return pd.read_excel(uploaded_file)

# Upload da planilha
uploaded_file = st.file_uploader("📤 Faça o upload da planilha de preços:", type="xlsx")

if uploaded_file is not None:
    df = load_data(uploaded_file)

    busca = st.text_input("🔍 Digite parte da descrição do produto:")

    # Filtra descrições que contêm a busca
    filtro = df[df['DESCRICAO'].str.contains(busca, case=False, na=False)]

    if not filtro.empty:
        descricao_selecionada = st.selectbox("📝 Selecione a descrição:", filtro['DESCRICAO'])

        if descricao_selecionada:
            produto = df[df['DESCRICAO'] == descricao_selecionada].iloc[0]

            preco_venda = produto['A VISTA']
            preco_custo = produto['PRECO_CUSTO']
            icms = produto['ICMS_RS']
            custo_total = produto['CUSTO_TOTAL']
            lucro_atual = produto['LUCRO_RS']
            lucro_percent = produto['LUCRO_%']
            preco_minimo = produto['PRECO_MINIMO_RS']
            desconto_maximo = produto['DESC_MAX_RS']
            desconto_max_percent = produto['DESC_MAX_%']
            frete = produto['FRETE']

            total_com_frete = preco_venda + frete

            st.header(f"📋 {descricao_selecionada}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"💰 **Preço de Venda:** {formatar_moeda(preco_venda)}")
                st.write(f"🛠️ **Preço de Custo:** {formatar_moeda(preco_custo)}")
                st.write(f"🏦 **ICMS:** {formatar_moeda(icms)}")
                st.write(f"🧾 **Custo Total:** {formatar_moeda(custo_total)}")
                st.write(f"💹 **Lucro Atual:** {formatar_moeda(lucro_atual)} ({lucro_percent:.2f}%)")

            with col2:
                st.write(f"💸 **Preço Mínimo:** {formatar_moeda(preco_minimo)}")
                st.write(f"📉 **Desconto Máximo:** {formatar_moeda(desconto_maximo)} ({desconto_max_percent:.2f}%)")
                st.write(f"🚚 **Frete:** {formatar_moeda(frete)}")
                st.write(f"🛍️ **Total com Frete:** {formatar_moeda(total_com_frete)}")

            st.subheader("🛠️ Ajuste de Percentuais:")

            icms_percent = st.number_input("🏦 ICMS %", value=20.5)
            corretor_percent = st.number_input("👨‍💼 Corretor %", value=3.0)
            royalties_percent = st.number_input("📢 Royalties + Propaganda %", value=9.0)
            simples_percent = st.number_input("🏛️ Simples Nacional %", value=4.5)
            adm_percent = st.number_input("📋 Despesas Administrativas %", value=5.0)

            despesas_variaveis_percent = corretor_percent + royalties_percent + simples_percent + adm_percent

            st.subheader("💡 Simulações de Desconto com Frete:")

            opcoes_desconto = [5, 7, 10]
            for desc in opcoes_desconto:
                preco_com_desc = preco_venda * (1 - desc / 100)
                total_com_frete_desc = preco_com_desc + frete

                # Lucro calculado sem considerar o frete
                despesas_desc = preco_com_desc * (despesas_variaveis_percent / 100)
                custo_completo_desc = preco_custo + (preco_custo * (icms_percent / 100)) + despesas_desc
                lucro_desc = preco_com_desc - custo_completo_desc
                lucro_perc_desc = (lucro_desc / preco_com_desc) * 100

                with st.container():
                    st.write(f"🔸 **Desconto {desc}%:**")
                    st.write(f"➡️ Preço: {formatar_moeda(preco_com_desc)}")
                    st.write(f"➡️ 🚚 Frete: {formatar_moeda(frete)}")
                    st.write(f"➡️ 🛍️ Total com Frete: {formatar_moeda(total_com_frete_desc)}")
                    st.write(f"➡️ 💰 Lucro: {formatar_moeda(lucro_desc)} ({lucro_perc_desc:.2f}%)")
                    st.write("---")
    else:
        if busca:
            st.warning("⚠️ Nenhum produto encontrado com esse termo.")
else:
    st.info("📥 Faça upload de uma planilha para começar.")

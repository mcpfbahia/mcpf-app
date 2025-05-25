import streamlit as st
import pandas as pd

# Função para formatar moeda brasileira
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Carrega a planilha processada
df = pd.read_excel('mcpf_formacao_preco_processada.xlsx')

st.title("Consulta de Produto - MCPF")

busca = st.text_input("Digite parte da descrição do produto:")

# Filtra descrições que contêm a busca (case insensitive)
filtro = df[df['DESCRICAO'].str.contains(busca, case=False, na=False)]

if not filtro.empty:
    descricao_selecionada = st.selectbox("Selecione a descrição:", filtro['DESCRICAO'])

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

        st.subheader(f"{descricao_selecionada}")

        st.write(f"**Preço de Venda:** {formatar_moeda(preco_venda)}")
        st.write(f"**Preço de Custo:** {formatar_moeda(preco_custo)}")
        st.write(f"**ICMS:** {formatar_moeda(icms)}")
        st.write(f"**Custo Total:** {formatar_moeda(custo_total)}")
        st.write(f"**Lucro Atual:** {formatar_moeda(lucro_atual)} ({lucro_percent:.2f}%)")
        st.write(f"**Preço Mínimo:** {formatar_moeda(preco_minimo)}")
        st.write(f"**Desconto Máximo:** {formatar_moeda(desconto_maximo)} ({desconto_max_percent:.2f}%)")

        st.subheader("Simulações de Desconto")
        opcoes_desconto = [5, 7, 10]
        for desc in opcoes_desconto:
            preco_com_desc = preco_venda * (1 - desc / 100)
            despesas_variaveis_percent = 3 + 6 + 3 + 4.5 + 5
            despesas_desc = preco_com_desc * (despesas_variaveis_percent / 100)
            custo_completo_desc = preco_custo + (preco_custo * 0.215) + despesas_desc
            lucro_desc = preco_com_desc - custo_completo_desc
            lucro_perc_desc = (lucro_desc / preco_com_desc) * 100
            st.write(f"🔸 **Desconto {desc}%:** Preço {formatar_moeda(preco_com_desc)}, Lucro {formatar_moeda(lucro_desc)} ({lucro_perc_desc:.2f}%)")
else:
    if busca:
        st.warning("Nenhum produto encontrado com esse termo.")

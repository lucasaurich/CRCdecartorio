import re
from datetime import datetime
import streamlit as st

def process_text(text):
    # Pattern 1: First line of the text
    pattern1 = re.search(r"^(.*)$", text, re.MULTILINE)
    first_line = pattern1.group(1).strip() if pattern1 else ""

    # Pattern 2: Extract specified parts from the line immediately after Pattern 1
    pattern2 = re.search(r"^[^\n]*\n([^\n]*) - ([^\n]*) - ([A-Z]{2})", text, re.MULTILINE)
    if pattern2:
        before_first_dash = pattern2.group(1).strip()
        between_dashes = pattern2.group(2).strip()
        uppercase_letters = pattern2.group(3).strip()
        pattern2_text = f"{before_first_dash}, {between_dashes}, {uppercase_letters}"
    else:
        pattern2_text = ""

    # Pattern 3: The phrase "Código da comunicação" and the number following it
    pattern3 = re.search(r"(Código da comunicação:\s*\d+)", text, re.MULTILINE)
    codigo_comunicacao = pattern3.group(1).strip() if pattern3 else ""

    # Pattern 4: Everything after Pattern 3 until the word "OBSERVAÇÕES"
    pattern4 = re.search(r"Código da comunicação:\s*\d+\n+(.*?)(?=\nOBSERVAÇÕES:)", text, re.DOTALL)
    text_until_observacoes = pattern4.group(1).strip() if pattern4 else ""

    # Get today's date in the desired format
    todays_date = datetime.today().strftime("%d/%m/%Y")

    # Generate "Texto para o Livro"
    texto_para_o_livro = (f"ANOTAÇÃO: Conforme {first_line} recebida via CRC pelo Cartório de {pattern2_text}, "
                          f"{codigo_comunicacao}, fomos informados que no dia {text_until_observacoes}. "
                          f"O referido é verdade e dou fé. Cariacica-ES, {todays_date}. Eu, _____________ – Escrevente")

    # Generate "Texto para Certidão"
    texto_para_certidao = (f"ANOTAÇÃO: As margens do termo consta que conforme {first_line} recebida via CRC pelo Cartório de "
                           f"{pattern2_text}, {codigo_comunicacao} fomos informados que no dia {text_until_observacoes}. "
                           f"O referido é verdade e dou fé. Cariacica-ES, {todays_date}. Eu, (ass) – Escrevente.")

    return texto_para_o_livro, texto_para_certidao

def main():
    st.title("Processador de Comunicação de Casamento Civil")

    # Text input area
    text = st.text_area("Cole o texto da comunicação aqui:", height=300)

    if st.button("Processar"):
        if text:
            texto_para_o_livro, texto_para_certidao = process_text(text)

            st.subheader("Texto para o Livro:")
            st.text_area("", texto_para_o_livro, height=150)

            st.subheader("Texto para Certidão:")
            st.text_area("", texto_para_certidao, height=150)
        else:
            st.warning("Por favor, insira o texto da comunicação.")

if __name__ == "__main__":
    main()

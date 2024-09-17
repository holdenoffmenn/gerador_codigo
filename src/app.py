import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# Inicializa a "session_state" para controlar o estado do botão
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

def main():
    # Exibir logo e apresentação
    st.image("public/logo_light.svg", width=250)  # Substitua "logo.png" pelo caminho da sua logo
    st.title('Gerador de Código')
    st.write('Bem-vindo à nossa ferramenta. Por favor, insira seu email para continuar.')

    email = st.text_input('Email')

    if email:
        if "rd.com.br" in email or "rdsaude.com.br" in email:
            st.success('Email validado. Por favor, insira as seguintes informações:')
            gitlab_token = st.text_input('TOKEN do seu Gitlab')
            repository = st.text_input('Link para o Repositório Gitlab')
            gitlab_webhook_secret = st.text_input('Webhook Secret do seu Repositório Gitlab')
            code_informations = st.text_area('Informações do Código')

            if gitlab_token and repository and gitlab_webhook_secret and code_informations:
                # Controle do botão junto com estado clicado
                if st.button('Gerar Código', disabled=st.session_state.button_disabled) and not st.session_state.button_clicked:
                    st.session_state.button_clicked = True
                    st.session_state.button_disabled = True

                if st.session_state.button_clicked:
                    st.session_state.button_disabled = True
                    with st.spinner('Enviando informações...'):
                        time.sleep(2)  # Simulando tempo de envio
                        response = enviar_dados_para_api(email, gitlab_token, repository, gitlab_webhook_secret, code_informations)

                        if response['status'] == 'sucesso':
                            st.success('Sucesso! As informações foram enviadas corretamente.')
                            st.write(f"**Message:** {response['message']}")
                            st.write("**Arquivos Gerados:**")
                            files_list = response['generated_files']
                            for file in files_list:
                                st.write(f"- {file}")
                            st.write(f"**Merge Request URL:** [Clique aqui]({response['mr_url']})")
                        else:
                            st.error('Erro: O processo falhou. Tente novamente.')
                            time.sleep(4)  # Pequeno tempo para exibir a mensagem
                            st.rerun()

                    if st.button('Voltar'):
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        else:
            st.error('Erro: Email inválido. Use um email do domínio rd.com.br ou rdsaude.com.br.')

def enviar_dados_para_api(email, gitlab_token, repository, gitlab_webhook_secret, code_informations):
    url = 'https://integration-gitlab-405058905014.us-east1.run.app/process-and-create-pr'  # Substitua pela URL da sua API
    payload = {
        "user_input": code_informations,
        "gitlab_url": "https://gitlab.com",
        "gitlab_token": gitlab_token,
        "repository": repository,
        "gitlab_webhook_secret": gitlab_webhook_secret
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return {'status': 'sucesso', **response.json()}
        else:
            return {'status': 'erro', 'mensagem': response.text}
    except requests.exceptions.RequestException as e:
        return {'status': 'erro', 'mensagem': str(e)}


if __name__ == '__main__':
    main()
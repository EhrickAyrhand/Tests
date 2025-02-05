from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import time

# Lista de dados de teste
dados_teste = [
    {"nome": "João Silva", "email": "joao@email.com"},  # Válido
    {"nome": "", "email": "joao@email.com"},            # Nome vazio
    {"nome": "Maria Souza", "email": "maria@email"},    # E-mail inválido
    {"nome": "Teste 123", "email": "teste123@email.com"},  # Válido
]

# Configuração do driver (abre o navegador)
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Usa o ChromeDriver
    driver.get("https://www.kabum.com.br/")  # Substitua pela URL real da página
    driver.maximize_window()
    yield driver  # Retorna o driver para os testes
    driver.quit()  # Fecha o navegador no final dos testes

# Teste para validar o cadastro com diferentes dados
@pytest.mark.parametrize("dados", dados_teste)
def test_cadastro_newsletter(driver, dados):
    # Encontrar os campos e preenchê-los
    campo_botão = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    campo_nome = driver.find_element(By.ID, "formNewsletterName")
    campo_email = driver.find_element(By.ID, "formNewsletterEmail")
    botao_envio = driver.find_element(By.ID, "botaoEnvioNewsletter")

    campo_botão.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Limpa os campos antes de preencher
    campo_nome.clear()
    campo_email.clear()

    # Preenche os dados
    campo_nome.send_keys(dados["nome"])
    campo_email.send_keys(dados["email"])

    # Clica no botão de envio
    botao_envio.click()
    time.sleep(2)  # Aguarda carregamento da resposta

    # Verifica se há uma mensagem de erro ou sucesso
    try:
        mensagem = driver.find_element(By.CLASS_NAME, "classe_mensagem")  # Substitua pela classe correta
        assert "sucesso" in mensagem.text.lower() or "erro" in mensagem.text.lower()
    except:
        pytest.fail("Nenhuma mensagem de resposta encontrada")

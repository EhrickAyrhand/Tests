from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    wait = WebDriverWait(driver, 10)  # Aguarda até 10 segundos

    # Aceitar cookies se necessário
    try:
        botao_cookies = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        botao_cookies.click()
    except:
        print("Nenhum botão de cookies encontrado")

    # Encontrar os campos do formulário
    campo_nome = wait.until(EC.presence_of_element_located((By.ID, "formNewsletterName")))
    campo_email = driver.find_element(By.ID, "formNewsletterEmail")
    botao_envio = driver.find_element(By.ID, "botaoEnvioNewsletter")

    # Rolar a página até o final para garantir visibilidade
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_nome)
    time.sleep(10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_envio)


    # Limpa os campos antes de preencher
    campo_nome.clear()
    campo_email.clear()

    # Preenche os dados
    campo_nome.send_keys(dados["nome"])
    campo_email.send_keys(dados["email"])

    # Clica no botão de envio
    botao_envio.click()

    # Aguarda a mensagem de resposta aparecer
    try:
        mensagem = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(normalize-space(), 'Pronto, agora você receberá ofertas exclusivas no e-mail')]")
        ))

        # Verifica se o texto contém "sucesso" ou "erro"
        assert "sucesso" in mensagem.text.lower() or "erro" in mensagem.text.lower(), "Mensagem inesperada"

    except:
        pytest.fail("❌ Nenhuma mensagem de resposta encontrada")


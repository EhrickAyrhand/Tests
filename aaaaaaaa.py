from selenium import webdriver

driver = webdriver.Chrome()  # Abre o navegador
driver.get("https://www.google.com")  # Abre o Google
driver.quit()  # Fecha o navegador

from factory import create_app  # Importa a função create_app do módulo factory

app = create_app()  # Cria a aplicação Flask utilizando a função create_app

if __name__ == "__main__":
    app.run(debug=True)  # Executa a aplicação em modo de depuração se o script for executado diretamente

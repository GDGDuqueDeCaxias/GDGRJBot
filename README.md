# GDG Aracaju Bot

Bot de Telegram

## Dependências:

- Python 3.4
- Instalar as dependências via `pip install -r requirements.txt`

## Uso:

- Instalar as dependências
- Falar com o @BotFather no Telegram e criar seu bot através dos comandos disponíveis nele
- Inserir o token de uma das formas:
  - Sobrescrever o dicionário defaults
  - Passar por parâmetros via --telegram_token, --meetup_key, --group_name
  - Incluir nas variáveis de ambiente via TELEGRAM_TOKEN, MEETUP_KEY, GROUP_NAME
- Rodar o código `python gdgajubot.py`
- Falar com o seu bot no Telegram para testar

## Dependências no Windows

- A lib `lxml` pode ser difícil de instalar via pip. Tente baixar o binário através do [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)

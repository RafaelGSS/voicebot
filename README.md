# VOICEBOT

Projeto realizado para integrar com o APP com o intuito de transformar seu pedido por voz em venda.

---

## API

WSGI rodando na porta especificada no **env.py** que contém as seguintes rotas:

**Actions**:
    
    - ASK_AGAIN
    - ASK_STATE
    - NEXT

* /api/voice/city - **GET** 
  * **station_name** [Obrigatório]
    *  Cidade 
    * Respostas:
    * ``` {	“action” 	: “ASK_AGAIN” }``` Caso não encontre uma cidade "match"
    * ``` {	“value” 	: 2, “action” 	: “NEXT” }``` Retorna ID da cidade "match"
    * ``` {	“value”			: “1, 2”, “action” 			: “ASK_STATE” }``` Caso a cidade "match" contenha em mais de um estado. Retorna ID das cidades no qual houveram "match"
    

* /api/voice/state - **GET**
    * **station_name** [Obrigatório] *Cidade falada anteriormente*
    * **state_name** [Obrigatório] *Estado*
    * Respostas:
    * ``` {	“action” 	: “ASK_AGAIN” }``` Caso não encontre uma cidade "match"
    * ``` {	“value” 	: 2, “action” 	: “NEXT” }``` Retorna ID da cidade "match"


* /api/voice/date - **GET**
    * **date** [Obrigatório] *Data*
    * Respostas:
    * ``` {	“value” : “2018-08-10”,	“action” : “NEXT” }``` Retorna data "match"


---
## Dependências e Configuração

Necessita de uma versão do **Python 3.5^**


Instalação de módulos:
```
pip install -r requeriments.txt
```

## Iniciando aplicação

### Rodando Migration

Após a configuração de um banco de dados mysql localhost

Setar suas configurações no **env.py** juntamente com o nome da database criada.

Para rodar a migration basta executar o arquivo **run.py** presente na pasta

```
- app
    - database
        - migrations
            - base
                - run.py
```

---

### Rodando aplicação
O Flask por padrão está rodando na porta **5000**, se necessário é possível mudar 
basta ir no **env.py**


Toda configuração com **banco de dados**  reside no arquivo **env.py** na raiz.

Para rodar a aplicação basta executar o arquivo **main.py** na raiz

```
- app
main.py
```

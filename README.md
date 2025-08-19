```markdown
# 📡 Monitor Diário MG

Este projeto realiza o monitoramento automatizado do Diário Oficial de Minas Gerais, buscando por palavras-chave específicas e enviando alertas via WhatsApp utilizando a API gratuita do [CallMeBot](https://www.callmebot.com/).

---

## 🚀 Funcionalidades

- Acessa diariamente o Diário Oficial de MG
- Busca por palavras-chave definidas pelo usuário
- Envia notificações via WhatsApp com os resultados encontrados
- Fácil de configurar e executar localmente

---

## 🛠️ Requisitos

- Python 3.8+
- Conexão com a internet
- Conta no WhatsApp
- Chave de API do CallMeBot

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone git@github.com-outlook:catrique/monitor-diario-mg.git
cd monitor-diario-mg
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔑 Como obter a API Key do CallMeBot

1. Salve o número do CallMeBot na sua agenda do WhatsApp: `+34 644 52 74 88`
2. Envie a seguinte mensagem para ele via WhatsApp:

```
I allow callmebot to send me messages
```

3. Você receberá uma resposta com sua `api_key`, algo como:

```
Your API key is: 123456
```

4. Guarde essa chave com segurança. Você vai usá-la no script para enviar mensagens.

---

## 🧪 Execução

Para rodar o monitoramento:

```bash
python monitor-diario-mg.py
```

O script buscará as palavras-chave no Diário Oficial e enviará uma mensagem via WhatsApp se encontrar algo relevante.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e compartilhar.

---

## 🤝 Contribuições

Pull requests são bem-vindos! Se tiver sugestões ou melhorias, fique à vontade para abrir uma issue.

---

## 📬 Contato

Criado por [Cáled Tarique](https://github.com/CaledTarique)  
Dúvidas ou sugestões? Me chama no WhatsApp ou abre uma issue aqui no GitHub!

```
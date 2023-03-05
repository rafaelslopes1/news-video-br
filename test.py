from newspaper import Config
from newspaper import Article
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 15

url = 'https://www.poder360.com.br/brasil/eu-sou-o-ex-mais-amado-do-brasil-diz-bolsonaro-nos-eua/'


def remove_blank_lines(content):
    all_lines = content.split('\n')
    without_blank_lines = list(filter(
        lambda line: len(line.strip()) != 0, all_lines))
    return without_blank_lines


article = Article(url.strip(), config=config)
article.download()
article.parse()
article.nlp()

without_blank_lines = remove_blank_lines(article.text)

base_messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant who sanitizes news articles. \
          The response cannot have escape characters, and must be plain text, with no line breaks."
    },
    {
        "role": "user",
        "content": "Reescreva a notícia abaixo em português brasileiro. \
          O novo texto deve ser otimizado para uma narração de vídeo de \
          notícia no Youtube, de forma a aumentar a retenção do público, \
          contendo uma linguagem de fácil compreenssão, dividido em parágrafos,\
          e mantendo riqueza de informações e o tom de seriedade. \
          Ele deve conter no mínimo 1300 caracteres, e deve ser pouco \
          redundante. Remova, do novo texto, qualquer referência ao jornal \
          que publicou a notícia. \
          O novo texto deve ser limpo, removendo quaisquer informações fora \
          do contexto da notícia, como propagandas, chamadas para ação, \
          descrição de imagens e links, mas sem encurtando-lo tanto. O novo \
          texto também deve ser escrito de forma a diminuir as chances de \
          problemas com o algoritmo do Youtube: \n{}".format(without_blank_lines)
    }
]

sanetized_article_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.4,
    messages=base_messages
)

article = sanetized_article_response.choices[0].message.content

base_messages.append({
    "role": "assistant",
    "content": article
})

base_messages.append({
    "role": "user",
    "content": "Escreva um título baseado no texto. \
  O título deve ser chamativo para um vídeo do Youtube, com no máximo \
  70 caracteres, sendo o mais específico possível, contendo números, \
  quando houverem números relevantes na notícia, e deve possuir \
  adjetivos fortes."
})

title_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.8,
    messages=base_messages
)

title = title_response.choices[0].message.content

base_messages.append({
    "role": "assistant",
    "content": title
})

base_messages.append({
    "role": "user",
    "content": "Escreva uma descrição de vídeo do Youtube, baseada no \
  texto. Ela deve ser um resumo conciso do texto, com no máximo 300 \
  caracteres"
})

description_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.8,
    messages=base_messages
)

description = description_response.choices[0].message.content

base_messages.append({
    "role": "assistant",
    "content": description
})

base_messages.append({
    "role": "user",
    "content": "Responda com as palavras-chave dessa notícia, em um texto \
    simples, com as palavras-chave separadas por vírgula"
})

keywords_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.8,
    messages=base_messages
)

keywords = keywords_response.choices[0].message.content

print(title)
print('\n\n')
print(description)
print('\n\n')
print(article)
print('\n\n')
print(keywords)

# print(article.title)
# print(article.text)

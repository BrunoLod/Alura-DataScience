# -*- coding: utf-8 -*-
"""📚 Introdução ao PLN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11Kxt3Igpvz7AUmomgAQFMykb6fgEVG_Y

### 📚 Introdução ao Processamento de Linguagem Natural (PLN):

Olá! Bem-vindas e bem vindos ao fascinante mundo do Processamento de Linguagem Natural (PLN)! Nesta jornada, irei explorar os passos necessários que fornecem aos computadores a capacidade de entender e processar a linguagem humana.

🗣️ A linguagem humana é incrivelmente complexa e rica em nuances. Compreender e interpretar corretamente textos, conversas e até mesmo o tom de voz é uma habilidade natural para nós, seres humanos. No entanto, para os computadores, essa tarefa é muito mais desafiadora.

🤖 O PLN é um campo da inteligência artificial (IA) que se concentra em desenvolver algoritmos e técnicas para permitir que os computadores compreendam, analisem e gerem texto de maneira semelhante aos humanos. Ele abrange uma ampla gama de aplicações, desde assistentes virtuais e tradutores automáticos até sistemas de recomendação e análise de sentimentos.

💡 Com o PLN, podemos automatizar tarefas tediosas, extrair insights valiosos de grandes volumes de dados não estruturados e melhorar a interação entre humanos e máquinas. Ele desempenha um papel fundamental em muitos aspectos da nossa vida cotidiana, desde pesquisas na web até assistentes pessoais em nossos dispositivos móveis.

🚀 Ao longo desta jornada, para ilustrar o processo da compreensão dos computadores acerca dos textos, irei utilizar de um dataframe contraído no Kaggle. O objetivo será criar um modelo de Machine Learning que apresente uma boa acurácia na classificação de uma resenha em relação a sentimentos positvos ou negativos.

### Importando as bibliotecas que serão necessárias ao estudo: 🏛️
"""

import nltk
import string
import unicodedata
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from nltk import ngrams
from nltk import tokenize
from wordcloud import WordCloud
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

"""# Carregando o dataframe e verificando a sua estrutura e proporção dos rótulos : 🔍"""

df = pd.read_csv("/content/imdb-reviews-pt-br.csv")

df.head()

def verificaDataFrame(df):

  if df.duplicated().sum() != 0 and df.isna().sum() != 0:

    qt_duplicados = df.duplicated().sum()
    qt_nulos = df.isna().sum()

    print("O dataframe apresenta dados duplicados e nulos")
    print(f"{qt_duplicados} dados duplicados. ")
    print(f"{qt_nulos} dados nulos")
    print("Por padrão, realizarei a exclusão deles, mas a depender de cada cenário \n uma outra abordagem pode ser necessária.")

    df = df.drop_duplicates()
    df = df.dropna()

    return df

  else:

    print("O dataframe não apresenta dados duplicados.")
    print("Aqui está o seu formato: \n")
    print(df.shape)

verificaDataFrame(df)

"""- Proporção dos dados: ⚖️

Essa etapa é importante, pois caso os dados estejam desbalanceados, a análise do modelo de machine learning pode ser interferido, dando a ele viés em suas previsões. Nesse cenário em que há o desbalanceamento, deve-se adotar uma outra abordagem, segundo a qual fomente uma proporcionalidade dos dados da variável target.
"""

# Calcular a contagem de valores da coluna 'sentiment'
contagem_sentimentos = df['sentiment'].value_counts()

# Definir os dados para o gráfico de pizza
dados_grafico = go.Pie(labels=contagem_sentimentos.index,
                       values=contagem_sentimentos.values,
                       hoverinfo='label+percent',
                       textinfo='percent',
                       textfont=dict(size=20),
                       hole=0.3,
                       pull=[0.1, 0])

# Definir o layout do gráfico
layout = go.Layout(title='Distribuição de Sentimentos',
                   margin=dict(l=0, r=0, t=30, b=0),
                   title_y=0.9)

# Criar a figura do gráfico de pizza
figura = go.Figure(data=[dados_grafico], layout=layout)

# Exibir o gráfico
figura.show()

"""### Remodelando o dataframe:

Criando uma coluna, que carregará a mesma semântica da coluna "sentimento", porém em termos numéricos, para se aproximar do que é utilizado segundo o Estado da Arte.
"""

df["classificacao"] = df["sentiment"].replace(["neg", "pos"], [0,1])
df.head()

"""- Analisando brevemente duas resenhas para verificar como são: 🔬"""

df.text_pt[0]

df.text_pt[2]

"""### Passando a entrada de texto ao modelo: ➡️

Certo, eu possuo o dataframe e o texto da resenha em português parece estar consistente. Desse modo, como posso passá-lo efetivamente ao modelo ? Basta segmentar numa porção de *treino* e *teste* e instanciar um modelo  de machine learning ? Não, antes de realizar esse processo, deve-se vetorizar o texto, que em termos práticos significa extrair cada palavra do texto, passando posteriormente ao processo de "vocabularização", formando uma bag of words, que informa a quantidade de vezes que uma palavra está presente ao texto. Vejamos :

- Vetorização :
"""

texto = ["Assisti um filme ótimo", "Assisti a um filme ruim",
         "Assisti a um filme muito muito bom", "Assisti a um filme paia"]

vetorizar = CountVectorizer()

vetorizar.fit_transform(texto)

vetorizar.get_feature_names_out()

"""- "Vocabularização" :"""

bag_of_words = vetorizar.fit_transform(texto)

matriz_esparsa = pd.DataFrame.sparse.from_spmatrix(bag_of_words,
                                        columns = vetorizar.get_feature_names_out())

matriz_esparsa

"""No dataframe acima, é possível perceber o que havia comentado. Tomando como a lista texto anteriormente passada, nota-se que a quantidade de vezes em que cada palavra esteve presente numa frase.

- OBS❗️

Percebeu que o nome da variável é matriz esparsa ? Isso não ocorre a toa. No processo de "vocabularização", que é perpassado pela vetorização do texto, palavras ou termos, no sentido mais genérico, que não estão presentes na frase recebem um valor nulo, que o algorítimo atribui como zero. O nome de uma matriz na qual apresenta alguns elementos diferentes de zero, mas muitos zeros é justamente matriz esparsa.

### Retornando ao dataframe: 🔙
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# bag_of_words = vetorizar.fit_transform(df.text_pt)
# bag_of_words.shape

"""⚠️

Segundo a saída acima, nota-se que temos uma matriz de alta dimensionalidade, em especial a quantidade de colunas, que é de 129.6k aproximadamente. Isso acarreta numa elevada exigência de processamento, que pode tornar o processo computacional oneroso.

Desse modo, recomenda-se a diminuição de features (no que tange as colunas), as quais, apesar de prover uma matriz com menor dimensão, conseguem ser eficazes à análise. Estarei utilizando para esse presente estudo uma max_feature de 50.

- Baseline 📏

> Modelo que representa a baseline do projeto, o ponto inicial, por meio do qual, ao final e ao decorrer do processo poderemos comparar o ganho e/ou perda relativa de acurácia, se ocorrer.
"""

def classificar_texto(df, texto, classificacao):

    vetorizar = CountVectorizer(max_features=50)

    bag_of_words = vetorizar.fit_transform(df[texto])

    # Segmentando os dados na sua porção treino e teste, da parte do dataframe
    # que me é pertinente, sendo a coluna em português. Em seguida, o outro parâmetro,
    # passo a proporção que deve ser seguida, que é a variável target do df.

    train, test, X_train, y_test = train_test_split(bag_of_words,
                                                df.classificacao,
                                                random_state = 22)

    # Modelo de regressão logística para prever um texto de teste
    # a que rótulo ele pertence: positivo ou negativo.

    regressao_logistica = LogisticRegression()
    regressao_logistica.fit(train, X_train)

    # Mensurando a acurácia do modelo:
    acuracia = round(regressao_logistica.score(test, y_test), 3)

    print(f"O modelo de baseline apresenta uma acurácia aproximada de {acuracia*100} %")
    print("")

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# classificar_texto(df, "text_pt", "classificacao")

"""# Tratamento 🏥     

Ok, eu já tenho o dataframe e um modelo de baseline. Há algo a mais que possa ser feito ou é simplesmente isso o PLN ? Não, há algumas coisas, pelo menos nessa introdução, que podem ser feitas, as quais irão se debruçar tanto pelo **tratamento do texto** em si, quanto daquilo que servirá de **entrada** ao modelo de regressão logística.

Na etapa de tratamento do texto, temos que visar um meio com o qual a mensagem possa ser o tão mais eficiente possível, sem perder seu conteúdo semântico, de modo que torne o modelo habilitado a generalizar e a identificar padrões, contribuindo positivamente com a sua análise. Esquematicamente para essa etapa, tem-se:
- tokenização;
- remoção das stopword, pontuação e acentuação;
- processo de stemming (encontrar o radical das palavras)  
>

Por outro lado, na esfera da entrada dos dados do modelo, há justamente o tratamento desses, que incide sobre os pesos dados às palavras que compõem o texto (TF-IDF) e sua sequência lógica (N-Gramns).

- Verificando as palavras mais frequentes do dataframe 🔬

Mas antes de seguir às etapas de tratamento, cabe uma rápida visualização acerca das palavras que são mais frequentes no dataframe.
"""

# Commented out IPython magic to ensure Python compatibility.
# # Nuvem de palavras:
# 
# %%time
# 
# from wordcloud import WordCloud
# 
# # Criando um conjunto que tenha todas as palavras de todas as resenhas do
# # dataframe, como forma de visualizar a prevalência de cada palavra.
# todas_palavras = ' '.join([texto for texto in df.text_pt])
# 
# # Gerando a nuvem de palavras:
# nuvem_palavras = WordCloud(width = 800, height=500,
#                            max_font_size=110,
#                            collocations=False).generate(todas_palavras)
# 
# # OBS:
# # O parâmetro collocations = False, indica que eu não quero ter
# # na nuvem de palavras bigramas, isto é, par de palavras, como "um filme",
# # mas apenas uma única palavra, como "filme", "um", "bom", "ruim" e etc.
# 
# plt.figure(figsize=(10,7))
# plt.imshow(nuvem_palavras, interpolation="bilinear")
# plt.axis('off')  # Remover os números do eixo x e y
# plt.show()

"""- Criando um novo dataframe para compreender melhor a frequência das palavras."""

# Agora que, formalmente, concebe-se, em síntese, o que é um token
# e o processo de tokenização, podemos tokenizar o nosso texto, além
# do processo de outrora, que foi atrelado ao objetivo de excluir as
# stopwords, que pouco contribuem com a compreensão semântica do texto.

# Nesse sentido, vamos tokenizar a resenha e depois visualizar em um
# dataframe as palavras que são mais frequentes.

token_space = tokenize.WhitespaceTokenizer()
token_frase = token_space.tokenize(todas_palavras)
frequencia = nltk.FreqDist(token_frase)

df_frequencia = pd.DataFrame({"Palavra": list(frequencia.keys()),
                                   "Frequência": list(frequencia.values())})

df_frequencia.head(20)

# Visualizando os itens da tabela via gráfico de Pareto:

def pareto(df, coluna ,quantidade):

  plt.figure(figsize=(12,8))

  ax = sns.barplot(data=df.nlargest(columns=coluna, n = quantidade),
                   x = "Palavra", y = "Frequência", color = "gray")

  ax.set(ylabel = "Contagem")

  # Rotaciona em 90° os rótulos do eixo de x.
  plt.xticks(rotation=90)
  plt.show()

pareto(df_frequencia, "Frequência", 20)

"""Por meio desse conjunto de informações visuais tornou possível identificar a prevalência de termos que pouco dizem respeito a semântica do texto em relação a outros ? Nota-se muitos artigos, algumas preposições e etc. Além disso, é possível de perceber palavras com acentuação.

A esses termos, desconsiderando, em essência, o último, damos o nome de stopwords, os quais precisam ser excluídos do modelo, para que apenas termos que apresentam relevância semântica sejam mantidos.

Dado que não apenas os stopwords, mas outros elementos, como ancetuação, pontuação também devem ser excluídos, a primeira etapa do tratamento do texto se dará por excluir tais termos.

### Tratando o texto 📜
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Baixar as stopwords em português
# nltk.download('stopwords')
# nltk.download('punkt')
# 
# # Definir as stopwords em português
# stopwords_pt = set(stopwords.words('portuguese'))
# 
# # Função para remover stopwords, pontuações e acentuações
# def remover_stopwords_pontuacoes_acentos(texto):
#     # Tokenizar o texto
#     tokens = word_tokenize(texto.lower(), language='portuguese')
# 
#     # Remover stopwords, pontuações e acentuações
#     tokens_sem_stopwords_pontuacoes = [token for token in tokens if token not in stopwords_pt and token.isalpha()]
#     tokens_sem_acentos = [unicodedata.normalize('NFKD', token).encode('ascii', 'ignore').decode('utf-8') for token in tokens_sem_stopwords_pontuacoes]
# 
#     # Reconstruir o texto sem stopwords, pontuações e acentuações
#     texto_sem_stopwords_pontuacoes_acentos = ' '.join(tokens_sem_acentos)
# 
#     return texto_sem_stopwords_pontuacoes_acentos

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Aplicar a função ao dataframe e criar uma nova coluna com o texto processado.
# df['tratamento_1'] = df['text_pt'].apply(remover_stopwords_pontuacoes_acentos)
# 
# # Exibir as primeiras linhas do dataframe com a nova coluna:
# df.head()

"""- Verificando brevemente os textos da nova coluna:

Observe que em ambas as resenhas (que são as mesmas anteriormente mostradas) não há mais a presença de acentuação, pontuações e stopwords.
"""

df.tratamento_1[0]

df.tratamento_1[2]

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Verificando novamente o gráfico de Pareto,
# # para visualizar as palavras mais frequentes.
# 
# # Criando um conjunto que tenha todas as palavras de todas as resenhas do
# # dataframe, como forma de visualizar a prevalência de cada palavra.
# todas_palavras = ' '.join([texto for texto in df.tratamento_1])
# 
# token_space = tokenize.WhitespaceTokenizer()
# token_frase = token_space.tokenize(todas_palavras)
# frequencia = nltk.FreqDist(token_frase)
# 
# df_frequencia = pd.DataFrame({"Palavra": list(frequencia.keys()),
#                                    "Frequência": list(frequencia.values())})

pareto(df_frequencia, "Frequência", 20)

"""🗨️ Observando a imagem acima, nota-se que as palavras com acentuação foram excluídas, bem como os acentos e as stopwords, mas ainda há algo: note quais são as palavras com maior frequência - filme e filmes.

Isso ocorre, no presente notebook, por óbvio, tendo em vista que se trata de uma análise dos sentimentos de resenhas de filmes obtidas via um dataframe do kaggle.

Mas o quão útil é permitir que palavras tão semelhantes, que, em síntese, possuem essência análoga, divergindo apenas a sua quantidade, presentes no modelo ? Não seria mais eficiente, porém, conservar apenas a sua unidade básica, a sua porção radical ? Sim, e esses são os stemms.

### Stemmização 🌱

Stemmização é o nome que dei ao processo de encontrar a radical das palavras, desconsiderando o seu tamanho, ou numa linguagem gramatical, seu número. Para visualizar, basta pegarmos duas palavras que em essência se referem a um mesmo objeto, divergindo apenas em sua quantidade: filme e filmes. Note que o radical de ambas, é filme.

Mas há uma outra forma de eu entender sobre esse processo ? Sim, esse processo busca o radical das palavras, aquilo que nelas é o mais elementar e as qualificam como tais, ou seja, a sua unidade básica. O efeito disso é não apenas remover o numeral das palavras, mas também seu sufixo e/ou prefixo.

A razão de existir desse processo está em reduzir a dimensionalidade dos dados, simplificando o texto a partir do agrupamento de termos semelhantes com base em seus radicais. Desse modo, variações verbais ou de outra natureza não prejudica o modelo.

Por mais contraditório que possa parecer à primeira vista, esse processo não interefere negativamente no modelo, mas pode até melhorá-lo, de modo que o torna hábil a generalizar melhor e encontrar facilmente mais padrões no texto.

- Em síntese:

O processo de "stemmização" é cortar da palavra tudo aquilo que não é o seu radical, a sua unidade básica, de modo que não interfira negativamente no modelo, mas que, por meio do agrupamento de termos semelhantes, permite a esse a capacidade de generalização e identificação de padrões.
"""

nltk.download('rslp')
nltk.download('punkt')

stemmer = nltk.RSLPStemmer()

print("Exemplo com a palavra corredor: ", stemmer.stem("corredor"), "\n")
print("Exemplo com a palavra correr: ", stemmer.stem("correr"))

# Aplicando o stemm no dataframe:

# Inicializar o stemmer
stemmer = PorterStemmer()

# Função para aplicar stemming a uma frase
def aplicar_stemming(frase):
    nova_frase = []
    for palavra in word_tokenize(frase):
        stem = stemmer.stem(palavra)
        nova_frase.append(stem)
    return ' '.join(nova_frase)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Aplicar stemming à coluna 'tratamento_3' do dataframe
# df["tratamento_2"] = df["tratamento_1"].apply(aplicar_stemming)
# 
# # Exibir o dataframe atualizado
# df.head()

# Reformulando o dataframe, para ficar mais elegante:

df = df[["id", "text_en", "text_pt", "tratamento_1", "tratamento_2",
         "sentiment", "classificacao"]]

df.head()

"""### Dividindo a WordCloud em nuvem de sentimentos negativos 👎 e positivos 👍.

Verificando a nuvem de palavras após o tratamento do texto, verificando a forma delas, visualizando se ainda guardam a sua forma anterior ou não.
"""

def nuvem_palavras_neg(df, coluna):
    texto_negativo = df.query("sentiment == 'neg'")
    todas_palavras = ' '.join([df for df in texto_negativo[coluna]])

    nuvem_palavras = WordCloud(width= 800, height= 500,
                              max_font_size = 110,
                              collocations = False).generate(todas_palavras)
    plt.figure(figsize=(10,7))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def nuvem_palavras_pos(df, coluna):
    texto_negativo = df.query("sentiment == 'pos'")
    todas_palavras = ' '.join([df for df in texto_negativo[coluna]])

    nuvem_palavras = WordCloud(width= 800, height= 500,
                              max_font_size = 110,
                              collocations = False).generate(todas_palavras)
    plt.figure(figsize=(10,7))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# nuvem_palavras_neg(df, "tratamento_2")

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# nuvem_palavras_pos(df, "tratamento_2")

"""Verificando agora a acurácia do modelo após o tratamento dos textos."""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# print(classificar_texto(df, "tratamento_2", "classificacao"))

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# print(classificar_texto(df, "text_pt", "classificacao"))

"""Note que a partir do tratamento do texto, há um ganho de um em relação ao outro de 2.3%.

### Tratando a entrada no modelo 🤖

- Abordagem TF-IDF 🕵️

Ok, eu já realizei o tratamento do texto de variadas formas, perpassando para a sua padronização em minúscula, removendo artigos e preposições, pontuações, bem como reduzindo cada termo em sua unidade básica - ou radical. Mas há outra coisa que eu possa fazer para auxiliar o modelo no processo de classificação do sentimento prevalente no texto, com base em sua semântica ?

Sim, mas para observar isso, precisamos de um exemplo:
"""

# Definir os dados
texto = ["Assisti um filme ótimo", "Assisti a um filme ruim",
         "Assisti a um filme muito muito bom", "Assisti a um filme paia"]

# Inicializar o vetorizador
vetorizador = CountVectorizer()

# Vetorizar o texto
bag_of_words = vetorizador.fit_transform(texto)

# Criar um dataframe com as palavras como colunas
df_bw = pd.DataFrame(bag_of_words.toarray(), columns=vetorizador.get_feature_names_out())

# Exibir o dataframe
df_bw

"""🗨️ Tanto pela lista quanto pela tabela acima, verifica-se que há termos que se repetem, na forma que a repetição é percebida explicitadamente na primeira e compreendida pela quantidade de vezes em que um mesmo termo aparece em linhas diferentes, as quais representam as frases. Com isso uma pergunta pode surgir?

Termos que se repetem em mais de uma das vezes..., enquanto outros, que podem trazer até mais relevância semântica, como os "ótimos", "bons", "ruins", "péssimos" e etc, aparecem pouco... Isso pode interfirir negativamente no modelo?

Quero dizer, dado que um termo aparece mais, esse pode ter mais impacto na classificação do que outros que aparecem menos ? E se sim, porém além: e se esses que aparecem menos podem prover maior caráter semântico ao modelo ? O que fazer ?

Com base nessa problemática que se utiliza a abordagem do **TF-IDF**, basicamente ela atribui um valor inversamente proporcional à quantidade de termos que aparecem num conjunto de dados, ou dataset. Nesse sentido, se um termo aparece muitas vezes, esse possuirá um peso menor, de modo que um outro, que se apresenta numa menor quantidade terá um peso maior.

Assim, relacionando com o tema desse notebook, a palavra "film", radical de "filme" ou "filmes", terá um peso menor, quando comparada às palavras "bom", "ótimo", "ruim", "péssimo" e etc, que aparecem menos.

- Exempleficando a abordagem 💡
"""

frases = ["Assisti um filme ótimo", "Assisti um filme péssimo"]

tfidf = TfidfVectorizer(lowercase=False, max_features=50)

caracteristicas = tfidf.fit_transform(frases)

pd.DataFrame(
    caracteristicas.todense(),
    columns=tfidf.get_feature_names_out()
)

"""Por meio da tabela a seguir consegue observar como se dá o processo de atribuição dos pesos? Note que justamente nas palavras que aparecem uma única vez são aquelas que possuem pesos maiores, de modo que ocorre o oposto naquelas que apresentam uma aparição dupla.

- Verificando a acurácia:

Agora que já entendemos como funciona essa abordagem, segmentaremos as resenhas, compreendendo a resenha em pt-br original e aquela que, a partir dessa, criamos após os processos de tratamento, com o objetivo de verificar a acurácia, compará-la.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # TF-IDF para a coluna não tratada:
# 
# tfidf_bruto = tfidf.fit_transform(df["text_pt"])
# 
# train, test, X_train, y_test = train_test_split(tfidf_bruto,
#                                                 df.classificacao,
#                                                 random_state = 22)
# 
# # Modelo de regressão logística para prever um texto de teste
# # a que rótulo ele pertence: positivo ou negativo.
# 
# regressao_logistica = LogisticRegression()
# regressao_logistica.fit(train, X_train)
# 
# acuracia_tfidf_bruto = regressao_logistica.score(test, y_test)
# 
# # -------------------------------------------------------------------------------- #
# 
# # TF-IDF para a coluna tratada e stemmizada:
# 
# tfidf_tratados = tfidf.fit_transform(df["tratamento_2"])
# 
# train, test, X_train, y_test = train_test_split(tfidf_tratados,
#                                                 df.classificacao,
#                                                 random_state = 22)
# 
# regressao_logistica.fit(train, X_train)
# acuracia_tfidf_tratados = regressao_logistica.score(test, y_test)
# 
# 
# print(f"A acurácia da coluna sem tratamento, utilizando o TF-IDF é de {round(acuracia_tfidf_bruto ,3)*100} %")
# print("")
# print(f"A acurácia da coluna com tratamento e stemmizada, utilizando o TF-IDF é de {round(acuracia_tfidf_tratados ,3)*100} %")
# print("")

"""Observando as novas acurácias com base na nova abordagem utilizada, nota-se que o modelo apresentou um ganho de 0.2 %. Ou seja, apresenta um ganho, porém ainda não tão significativo.

### N-Gramns: 📚

Para passar um texto em um modelo, precisei vetorizá-lo, além de tokenizá-lo por meio das "n" etapas de tratamentos necessárias, visando a sua consistência e capacidade de generalização e identificação de padrões, certo? Porém, veja, utilizar a vetorização normal, criando a bag_of_words, composta de palavra por palavra, não pode ser necessariamente o mais eficiente.

Por isso surge a abordagem dos n-gramns, recurso que permite representar sequências de palavras em um texto de uma forma estruturada e contextualizada. Em termos simples, um N-grama é uma sequência contínua de N itens consecutivos de uma amostra de texto. Esses itens podem ser caracteres, palavras, ou até mesmo símbolos, dependendo do contexto em que estão sendo utilizados.

Por exemplo, considere a frase: "Eu gosto de sorvete de chocolate". Se decidirmos dividir essa frase em bi-gramas (2-grams), obteremos:

- "Eu gosto"
- "gosto de"
- "de sorvete"
- "sorvete de"
- "de chocolate"

💬 Agora, se optarmos por dividir a mesma frase em tri-gramas (3-grams), obteremos:

- "Eu gosto de"
- "gosto de sorvete"
- "de sorvete de"
- "sorvete de chocolate"

🔍 Os N-grams são úteis porque capturam a estrutura e o contexto do texto de uma forma mais detalhada do que palavras individuais. Ao analisar os N-grams em um texto, podemos entender melhor como as palavras estão relacionadas umas com as outras e como elas contribuem para o significado global da frase ou do documento.

- Verificando os N-gramns em código:
"""

from nltk import ngrams

frase = "Assisti um ótimo filme."
frase_separada = token_space.tokenize(frase)

print("Como ficava a frase sem utilizar o ngrams: \n", frase_separada)
print("")

pares = ngrams(frase_separada, 2)
print("A frase em pares: \n", list(pares))

print("")

trio = ngrams(frase_separada, 3)
print("A frase em trio: \n", list(trio))

"""💬 Conseguiu observar a diferença ? Observou como o ngrams garante uma sequência por meio do agrupamento que forma, promovendo uma sequência, como espécime de memória, a qual pode contribuir com a análise semântica do texto, diferente do primeiro processo em que não há a utilização do ngrams?

Nesse sentido, além dos processos de tratamento do texto, perpassando pela remoção da pontuação, dos stopwords, da stemmização e do TF-IDF, recomenda-se para a análise semântica do modelo de PLN, que os textos estejam segundo os N-gramns, que garantem uma sequência lógica das frases, contribuindo com a análise da semântica to texto.

- Utilizando os N-gramns, ao modelo e verificar se há ou não ganho em sua acurácia:
"""

from tqdm import tqdm_notebook

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Inicialize o TfidfVectorizer
# tfidf = TfidfVectorizer(ngram_range=(1, 2))
# 
# # Ajuste o TfidfVectorizer e obtenha a representação TF-IDF dos dados
# vetor_tfidf = tfidf.fit_transform(df["tratamento_2"])
# 
# # Crie uma barra de progresso para monitorar o progresso
# progresso = tqdm_notebook(total=vetor_tfidf.shape[0], desc="Criando vetor TF-IDF")
# 
# # Segmentação:
# treino, teste, classe_treino, classe_teste = train_test_split(vetor_tfidf,
#                                                               df["classificacao"],
#                                                               random_state=22)
# 
# # Modelo:
# regressao_logistica = LogisticRegression()
# regressao_logistica.fit(treino, classe_treino)
# 
# # Atualize a barra de progresso
# progresso.update(vetor_tfidf.shape[0])
# progresso.close()
# 
# # Calcule a acurácia do modelo
# acuracia_tfidf_ngrams = regressao_logistica.score(teste, classe_teste)
# 
# # Exiba a acurácia
# print(f"A acurácia do modelo, com a utilização dos n-gramns foi de {round(acuracia_tfidf_ngrams, 3)*100} %")
# print("")

"""Note como a utilização dos N-gramns foi eficiente ao modelo. Antes ele possuia uma acurácia de 69.5%, agora ele possui uma acurácia de 89.2%, representando um salto de pouco mais que 20% de um em relação ao outro.

### Vericando quais são as variáveis explicativas que contribuem com a resposta do modelo: 🔍

Algo que o modelo de regressão logística permite realizar é a verificação do quanto certas variáveis contribuem ou não a resposta do modelo. Nesse sentido, no presente contexto, podemos analisar quais são as variáveis que impactam tanto numa classificação de sentimento tida como positiva quanto de negativa, vejamos:

- Sentimento : "pos"
"""

pesos = pd.DataFrame(
    regressao_logistica.coef_[0].T,
    index = tfidf.get_feature_names_out()
)
pesos.nlargest(10, 0)

"""- Sentimento: "neg"
"""

pesos.nsmallest(10, 0)


# Sistema Inteligente para Passaporte brasileiro

Este projeto implementa um sistema inteligente capaz de carregar imagens faciais, extrair suas features (vetores de características) e posteriormente utilizá-las para treinar um modelo de aprendizado de máquina.

---

## 1. Pré-requisitos

Antes de iniciar, verifique se você possui:

* Python instalado (versão 3.8 ou superior recomendada)
* Pip atualizado
* Ambiente virtual configurado (opcional mas muito recomendado)

---

## 2. Instalação das Dependências

Todas as dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalá-las, coloque o comando:

```bash
pip install -r requirements.txt
```

Isso ira instalar todas as bibliotecas necessárias para o funcionamento do sistema.

---

## 3. Download do Banco de Dados de Faces

O sistema foi projetado para funcionar com o conjunto de imagens de faces do banco de dados FEI.

Faça o download pelo link:

[https://fei.edu.br/~cet/facedatabase.html](https://fei.edu.br/~cet/facedatabase.html)

---

## 4. Organização das Imagens

Após baixar e extrair o dataset, mova as imagens para a pasta do geradorBR, ele irá utilizar as imagens para gerar passaportes brasileiros

A estrutura recomendada é:

```
/GerarBR
    /banco_fotos
        imagem.jpg
```
---

## 5. Extração de Features

Com as imagens organizadas, o sistema poderá carregar cada uma delas e gerar suas features. Esse processo normalmente inclui:

1. Leitura da imagem
2. Pré-processamento
3. Passagem por um extrator
4. Geração de vetores de características

Essas features serão utilizadas na etapa de treinamento do modelo.

---

## 6. Treinamento do Modelo

Após gerar todas as features:

1. O sistema irá agrupá-las e preparar os dados
2. Será executado o processo de treinamento
3. O modelo poderá ser salvo para uso posterior

---

## 7. Execução do Sistema

Cada módulo do projeto pode ter scripts específicos, mas a execução geral segue os passos:

1. Instalar dependências
2. Organizar imagens
3. Executar o extrator de features
4. Iniciar o treinamento


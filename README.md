# 🔄 ETL de VLANs - Tratamento e Integração com NetBox

Este projeto consiste em um pipeline ETL desenvolvido em **Python** para tratar e estruturar dados brutos de VLANs extraídos de um arquivo `.txt`, com o objetivo de gerar um `.csv` compatível com os requisitos de importação do **NetBox**. 

Além disso, os dados tratados são armazenados localmente em um banco de dados **PostgreSQL**, permitindo sua reutilização em diferentes contextos futuros, como integrações com aplicações nativas ou sistemas de gerenciamento.

## 🧩 Tecnologias Utilizadas

- Python 3.x
- `re` (expressões regulares para limpeza dos dados)
- `psycopg2` (integração com PostgreSQL)
- PostgreSQL local
- CSV para importação no NetBox

## ⚙️ Funcionalidades

- Leitura de dados brutos de VLANs em arquivo `.txt`
- Limpeza e estruturação dos dados com `regex`
- Armazenamento dos dados tratados em banco PostgreSQL
- Exportação dos dados limpos para arquivo `.csv` compatível com NetBox
- Flexibilidade para futuras integrações com outros sistemas ou aplicações

## 🧠 Motivação

Este projeto faz parte do meu **portfólio como futuro Engenheiro de Dados** e foi desenvolvido com foco na **resolução de um problema real de negócio**, priorizando boas práticas de engenharia e clareza nos processos, ao invés de dependência de ferramentas específicas.

O pipeline resolve um desafio comum em ambientes de infraestrutura de rede: transformar dados não estruturados em informações organizadas, válidas e utilizáveis em sistemas como o NetBox.

## 📁 Estrutura do Projeto

etl_vlans/
├── data/
│ └── vlans.txt # Arquivo original com dados brutos
├── output/
│ └── vlans_formatadas.csv # Arquivo CSV pronto para o NetBox
├── etl_pipeline.py # Script principal do ETL
├── requirements.txt # Dependências do projeto
└── README.md

## 🖼️ Exemplo do Pipeline em Execução

![Pipeline ETL - Exemplo](images/pipeline.jpeg)

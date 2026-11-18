# ONG Água Azul — Sistema de Gestão de Doações (MVP)

Aplicação web responsiva desenvolvida como Projeto de Software (Experiência Prática) para apoiar a gestão de campanhas, famílias atendidas e doações da **ONG Água Azul** (Guarulhos - SP).

## Problema e Objetivo
Substituir controles dispersos em anotações e planilhas por um sistema centralizado, simples e acessível pelo celular, reduzindo retrabalho e garantindo rastreabilidade sobre as entregas realizadas às famílias.

## Tecnologias Utilizadas
- **Linguagem:** Python 3.12
- **Framework Web e ORM:** Django
- **Interface Responsiva:** HTML5, CSS3 e Bootstrap 5
- **Banco de Dados:** SQLite (embarcado)

## Funcionalidades Principais (MVP)
- **RF01:** Autenticação obrigatória para equipe autorizada.
- **RF02:** Cadastro único de famílias atendidas.
- **RF03:** Cadastro e encerramento de campanhas de doação.
- **RF04:** Registro de doações vinculadas a famílias e campanhas ativas.
- **RF05:** Consulta do histórico e resumo de entregas por campanha.

## Como executar localmente
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

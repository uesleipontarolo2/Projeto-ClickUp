
# Extração de dados do ClickUp

Extração de dados do ClickUp utilizando Python

## Objetivo do Projeto

O objetivo deste projeto é solucionar um gap identificado em meu departamento por meio do uso de dados extraídos do ClickUp. O foco é melhorar a eficiência no gerenciamento de tarefas, proporcionando uma melhor organização, acompanhamento e visualização das atividades.

Para saber mais sobre o ClickUp, visite o [site oficial do ClickUp](https://clickup.com).



## Funcionalidades

- Dados das tarefas
- Nome das tags
- Nome dos membros
- Dados dos tempo gasto por tarefa e tempo por membros



## API do ClickUp

#### Endpoints
Tasks
```http
  GET /list/{list_id}/task
```
Members
```http
  GET /task/{task_id}/member
```
Times Entries
```http
  GET /team/{team_Id}/time_entries
```
Tags
```http
  GET /space/{space_id}/tag
```


| Parâmetros   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `Authorization` | `string` | **Obrigatório**. Chave de autorização |
| `list_id` | `string` | Lista de projetos |
| `team_id` | `string` | ID do time |
| `space_id ` | `string` | ID do Espaço de trabalho |
| `assignee ` | `string` | Membros atribuidos |
| `include_task_tags ` | `string` | Incluir tags |


## Referência

 - [Documentação da API do ClickUp]https://clickup.com/api/)
## Como obter o projeto

Para obter uma cópia deste projeto, siga as etapas abaixo:

1. Abra o terminal ou prompt de comando no seu ambiente.
2. Navegue até o diretório onde deseja clonar o projeto.
3. Execute o seguinte comando para clonar o repositório:

```shell
git clone https://github.com/uesleipontarolo2/Projeto-ClickUp.git
```

Antes de executar o projeto, certifique-se de ter as seguintes bibliotecas instaladas:

- requests
- pandas
- datetime
- psycopg2

Você pode instalá-las executando o seguinte comando no seu ambiente Python:

```shell
pip install requests pandas psycopg2
pip install requests pandas
```
## 🚀 Sobre mim
Analista de Marketing e Gestor de Tráfego. Atualmente, sou acadêmico do curso de Engenharia Elétrica na UNIC e do curso de Ciência de Dados na UNOPAR. Desde a adolescência, tenho sido entusiasta de tecnologia, inovações e matemática, buscando constantemente aplicar esses conhecimentos no crescimento e desenvolvimento de empresas.


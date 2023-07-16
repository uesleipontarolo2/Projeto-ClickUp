# imports
import requests
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import extras

# conectar com o banco de dados
conn = psycopg2.connect(
    database='#',
    host='localhost',
    user='#',
    password='#',
    port='5432'
)

print(conn.info)
cursor = conn.cursor()


# Query padrões
list_id = "#"  # lista projetos
team_id = '#'  # id da equipe
space_id = '#'  # id do espaço
headers = {"Authorization": "#"}

# Coletar as tarefas
url_task = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

query_task = {
    "subtask": "true",
    "include_closed": "true"
}

response_task = requests.get(url_task, headers=headers, params=query_task)
data_task = response_task.json()

# Coletar dados das tarefas
tasks_data = []
for task in data_task['tasks']:
    task_id = task['id']
    task_name = task['name']
    date_created = datetime.fromtimestamp(int(task['date_created']) / 1000)
    date_updated = datetime.fromtimestamp(int(task['date_updated']) / 1000)
    url = task['url']
    status_name = task['status']['status']

    if task['date_closed'] is not None:
        date_closed = datetime.fromtimestamp(int(task['date_closed']) / 1000)
    else:
        date_closed = task['date_closed']

    if task['due_date'] is not None:
        due_date = datetime.fromtimestamp(int(task['due_date']) / 1000)
    else:
        due_date = task['due_date']

    assignee_ids = []
    for assignee in task['assignees']:
        assignee_id = assignee['id']
        assignee_ids.append(assignee_id)
    assignee_ids = list(map(int, assignee_ids))

    tags_task = []
    for tag in task['tags']:
        tags_name = tag['name']
        tags_task.append(tags_name)

    tasks_data.append({
        'task_id': task_id,
        'task_name': task_name,
        'date_created': date_created,
        'date_updated': date_updated,
        'due_date': due_date,
        'url': url,
        'status_name': status_name,
        'date_closed': date_closed,
        'assignee_ids': assignee_ids,
        'tags_task': tags_task
    })

task_tags_relantionship = []
for task_tag in tasks_data:
    task_id = task_tag['task_id']
    task_tags = task_tag['tags_task']

    for tag in task_tags:
        task_tags_relantionship.append({'task_id': task_id, 'tag_name': tag})

for task_id in task_tags_relantionship:
    task_id = task_id['task_id']
    
    cursor.execute("SELECT task_id FROM task_tags_relantionship WHERE task_id = %s", (task_id,))
    existing_taskid = cursor.fetchone()

    if existing_taskid:
        cursor.execute('DELETE FROM task_tags_relantionship WHERE task_id = %s', (task_id,))

for task_tag in task_tags_relantionship:
    task_id = task_tag['task_id']
    tag_name = task_tag['tag_name']

    cursor.execute(
        'INSERT INTO task_tags_relantionship (task_id, tag_name) VALUES (%s, %s)', (task_id, tag_name))


task_merbers_relantionship = []
for member_task in tasks_data:
    task_id = member_task['task_id']
    assignee_ids = member_task['assignee_ids']

    for assignee_id in assignee_ids:
        task_merbers_relantionship.append(
            {'task_id': task_id, 'member_id': assignee_id})

for task_id in task_merbers_relantionship:
    task_id = task_id['task_id']
    
    cursor.execute("SELECT task_id FROM task_merbers_relantionship WHERE task_id = %s", (task_id,))
    existing_taskid = cursor.fetchone()

    if existing_taskid:
        cursor.execute('DELETE FROM task_merbers_relantionship WHERE task_id = %s', (task_id,))

for task_members in task_merbers_relantionship:
    task_id = task_members['task_id']
    member_id = task_members['member_id']

    cursor.execute(
        'INSERT INTO task_merbers_relantionship (task_id, member_id) VALUES (%s, %s)', (task_id, member_id))


# Enviando para o banco de dados as task
for task in tasks_data:
    task_id = task['task_id']
    task_name = task['task_name']
    date_created = task['date_created']
    date_updated = task['date_updated']
    due_date = task['due_date']
    url = task['url']
    status_name = task['status_name']
    date_closed = task['date_closed']
    assignee_ids = task['assignee_ids']
    tags_task = task['tags_task']

    # Verificar se ja tem task
    cursor.execute("SELECT task_id FROM task WHERE task_id = %s", (task_id,))
    existing_task = cursor.fetchone()

    # Caso ja exista uma task
    if existing_task:
        cursor.execute("UPDATE task SET task_name = %s, date_created = %s, date_updated = %s, due_date = %s, url = %s, "
                       "status_name = %s, date_closed = %s, assignee_ids = %s, tags_task = %s WHERE task_id = %s",
                       (task_name, date_created, date_updated, due_date, url, status_name, date_closed, assignee_ids,
                        tags_task, task_id))
    else:
        cursor.execute("INSERT INTO task (task_id, task_name, date_created, date_updated, due_date, url, status_name, "
                       "date_closed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (task_id, task_name, date_created, date_updated, due_date, url, status_name, date_closed))


# retorno dos membros
url_members = "https://api.clickup.com/api/v2/list/" + list_id + "/member"
response_members = requests.get(url_members, headers=headers)
data_members = response_members.json()

# Coletar dados dos membros
member_data = []
for member in data_members['members']:
    member_id = member['id']
    member_name = member['username']

    member_data.append({
        'member_id': member_id,
        'member_name': member_name
    })

for members in member_data:
    member_id = members['member_id']
    member_name = members['member_name']
    # Verificar ID
    cursor.execute(
        'SELECT member_id FROM members WHERE member_id = %s', (member_id,))
    existing_member = cursor.fetchone()

    if existing_member:
        cursor.execute(
            'UPDATE members SET member_name = %s WHERE member_id = %s', (member_name, member_id))
    else:
        cursor.execute(
            "INSERT INTO members (member_id, member_name) VALUES (%s, %s)", (member_id, member_name))


# coletar tempo rastreado
data_hour = []
for membro in member_data:
    member_id = membro['member_id']
    url = "https://api.clickup.com/api/v2/team/" + team_id + "/time_entries?"

    query_hour = {
        "assignee": str(member_id),
        "include_task_tags": "true",
    }

    response = requests.get(url, headers=headers, params=query_hour)

    data_hour.append(response.json())


# Dados do tempo rastreado
time_hour = []
for item in data_hour:
    for data in item['data']:
        time_id_hour = data['id']
        task_id_hour = data['task']['id']
        user_id_hour = data['user']['id']
        task_tags_hour = [tag['name'] for tag in data['task_tags']]
        start_hour = datetime.fromtimestamp(int(data['start']) / 1000)
        end_hour = datetime.fromtimestamp(int(data['end']) / 1000)
        duration_hour = round(timedelta(milliseconds=int(
            data['duration'])).total_seconds() / 60, 2)

        time_hour.append({
            'time_id': time_id_hour,
            'task_id': task_id_hour,
            'user_id': user_id_hour,
            'task_tags': task_tags_hour,
            'start': start_hour,
            'end': end_hour,
            'duration': duration_hour
        })

for hour in time_hour:
    time_id = int(hour['time_id'])
    task_id = hour['task_id']
    user_id = hour['user_id']
    task_tags = hour['task_tags']
    start = hour['start']
    end = hour['end']
    duration = hour['duration']

    # Verificar ID
    cursor.execute('SELECT time_id FROM hours WHERE time_id = %s', (time_id,))
    existing_hours = cursor.fetchone()

    if existing_hours:
        cursor.execute(
            'UPDATE hours SET task_id = %s, user_id = %s, start_date = %s, end_date = %s, duration = %s WHERE time_id = %s',
            (task_id, user_id, start, end, duration, time_id))
    else:
        cursor.execute('INSERT INTO hours (time_id, task_id, user_id, start_date, end_date, duration) VALUES (%s, %s, %s, %s, %s, %s)',
                       (time_id, task_id, user_id, start, end, duration))


#relacionamento entre time e tags

hour_tags_relationship = []
for hour_tag in time_hour:
    time_id = hour_tag['time_id']
    time_tags = hour_tag['task_tags']

    for tag in time_tags:
        hour_tags_relationship.append({'time_id': time_id, 'tag_name': tag})

# Faz a limpa na tabela caso já exista uma tarefa com o mesmo id
for hour_tag in hour_tags_relationship:
    time_id = hour_tag['time_id']

    cursor.execute('SELECT time_id FROM hour_tags_relationship WHERE time_id = %s', (time_id,))
    existing_timeid = cursor.fetchone()

    if existing_timeid:
        cursor.execute('DELETE FROM hour_tags_relationship WHERE time_id = %s', (time_id,))

# Adiciona as horas por tags
for hour_tag in hour_tags_relationship:
    time_id = hour_tag['time_id']
    tag_name = hour_tag['tag_name']

    cursor.execute('INSERT INTO hour_tags_relationship (time_id, tag_name) VALUES (%s, %s)', (time_id, tag_name))


# coletar tags
url_tags = "https://api.clickup.com/api/v2/space/" + space_id + "/tag"
headers_tags = {
    "Content-Type": "application/json",
    "Authorization": "#"
}

response_tags = requests.get(url_tags, headers=headers_tags)
data_tags = response_tags.json()

tags_data = []
for tag in data_tags['tags']:
    tag_name = tag['name']
    tags_data.append({
        'tag_name': tag_name
    })

for tag in tags_data:
    tags_name = tag['tag_name']

    cursor.execute('INSERT INTO tags (tag_name) VALUES (%s)', (tags_name,))

conn.commit()

#df = pd.DataFrame(time_hour)

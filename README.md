# 💬 FORUM WEB

## Forum web com ligação ao banco de dados

### Linguagens e banco de dados
- python
  - fastAPI
  - Jinja2
  - msq.connector
    
- html
- css
- Mysql

### 📂 Estrutura

- static
   - assets
        - logo_forum.png
    - css
        - style.css
    - js
        - script.js
           
- templates
    - editar_post.html
    - editar.html
    - excluir.html
    - index.html
    - post.html
    - view.html
      
- venv
- app.py
- dao.py
- model.py   
## 📄 Código

### 📌 app.py

#### 🔹 Imports

```python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model import add_post, consulta_post, editar_post, excluir_post, consulta_post_por_id
```

Responsável por importar as bibliotecas necessárias para o funcionamento da aplicação, incluindo:

- **FastAPI**: framework principal da aplicação
- Manipulação de formulários (`Form`, `Request`)
- Tipos de resposta (`HTMLResponse`, `RedirectResponse`)
- Arquivos estáticos (CSS, imagens, etc.)
- Templates HTML com Jinja2
- Funções do `model.py`, responsáveis pela comunicação com o banco de dados

---

#### 🔹 Configuração da aplicação

```python
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
```

Nesta parte:

- A aplicação FastAPI é inicializada
- A pasta `static` é configurada para servir arquivos estáticos
- A pasta `templates` é definida para renderização das páginas HTML

---

#### 🔹 Rotas da aplicação (API)

```python
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts}
    )
```

Rota principal da aplicação:
- Busca todos os posts no banco de dados
- Renderiza a página inicial (`index.html`) com os dados

---

```python
@app.get("/postar", response_class=HTMLResponse)
async def pagina_postar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={}
    )
```

Exibe a página com o formulário para criação de novos posts.

---

```python
@app.get("/view", response_class=HTMLResponse)
async def pagina_view(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="view.html",
        context={"posts": posts}
    )
```

Exibe todos os posts cadastrados.

---

```python
@app.post("/add")
async def add(request: Request):
    form = await request.form()
    titulo = form.get("titulo")
    informacoes = form.get("informacoes")
    add_post(titulo, informacoes)
    return RedirectResponse(url="/view", status_code=303)
```

Recebe os dados do formulário e adiciona um novo post ao banco de dados.  
Após isso, redireciona para a página de visualização.

---

```python
@app.get("/editar", response_class=HTMLResponse)
async def pagina_editar_lista(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="editar.html",
        context={"posts": posts}
    )
```

Exibe a lista de posts disponíveis para edição.

---

```python
@app.get("/editar/{id}", response_class=HTMLResponse)
async def pagina_editar_post(request: Request, id: int):
    post = consulta_post_por_id(id)
    return templates.TemplateResponse(
        request=request,
        name="editar_post.html",
        context={"post": post}
    )
```

Carrega os dados de um post específico para edição.

---

```python
@app.post("/editar/{id}")
async def editar(id: int, titulo: str = Form(...), informacoes: str = Form(...)):
    editar_post(id, titulo, informacoes)
    return RedirectResponse(url="/view", status_code=303)
```

Atualiza os dados do post no banco de dados e redireciona para a página de visualização.

---

```python
@app.get("/excluir", response_class=HTMLResponse)
async def pagina_excluir(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="excluir.html",
        context={"posts": posts}
    )
```

Exibe a lista de posts disponíveis para exclusão.

---

```python
@app.post("/excluir/{id}")
async def excluir(id: int):
    excluir_post(id)
    return RedirectResponse(url="/excluir", status_code=303)
```

Remove um post do banco de dados e atualiza a lista exibida.

---

### dao.py
```python
import mysql.connector

def connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='forum'
    )
```

Responsável por estabelecer a conexão com o banco de dados **MySQL**.

#### 🔹 Parâmetros da conexão:

- **host**: endereço do servidor do banco (geralmente `localhost` em ambiente local)
- **user**: usuário do banco de dados
- **password**: senha do banco (vazia neste caso)
- **database**: nome do banco utilizado (`forum`)

---

#### ⚠️ Importante

Para que o projeto funcione corretamente, é necessário:

1. Ter o **MySQL** instalado e em execução
2. Criar o banco de dados com o nome:

```sql
CREATE DATABASE forum;
```

3. Criar a tabela utilizada pelos posts (exemplo básico):

```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    informacoes TEXT
);
```

---

### model.py
```python
from dao import connection
```

Importa a função responsável por criar a conexão com o banco de dados.

---

#### 🔹 Buscar todos os posts

```python
def consulta_post():
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT * FROM post
        '''
    )
    dados = cursor.fetchall()

    conn.close()
    return dados
```

- Realiza uma consulta para retornar todos os posts do banco
- Utiliza `dictionary=True` para retornar os dados em formato de dicionário

---

#### 🔹 Adicionar um novo post

```python
def add_post(titulo, informacoes):
    conn = connection()
    cursor = conn.cursor()

    query = '''
            INSERT INTO post (titulo, informacoes) VALUES 
            (%s, %s)
            '''
    cursor.execute(query, (titulo, informacoes))
    conn.commit()
    conn.close()
```

- Insere um novo registro na tabela `post`
- Utiliza parâmetros (`%s`) para evitar SQL Injection
- `commit()` garante que a alteração seja salva no banco

---

#### 🔹 Editar um post

```python
def editar_post(id, titulo, informacoes):
    conn = connection()
    cursor = conn.cursor()

    query = '''
            UPDATE post SET titulo = %s, informacoes = %s WHERE id = %s
            '''
    cursor.execute(query, (titulo, informacoes, id))
    conn.commit()
    conn.close()
```

- Atualiza os dados de um post existente com base no `id`

---

#### 🔹 Excluir um post

```python
def excluir_post(id):
    conn = connection()
    cursor = conn.cursor()

    query = '''DELETE FROM post WHERE id = %s'''
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
```

- Remove um post do banco de dados a partir do `id`

---

#### 🔹 Buscar post por ID

```python
def consulta_post_por_id(id):
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''SELECT * FROM post WHERE id = %s''', (id,))
    dado = cursor.fetchone()

    conn.close()
    return dado
```

- Retorna apenas um post específico com base no `id`
- Utiliza `fetchone()` para obter um único resultado

---
## 🎨 Frontend (Templates HTML + Jinja2)

O projeto utiliza **templates HTML com Jinja2**, integrados ao FastAPI, para renderizar páginas dinâmicas no navegador.

Os arquivos estão organizados na pasta:

```
templates/
```

E os arquivos estáticos (CSS, imagens) em:

```
static/
```

---

### 🔹 Estrutura base dos templates

Todos os HTMLs seguem uma estrutura semelhante:

- Importação de CSS via `/static`
- Header com navegação entre as rotas
- Conteúdo dinâmico dentro da tag `<main>`

Exemplo:

```html
<link rel="stylesheet" href="/static/css/style.css">
<img src="/static/assets/logo_forum.png">
```

Esses caminhos funcionam por conta da configuração feita no FastAPI:

```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

---

### 🔹 Integração com Jinja2

O Jinja2 permite inserir dados dinâmicos diretamente no HTML.

Exemplo do `editar.html`:

```html
{% for post in posts %}
    <div class="post-editar">
        <h3>{{ post.titulo }}</h3>
        <a href="/editar/{{ post.id }}">Editar</a>
    </div>
{% endfor %}
```

#### O que está acontecendo:

- `{% for post in posts %}` → percorre a lista de posts enviada pela API
- `{{ post.titulo }}` → exibe o título do post
- `{{ post.id }}` → usado para criar rotas dinâmicas

👉 Esses dados vêm do backend:

```python
return templates.TemplateResponse(
    request=request,
    name="editar.html",
    context={"posts": posts}
)
```

---

### 🔹 Formulários e envio de dados

Exemplo do `post.html`:

```html
<form action="/add" method="post">
    <input type="text" name="titulo">
    <input type="text" name="informacoes">
    <button type="submit">Adicionar</button>
</form>
```

#### Funcionamento:

- O formulário envia os dados para a rota `/add`
- O método `POST` é utilizado para envio de dados
- Os nomes (`name="titulo"`, `name="informacoes"`) são usados no backend para capturar os valores

No FastAPI:

```python
form = await request.form()
titulo = form.get("titulo")
informacoes = form.get("informacoes")
```

---

### 🔹 Navegação entre páginas

Os templates utilizam links diretos para as rotas da aplicação:

```html
<nav>
    <a href="/">Home</a>
    <a href="/view">Visualizar Posts</a>
    <a href="/postar">Criar Posts</a>
    <a href="/editar">Editar Posts</a>
    <a href="/excluir">Excluir Posts</a>
</nav>
```

Cada link corresponde a uma rota definida no `app.py`.

---

### 🔹 Separação de responsabilidades

- **HTML (templates)** → responsável pela interface
- **FastAPI (app.py)** → controla as rotas e envia os dados
- **Jinja2** → faz a ligação entre backend e frontend

---
# 💬 Forum Web

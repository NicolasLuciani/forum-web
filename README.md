# FORUM WEB

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

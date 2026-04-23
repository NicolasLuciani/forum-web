from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

context = {}

app.mount("/static", StaticFiles(directory="static"), name="static")

posts = [
    {
        "id": 1,
        "titulo": "Meu primeiro post",
        "resumo": "Resumo...",
        "conteudo": "Conteúdo completo...",
        "autor": "Carlos"
    }
]

@app.get("/")
async def home(request: Request, response_class=HTMLResponse):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "posts": posts
        }
)

@app.get("/create")
def create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html"
    )

@app.post("/add")
async def adicionar(request: Request):
    form = await request.form()

    new_post = {
        "id": len(posts) + 1,
        "titulo": form.get("titulo"),
        "resumo": form.get("resumo"),
        "conteudo": form.get("conteudo"),
        "autor": form.get("autor")
    }

    posts.append(new_post)

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{id}")
def deletar(id: int):
    global posts

    posts_filtrados = []

    for post in posts:
        if post["id"] != id:
            posts_filtrados.append(post)

    posts = posts_filtrados

    return RedirectResponse("/", status_code=303)


@app.get("/edit/{id}")
async def edit_page(request: Request, id: int):
    post_para_editar = next((post for post in posts if post["id"] == id), None)
    
    return templates.TemplateResponse(
        request=request, 
        name="edit.html", 
        context={"post": post_para_editar}
    )


@app.post("/update/{id}")
async def atualizar(request: Request, id: int):
    form = await request.form()
    
    for post in posts:
        if post["id"] == id:
            post["titulo"] = form.get("titulo")
            post["resumo"] = form.get("resumo")
            post["conteudo"] = form.get("conteudo")
            post["autor"] = form.get("autor")
            break
            
    return RedirectResponse(url="/", status_code=303)



bd = """
CREATE DATABASE forum_web;

USE forum_web;

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    resumo VARCHAR(255),
    conteudo TEXT,
    autor VARCHAR(100)
);

INSERT INTO posts (titulo, resumo, conteudo, autor) 
VALUES (
    ('Meu Primeiro Post'), 
    'Um resumo básico sobre o fórum', 
    'Este é o conteúdo completo que ficará guardado no banco de dados.', 
    'Carlos Silva'
);
"""
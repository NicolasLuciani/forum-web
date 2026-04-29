from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model import add_post, consulta_post, editar_post, excluir_post, consulta_post_por_id

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts}
    )

@app.get("/postar", response_class=HTMLResponse)
async def pagina_postar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={}
    )

@app.get("/view", response_class=HTMLResponse)
async def pagina_view(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="view.html",
        context={"posts": posts}
    )

@app.post("/add")
async def add(request: Request):
    form = await request.form()
    titulo = form.get("titulo")
    informacoes = form.get("informacoes")
    add_post(titulo, informacoes)
    return RedirectResponse(url="/view", status_code=303)

@app.get("/editar", response_class=HTMLResponse)
async def pagina_editar_lista(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="editar.html",
        context={"posts": posts}
    )

@app.get("/editar/{id}", response_class=HTMLResponse)
async def pagina_editar_post(request: Request, id: int):
    post = consulta_post_por_id(id)
    return templates.TemplateResponse(
        request=request,
        name="editar_post.html",
        context={"post": post}
    )

@app.post("/editar/{id}")
async def editar(id: int, titulo: str = Form(...), informacoes: str = Form(...)):
    editar_post(id, titulo, informacoes)
    return RedirectResponse(url="/view", status_code=303)


@app.get("/excluir", response_class=HTMLResponse)
async def pagina_excluir(request: Request):
    posts = consulta_post()
    return templates.TemplateResponse(
        request=request,
        name="excluir.html",
        context={"posts": posts}
    )

@app.post("/excluir/{id}")
async def excluir(id: int):
    excluir_post(id)
    return RedirectResponse(url="/excluir", status_code=303)
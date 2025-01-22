from langchain_core.runnables.graph import MermaidDrawMethod
from graph_compilation import app


graph_image = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
with open("graph_image.png", "wb") as f:
    f.write(graph_image)

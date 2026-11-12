# Wave Tec Manager

Sistema de gestão de assistência técnica, cadastro de clientes, equipamentos e ordens de serviço desenvolvido para a **Wave Tec**.

## Tecnologias e Arquitetura
* **Linguagem:** Python 3
* **Framework Web:** Django 5.2 (Arquitetura MVT)
* **Front-end:** HTML5, CSS3 (Bootstrap) e JavaScript (máscaras dinâmicas universais no `base.html`)
* **Geração de Documentos:** ReportLab (PDFs) e Pillow
* **Banco de Dados:** PostgreSQL (Produção via Neon.tech) / SQLite (Desenvolvimento local)
* **Hospedagem e Deploy:** Render (Gunicorn) integrado via CI/CD com GitHub
* **Ambiente Local:** Linux (Crostini / ChromeOS) com ambiente virtual (`venv`) e VS Code

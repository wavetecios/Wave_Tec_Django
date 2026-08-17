======================================================
        WAVE TEC v1.0
Sistema de Assistência Técnica
======================================================

Obrigado por utilizar o sistema Wave Tec.

===========================
REQUISITOS
===========================

• Windows 10 ou superior
• Python 3.11 ou superior

Durante a instalação do Python marque:

[X] Add Python to PATH

===========================
KIT PARA OUTRO PC
===========================

1 - Copie toda a pasta Wave_Tec_Django para o novo computador.

2 - Abra a pasta do projeto.

3 - Execute o arquivo instalar.bat.

4 - O instalador vai:
   - verificar se o Python está instalado
   - criar a venv local do projeto
   - instalar as dependências do requirements.txt
   - rodar as migrações do banco

5 - Depois da instalação, execute iniciar.bat.

6 - O sistema abrirá no navegador em:
   http://127.0.0.1:8000

===========================
ARQUIVOS IMPORTANTES
===========================

• requirements.txt = dependências do projeto
• db.sqlite3 = banco local
• venv = ambiente virtual do projeto

===========================
BACKUP
===========================

Execute:

backup.bat

Sempre antes de atualizar o sistema ou antes de mover o projeto.

===========================
DESENVOLVIDO POR

Cristiano Sant' Ana Wave Tec
Sistema desenvolvido em Django.

Versão: 1.0
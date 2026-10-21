
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess
import os

try:
    import psutil
except ImportError:
    psutil = None


# Horizon Toolbar - prototipo 0.1
# Interface inspirada no HorizonOS Oneplex

BG = "#17191D"
PANEL = "#22252B"
ACCENT = "#8AB4F8"
TEXT = "#F1F3F4"
MUTED = "#A7ADB7"

root = tk.Tk()
root.title("Horizon Toolbar")
root.configure(bg=BG)
root.resizable(False, False)
root.attributes("-topmost", True)

WIDTH = 350
HEIGHT = 300

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# Posiciona o painel próximo ao canto inferior direito.
# O espaço reservado considera a barra de tarefas padrão.
root.geometry(
    f"{WIDTH}x{HEIGHT}+{screen_w - WIDTH - 16}+"
    f"{screen_h - HEIGHT - 65}"
)


def abrir_programa(comando):
    try:
        subprocess.Popen(comando, shell=True)
    except OSError as erro:
        messagebox.showerror(
            "Horizon Toolbar",
            f"Não foi possível abrir o programa:\n{erro}"
        )


def atualizar():
    agora = datetime.now()

    relogio.config(text=agora.strftime("%H:%M:%S"))
    data.config(text=agora.strftime("%d/%m/%Y"))

    if psutil:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()

        sistema.config(
            text=f"CPU: {cpu:.0f}%   |   RAM: {ram.percent:.0f}%"
        )
    else:
        sistema.config(
            text="Instale psutil para monitorar CPU e RAM."
        )

    root.after(1000, atualizar)


# Cabeçalho
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=16, pady=(14, 8))

tk.Label(
    header,
    text="HORIZON",
    font=("Consolas", 16, "bold"),
    bg=BG,
    fg=ACCENT
).pack(side="left")

tk.Label(
    header,
    text="TOOLBAR 0.1",
    font=("Consolas", 9),
    bg=BG,
    fg=MUTED
).pack(side="right", pady=5)


# Cartão do relógio
card = tk.Frame(root, bg=PANEL)
card.pack(fill="x", padx=12, pady=4)

relogio = tk.Label(
    card,
    text="00:00:00",
    font=("Consolas", 28, "bold"),
    bg=PANEL,
    fg=TEXT
)
relogio.pack(pady=(10, 0))

data = tk.Label(
    card,
    text="00/00/0000",
    font=("Segoe UI", 10),
    bg=PANEL,
    fg=MUTED
)
data.pack(pady=(0, 10))


# Monitoramento
sistema = tk.Label(
    root,
    text="Carregando informações...",
    font=("Consolas", 10),
    bg=BG,
    fg=ACCENT
)
sistema.pack(pady=9)


# Botões de acesso rápido
atalhos = tk.Frame(root, bg=BG)
atalhos.pack(fill="x", padx=12, pady=3)


def criar_botao(pai, texto, comando):
    return tk.Button(
        pai,
        text=texto,
        command=comando,
        font=("Segoe UI", 9),
        bg=PANEL,
        fg=TEXT,
        activebackground=ACCENT,
        activeforeground=BG,
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=8
    )


criar_botao(
    atalhos, "Terminal",
    lambda: abrir_programa(["cmd.exe"])
).pack(side="left", fill="x", expand=True, padx=3)

criar_botao(
    atalhos, "Arquivos",
    lambda: abrir_programa(["explorer.exe"])
).pack(side="left", fill="x", expand=True, padx=3)

criar_botao(
    atalhos, "Tarefas",
    lambda: abrir_programa(["taskmgr.exe"])
).pack(side="left", fill="x", expand=True, padx=3)


# Rodapé
rodape = tk.Frame(root, bg=BG)
rodape.pack(fill="x", padx=15, pady=(7, 10))

tk.Label(
    rodape,
    text="HorizonOS Oneplex",
    font=("Segoe UI", 8),
    bg=BG,
    fg=MUTED
).pack(side="left")

tk.Button(
    rodape,
    text="Fechar",
    command=root.destroy,
    font=("Segoe UI", 8),
    bg=BG,
    fg=MUTED,
    activebackground=PANEL,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2"
).pack(side="right")


# Inicia as atualizações
if psutil:
    psutil.cpu_percent(interval=None)

atualizar()
root.mainloop()

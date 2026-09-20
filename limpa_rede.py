#!/usr/bin/env python3
"""Diagnostico e reparo conservador de conectividade para Windows e Linux."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import platform
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


LOG_DIR = Path.home() / ".limpa-rede" / "logs"
HOSTS_MARKERS = ("whatsapp", "facebook", "meta", "youtube")
CHECKS = (
    ("DNS", "https://www.google.com/generate_204"),
    ("WhatsApp Web", "https://web.whatsapp.com"),
    ("YouTube", "https://www.youtube.com/generate_204"),
)


class App:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_path = LOG_DIR / f"limpa-rede-{stamp}.log"

    def log(self, message: str) -> None:
        print(message)
        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")

    def run(self, command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str] | None:
        shown = " ".join(command)
        self.log(f"$ {shown}")
        if self.dry_run:
            self.log("  [simulacao] comando nao executado")
            return None
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=check)
        except (FileNotFoundError, PermissionError) as error:
            self.log(f"  [aviso] {error}")
            return None
        if result.stdout.strip():
            self.log(result.stdout.strip())
        if result.stderr.strip():
            self.log(result.stderr.strip())
        return result

    def hosts_path(self) -> Path:
        if platform.system() == "Windows":
            return Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "drivers" / "etc" / "hosts"
        return Path("/etc/hosts")

    def diagnose(self) -> None:
        self.log(f"Sistema: {platform.platform()}")
        self.log(f"Hostname: {socket.gethostname()}")
        self.log("\nTestando conectividade HTTP:")
        for name, url in CHECKS:
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "limpa-rede/1.0"})
                with urllib.request.urlopen(request, timeout=8) as response:
                    self.log(f"  [OK] {name}: HTTP {response.status}")
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                self.log(f"  [FALHA] {name}: {error}")
        self.log("\nResolucao DNS:")
        for host in ("web.whatsapp.com", "www.youtube.com"):
            try:
                addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, 443)})
                self.log(f"  [OK] {host}: {', '.join(addresses[:4])}")
            except socket.gaierror as error:
                self.log(f"  [FALHA] {host}: {error}")
        self.log(f"\nLog salvo em: {self.log_path}")

    def flush_dns(self) -> None:
        system = platform.system()
        if system == "Windows":
            self.run(["ipconfig", "/flushdns"])
        elif shutil.which("resolvectl"):
            self.run(["resolvectl", "flush-caches"])
        elif shutil.which("systemd-resolve"):
            self.run(["systemd-resolve", "--flush-caches"])
        else:
            self.log("[aviso] Nenhum comando de limpeza DNS conhecido foi encontrado.")

    def clean_hosts(self) -> None:
        path = self.hosts_path()
        if not path.exists():
            self.log(f"[aviso] Arquivo hosts nao encontrado: {path}")
            return
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
        except PermissionError:
            self.log(f"[erro] Sem permissao para ler {path}. Execute como administrador/root.")
            return
        kept = []
        removed = []
        for line in original.splitlines(keepends=True):
            fields = line.split("#", 1)[0].split()
            domains = fields[1:] if len(fields) >= 2 else []
            if any(marker in domain.lower() for domain in domains for marker in HOSTS_MARKERS):
                removed.append(line.rstrip())
            else:
                kept.append(line)
        if not removed:
            self.log("[OK] Nenhuma entrada relacionada a WhatsApp, Meta ou YouTube foi encontrada no hosts.")
            return
        self.log(f"[acao] {len(removed)} entrada(s) suspeita(s) encontrada(s) em {path}.")
        if self.dry_run:
            return
        backup = path.with_name(path.name + f".bak-{dt.datetime.now():%Y%m%d-%H%M%S}")
        try:
            shutil.copy2(path, backup)
            path.write_text("".join(kept), encoding="utf-8", newline="")
        except OSError as error:
            self.log(f"[erro] Nao foi possivel atualizar hosts: {error}")
            return
        self.log(f"[OK] Backup salvo em {backup}; entradas removidas com preservacao do restante do arquivo.")

    def reset_stack(self) -> None:
        if platform.system() != "Windows":
            self.log("[aviso] Reset automatico da pilha esta implementado apenas para Windows.")
            return
        self.run(["ipconfig", "/release"])
        self.run(["ipconfig", "/renew"])
        self.run(["netsh", "winsock", "reset"])
        self.run(["netsh", "int", "ip", "reset"])

    def repair(self, reset_stack: bool) -> None:
        self.flush_dns()
        self.clean_hosts()
        if reset_stack:
            self.reset_stack()
        self.log("\nReparo concluido. Execute novamente com 'diagnostico' para conferir o resultado.")
        self.log(f"Log salvo em: {self.log_path}")


def is_admin() -> bool:
    if platform.system() == "Windows":
        import ctypes

        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    return os.geteuid() == 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnostica e repara problemas comuns de conectividade.")
    parser.add_argument("acao", choices=("diagnostico", "reparo"), nargs="?", default="diagnostico")
    parser.add_argument("--dry-run", action="store_true", help="Mostra as acoes sem modifica-las")
    parser.add_argument("--reset-stack", action="store_true", help="No Windows, renova IP e reseta Winsock/TCP-IP")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    app = App(args.dry_run)
    if args.acao == "diagnostico":
        app.diagnose()
        return 0
    if not is_admin() and not args.dry_run:
        app.log("[erro] O reparo precisa ser executado como administrador/root.")
        return 2
    app.repair(args.reset_stack)
    return 0


if __name__ == "__main__":
    sys.exit(main())
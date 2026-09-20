# Limpa Rede

Ferramenta para Windows que diagnostica e faz reparos conservadores em falhas de conectividade no WhatsApp Web, YouTube e navegacao geral.

## O que mudou

- Funciona no Windows usando Python 3.10 ou superior.
- O modo padrao apenas diagnostica; nenhuma configuracao e alterada.
- O reparo limpa o cache DNS e remove apenas entradas suspeitas do arquivo `hosts`.
- O arquivo `hosts` e preservado: antes da alteracao e criado um backup com data e hora.
- O reset de IP, Winsock e TCP/IP no Windows e opcional.
- Todas as operacoes ficam registradas em `~/.limpa-rede/logs`.
- Nao altera DNS, firewall, proxy, navegador ou politicas corporativas automaticamente.

## Uso

Diagnostico seguro:

```bash
python limpa_rede.py diagnostico
```

Simular um reparo sem alterar nada:

```bash
python limpa_rede.py reparo --dry-run
```

Executar o reparo no PowerShell como Administrador:

```bash
python limpa_rede.py reparo
```

No Windows, incluir renovacao de IP e reset da pilha de rede:

```powershell
python limpa_rede.py reparo --reset-stack
```

## Usar no Windows

Para uma versao com Python instalado, execute `limpa rede.bat` e escolha uma opcao no menu. Para distribuir somente o executavel, use `dist\LimpaRede.exe`.

## Gerar executavel

Com Python instalado:

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --name LimpaRede limpa_rede.py
```

O executavel sera criado em `dist\LimpaRede.exe`. O PyInstaller gera binarios para o sistema em que o build e executado.

## Baixar e usar

1. Baixe o arquivo `LimpaRede-Windows.zip` na secao **Releases**.
2. Extraia o arquivo em uma pasta.
3. Execute `limpa rede.bat` como administrador.
4. Escolha `1` para diagnosticar ou `2` para simular um reparo.

O codigo-fonte e os arquivos para gerar o executavel estao neste repositorio. O download pronto para uso fica em **Releases**, separado do codigo-fonte.
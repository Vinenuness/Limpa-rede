# Limpa Rede

Ferramenta gratuita para Windows, desenvolvida em Python, para diagnosticar problemas de conectividade e executar reparos conservadores relacionados a rede, DNS e arquivo `hosts`.

O projeto foi desenvolvido com foco em seguranca, transparencia e controle do usuario. O diagnostico nao altera o sistema, e o modo de simulacao permite verificar as acoes antes de executar qualquer reparo.

## Por que o Limpa Rede?

Problemas de conectividade podem estar relacionados ao cache DNS, a configuracoes da rede ou a entradas incorretas no arquivo `hosts`.

O Limpa Rede reune verificacoes e procedimentos de manutencao em uma unica ferramenta. Assim, o usuario pode identificar possiveis problemas e executar reparos de forma controlada, com registro das operacoes realizadas.

## Principais recursos

- Compatibilidade com Windows e Python 3.10 ou superior.
- Diagnostico de conectividade HTTP e resolucao DNS.
- Simulacao de reparos antes da execucao das alteracoes.
- Limpeza do cache DNS.
- Verificacao de entradas relacionadas a WhatsApp, Meta e YouTube no arquivo `hosts`.
- Backup do arquivo `hosts` antes de modificacoes.
- Renovacao do endereco IP.
- Opcao de reset da pilha de rede do Windows.
- Registro das operacoes realizadas em arquivos de log.
- Nao altera automaticamente DNS, firewall, proxy, navegador ou politicas corporativas.

## Download para Windows

Baixe a versao pronta na [Release mais recente](https://github.com/Vinenuness/Limpa-rede/releases/latest).

1. Baixe `LimpaRede-Windows.zip` na secao **Assets**.
2. Extraia o arquivo ZIP em uma pasta.
3. Mantenha `LimpaRede.exe` e `limpa rede.bat` na mesma pasta.
4. Execute `limpa rede.bat` como administrador.
5. Escolha uma opcao no menu.

O pacote inclui o executavel e nao exige Python instalado.

## Como usar

### Diagnostico

Executa verificacoes de conectividade sem modificar configuracoes do sistema.

```powershell
python limpa_rede.py diagnostico
```

### Simulacao de reparo

Mostra as acoes previstas sem realizar alteracoes.

```powershell
python limpa_rede.py reparo --dry-run
```

### Reparo conservador

Limpa o cache DNS e verifica entradas suspeitas no arquivo `hosts`. Execute em um PowerShell como Administrador.

```powershell
python limpa_rede.py reparo
```

### Reparo com reset da pilha de rede

Tambem renova o endereco IP e reseta Winsock e TCP/IP.

```powershell
python limpa_rede.py reparo --reset-stack
```

## Usar o launcher do Windows

Com Python instalado, execute `limpa rede.bat` e escolha uma opcao no menu. O launcher procura `LimpaRede.exe` na mesma pasta e, caso ele nao esteja disponivel, tenta executar `limpa_rede.py` com o Python instalado.

As opcoes disponiveis sao:

- Diagnostico.
- Simulacao de reparo.
- Reparo conservador.
- Reparo com reset da pilha de rede.

## Logs e backups

As operacoes realizadas ficam registradas em:

```text
%USERPROFILE%\.limpa-rede\logs\
```

Antes de modificar o arquivo `hosts`, a ferramenta cria um backup com data e hora no mesmo diretorio do arquivo original. O restante do arquivo e preservado.

## Gerar executavel

Com Python instalado, instale o PyInstaller:

```powershell
python -m pip install pyinstaller
```

Depois, gere o executavel:

```powershell
pyinstaller --onefile --name LimpaRede limpa_rede.py
```

O arquivo sera criado em `dist\LimpaRede.exe`. O PyInstaller gera binarios para o sistema em que o build e executado.

## Tecnologias utilizadas

- Python
- Windows
- PowerShell
- DNS
- TCP/IP
- Arquivo `hosts`
- PyInstaller

## Estrutura do projeto

```text
Limpa-rede/
├── limpa_rede.py
├── limpa rede.bat
├── LimpaRede.spec
├── README.md
└── .gitignore
```

## Seguranca e limitacoes

Por padrao, o diagnostico nao modifica o sistema. Recomenda-se executar primeiro a simulacao (`--dry-run`) antes de realizar um reparo.

A ferramenta nao substitui ferramentas corporativas de gerenciamento de rede, politicas de seguranca ou procedimentos de suporte tecnico. Use o reset da pilha de rede com atencao, pois ele pode exigir uma reinicializacao do Windows ou reconfiguracao da conexao.

## Codigo-fonte

O codigo-fonte esta disponivel publicamente neste repositorio. Sugestoes e melhorias sao bem-vindas.

# Limpa Rede

Ferramenta gratuita para Windows desenvolvida em Python para **diagnosticar problemas de conectividade** e executar **reparos conservadores** relacionados à rede, DNS e arquivo `hosts`.

O projeto foi desenvolvido com foco em **segurança, transparência e controle do usuário**, permitindo realizar diagnósticos e simular reparos antes de executar alterações no sistema.

## Por que o Limpa Rede?

Problemas de conectividade podem estar relacionados a cache DNS, configurações de rede ou entradas no arquivo `hosts`.

O Limpa Rede reúne verificações e procedimentos de manutenção em uma única ferramenta, permitindo identificar possíveis problemas e executar reparos de forma controlada.

## Principais recursos

- Compatível com **Windows** e **Python 3.10 ou superior**.
- Modo de diagnóstico que não altera configurações do sistema.
- Simulação de reparos antes da execução das alterações.
- Limpeza do cache DNS.
- Verificação de entradas relacionadas a WhatsApp, Meta e YouTube no arquivo `hosts`.
- Backup do arquivo `hosts` antes de modificações.
- Renovação do endereço IP.
- Opção de reset da pilha de rede do Windows.
- Registro das operações realizadas em arquivos de log.
- Não altera automaticamente configurações de DNS, firewall, proxy, navegador ou políticas corporativas.

## Como usar

### 🔍 Diagnóstico

Executa verificações de conectividade sem modificar configurações do sistema.

```bash
python limpa_rede.py diagnostico

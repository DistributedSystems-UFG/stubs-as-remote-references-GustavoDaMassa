[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/TPGyf4AW)

# ASR08 — Implementação de Referências Remotas

Demonstração de stubs como referências remotas em RPC (Nota 4.8, Tanenbaum & van Steen). O exemplo implementa uma lista distribuída acessada por múltiplos clientes, onde o stub da lista é passado como parâmetro entre processos — um processo passa a referência remota para outro, que a usa para acessar o servidor transparentemente.

## Mecanismo demonstrado (parte a)

O cenário (Fig. 4.20 do livro) funciona assim:

1. **Client 1** conecta ao servidor e cria uma lista remota (`DBClient.create()` → servidor retorna um `listID`).
2. Client 1 adiciona um elemento à lista via stub (`DBClient.appendData('Client 1')`).
3. Client 1 serializa o próprio objeto `DBClient` (que contém `host`, `port` e `listID`) com `pickle` e o envia para Client 2 via socket.
4. **Client 2** recebe o objeto desserializado — agora tem um stub idêntico apontando para a **mesma lista** no servidor.
5. Client 2 adiciona dados à mesma lista (`appendData('Client 2')`) sem saber como a lista foi criada.
6. Client 2 chama `getValue()` e obtém `['Client 1', 'Client 2']`.

O stub (`DBClient`) é a **referência remota**: encapsula localização (`host:port`) e identidade (`listID`). Passá-lo como parâmetro é equivalente a passar uma referência em linguagens OO, exceto que aponta para um objeto em outro processo.

## Diferença local vs. AWS (parte c)

Na versão local todos os processos rodam na mesma máquina e os sockets se conectam a `localhost`. Na versão AWS os três processos rodam em instâncias EC2 separadas. As **únicas mudanças** são nos endereços IP em `constRPC.py` — a semântica das chamadas é idêntica: do ponto de vista do `DBClient`, ele sempre faz uma conexão TCP, serializa a operação com pickle e aguarda a resposta. O fato de o servidor estar em outra máquina física é completamente transparente para o código cliente.

A única diferença semântica observável é a **latência**: localmente as chamadas são praticamente instantâneas; na AWS há latência de rede (tipicamente 1-5ms entre instâncias na mesma região), o que pode tornar a janela de tempo entre o `sendTo` e o `recvAny` mais crítica para a sincronização manual (o `time.sleep(1)` em `run_client1.py`).

## Dependências

Python 3 — usa apenas `socket`, `pickle` e `multiprocessing` (stdlib).

## Como executar

### Demo local (uma máquina)

```bash
python3 run.py
```

### AWS (3 instâncias EC2)

Configure os IPs nas variáveis de ambiente antes de executar cada script:

**Instância 1 — Servidor:**
```bash
python3 run_server.py
```

**Instância 3 — Client 2 (inicie antes do Client 1):**
```bash
CLIENT2_HOST=<IP_instancia3> SERVER_HOST=<IP_instancia1> python3 run_client2.py
```

**Instância 2 — Client 1:**
```bash
SERVER_HOST=<IP_instancia1> CLIENT2_HOST=<IP_instancia3> python3 run_client1.py
```

### Saída esperada

```
# Instância 2 (Client 1)
[Client1] sent stub to client2 at <IP>:50054

# Instância 3 (Client 2)
[Client2] waiting for stub on port 50054...
[Client2] final list: ['Client 1', 'Client 2']
```

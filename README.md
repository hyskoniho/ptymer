
# PTymer

**PTymer** é um projeto em Python que fornece insights e ações dentro da execução de um código em contexto de tempo. Este pacote inclui três classes principais: `Timer`, `HourGlass` e `Alarm`, cada uma com funcionalidades específicas para monitoramento e controle de tempo.

## Índice

- [Instalação](#instalação)
- [Uso](#uso)
  - [Timer](#timer)
  - [HourGlass](#hourglass)
  - [Alarm](#alarm)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Instalação

PTYMER é compatível com Python 3.8 ou superior. Para instalar, use o pip:

```bash
pip install ptymer
```

## Uso

#### Timer
A classe Timer é usada para medir o tempo de execução de trechos de código. Ela pode ser instanciada de várias maneiras:
##### Instância Normal
```python
from ptymer import Timer

tm = Timer().start()
# Seu código aqui
tm.stop()
```

##### Gerenciador de Contexto
```python
from ptymer import Timer

with Timer() as tm:
    # Seu código aqui
```

##### Decorador
```python
from ptymer import Timer

@Timer()
def sua_funcao_aqui():
```

A classe Timer também possui a função ***Mark***, que cria uma marca de tempo no momento em que é chamada e, ao finalizar a instância Timer, é exibida uma lista com as marcas de tempo.

#### HourGlass
A classe ***HourGlass*** é usada para criar uma contagem regressiva. Após finalizar a contagem, ela executa uma função definida pelo usuário.
```python
from ptymer import HourGlass

hg = HourGlass(seconds=5, visibility=True, target=print, args=("Hello World",)).start()
```

*Nota:* Na tupla de argumentos, você precisa colocar uma vírgula no final para identificar que é uma tupla se houver apenas um elemento.

#### Alarm
A classe ***Alarm*** recebe uma lista de horários e uma função. Quando o algoritmo identifica que chegou em um dos horários, ele executa a função definida.
```python
from ptymer import Alarm

alarm = Alarm(target=target, args=(), schedules=["10:49:00"], visibility=True).start()
```

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório do GitHub.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
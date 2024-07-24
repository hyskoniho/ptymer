<div align="center">
  <h1>PTymer ⏱️</h1>
  <br></br>
  <img src="https://img.shields.io/badge/core-python-%2314354C.svg?style=for-the-badge">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://img.shields.io/badge/status-online-green?style=for-the-badge">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge">
</div>

**PTymer** is a Python project that provides insights and actions within the execution of code in a time context. This package includes three main classes: `Timer`, `HourGlass`, and `Alarm`, each with specific functionalities for time monitoring and control. You can find the full description in the [Wiki Page](https://github.com/hyskoniho/ptymer/wiki).

## Index

- [Installation](#installation)
- [Usage](#usage)
  - [Timer](#timer)
  - [HourGlass](#hourglass)
  - [Alarm](#alarm)
- [Contribution](#contribution)
- [License](#license)
- 
## Installation

PTymer is compatible with Python 3.8 and later versions, and is officially available on [PyPI](https://pypi.org/project/ptymer/). You can install it using pip:

```bash
pip install ptymer
```

## Usage

#### Timer
The Timer class is used to measure the execution time of code snippets. It can be instantiated in several ways:
##### Normal Instance
```python
from ptymer import Timer

tm = Timer().start()
# Your code here
tm.stop()
```

##### Context Manager
```python
from ptymer import Timer

with Timer() as tm:
    # Your code here
```

##### Decorator
```python
from ptymer import Timer

@Timer()
def your_function_here():
```


#### HourGlass
The HourGlass class is used to create a countdown timer. After the countdown finishes, it executes a user-defined function.
```python
from ptymer import HourGlass

hg = HourGlass(seconds=5, visibility=True, target=print, args=("Hello World",)).start()
```

*Note:* In the arguments tuple, you need to put a comma at the end to identify it as a tuple if there's only one element.

#### Alarm
The Alarm class takes a list of times and a function. When the algorithm identifies that it has reached one of the times, it executes the defined function.
```python
from ptymer import Alarm

alarm = Alarm(schedules=["10:49:00"], target=target, args=(), visibility=True).start()
```

<br></br>

###### ⚠️ WARNING!
Due to multiprocessing, it's highly recommended that you safeguard the execution of the main process, when using `HourGlass` and/or `Alarm` instance, with the following statement before your code:
```python
if __name__ == '__main__':
    # your code here
```
Some sample usage:
```python
def foo():
    return True

if __name__ == '__main__':
    foo()
```
You can find more information about this issue [here](https://github.com/hyskoniho/ptymer/wiki/Handling-Parallelism).

## Contribution
Contributions are welcome!!! Feel free to open issues and pull requests on the GitHub repository.
Pay attention to the [test files](https://github.com/hyskoniho/ptymer/tree/main/tests) content and don't forget to document every change!
We use Pytest and there's a [workflow](https://github.com/hyskoniho/ptymer/blob/main/.github/workflows/unit_test.yaml) set up on GitHub Actions that you might want to check out.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/hyskoniho/ptymer/blob/main/LICENSE) file for more details.

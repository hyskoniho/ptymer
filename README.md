
# PTymer

**PTymer** is a Python project that provides insights and actions within the execution of code in a time context. This package includes three main classes: `Timer`, `HourGlass`, and `Alarm`, each with specific functionalities for time monitoring and control.

## Index

- [Installation](#installation)
- [Usage](#usage)
  - [Timer](#timer)
  - [HourGlass](#hourglass)
  - [Alarm](#alarm)
- [Contribution](#contribution)
- [License](#license)

## Installation

PTymer is compatible with Python 3.8 or higher. 
To install, use pip:

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

alarm = Alarm(target=target, args=(), schedules=["10:49:00"], visibility=True).start()
```

## Contribution
Contributions are welcome! Feel free to open issues and pull requests on the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
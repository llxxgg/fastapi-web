
# 类型提示

函数参数使用类型提示后，在函数体中使用参数时，可以自动提示参数的类型和方法；

而且编辑器知道变量的类型，还能进行错误检查；

```python
def get_full_name(first_name: str, last_name: str):
    return first_name.title() + ' ' + last_name.title()
```

# Any类型

typing模块，导入Any类型，表示任意类型：

```python
from typing import Any  
def get_value(value: Any):
    return value
```

# 泛型

有些类型可以在方括号中接收“类型参数”（type parameters），用于声明其内部值的类型。比如“字符串列表”可以写为 `list[str]`。

这些能接收类型参数的类型称为“泛型类型”（Generic types）或“泛型”（Generics）。

你可以把相同的内建类型作为泛型使用（带方括号和内部类型）：

- list
- tuple
- set
- dict

# Pydantic模型

是一个执行数据校验的Python库

你用一些值创建这个类的实例，它会校验这些值，并在需要时把它们转换为合适的类型，返回一个包含所有数据的对象。

# asyncio库

asyncio是python3.4引入的一个库，提供了异步I/O、事件循环、协程和任务等功能。

如何用asyncio定义协程？

async关键字定义一个函数为协程函数，调用这个函数会返回一个协程对象，并不会执行。

asyncio中几个重要的概念：
- 事件循环（Event Loop）：asyncio中开启的一个无限的时间循环，asyncio会自动在满足条件时去调用相应的协程对象，
我们只需要将协程对象注册到该时间循环上即可。
- Coroutine ：协程对象，指一个用async来定义的函数，它在调用时不会立即执行，而是返回一个协程对象。协程对象需要注册
到事件循环，由事件循环进行调用。
- Future：代表将来执行或没有执行的任务的结果。
- task：是协程的进一步封装，其中包含任务的各种状态。task对象是Future的子类。

**以上几个概念，待通过代码理解**


协程的工作流程：

- 定义/创建协程对象
- 定义事件循环对象容器
- 将协程转为task任务
- 将task任务注册到事件循环对象容器中

```python
import asyncio

async def hello(name: str)->str:
    await asyncio.sleep(5)
    return f"Hello, {name}!"

coro = hello("World")

loop = asyncio.get_event_loop()

# task = loop.create_task(coro)
task = asyncio.ensure_future(coro)

loop.run_until_complete(task)

print(task.result())
```

```python
import asyncio

async def hello(x: int)->str:
    print("等待中.")
    await asyncio.sleep(x)
    return "等待{}".format(x)

coro1 = hello(1)
coro2 = hello(2)
coro3 = hello(3)

tasks = [
    asyncio.ensure_future(coro1),
    asyncio.ensure_future(coro2),
    asyncio.ensure_future(coro3),
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print(task.result())
```

async声明异步函数。通过await调用异步函数，等待其完成并获取结果。

await 执行的效果，和 Python 正常执行是一样的，也就是说程序会阻塞在这里，进入被调用的协程函数，执行完毕返回后再继续。

await相当于将协程挂起，等待被调用的协程函数执行完毕后再继续执行当前协程函数。从而让出线程执行其他协程。


python多线程是伪并发，只有一个线程执行。

并发通常用于 I/O 操作频繁的场景，而并行则适用于 CPU heavy 的场景。


asyncio.run(coro) 是 Asyncio 的 root call，表示拿到 event loop，运行输入的 coro，直到它结束，
最后关闭这个 event loop。事实上，asyncio.run() 是 Python3.7+ 才引入的，相当于老版本的以下语句：

```python

# asyncio.run(coro)
# 等价于以下代码：

import asyncio

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(coro)
finally:
    loop.close()
```

asyncio.run() 是异步程序的 “总开关”，它做了 3 件关键事情：
- 创建一个全新的事件循环
- 运行你传入的主协程（直到结束）
- 关闭事件循环，清理资源

它是整个异步程序的入口。

asyncio.create_task() = 并发任务，只能用在已运行的协程内； 它完成三件事：
- 包装：把协程 do_something() 包装成 Task 对象
- 注册：把这个任务加入当前正在运行的事件循环
- 调度：告诉事件循环：这个任务可以并发跑了

# 并发编程

## 进程和线程

- 进程： 计算机进行资源分配的基本单位，每个进程都有独立的内存空间和系统资源。
- 线程： CPU调度的基本单位

一个进程中可以有多个线程，同一个进程中的线程可以共享进程中的资源。

## 多线程

```python
import threading
import time


def go_work():
    print("start sleep")
    time.sleep(3)
    print("say hello")
    
    
for i in range(10):
    threading.Thread(target=go_work).start()
```

threading.Thread 创建线程时，默认是非守护线程，主线程必须等待所有非守护线程执行完，主线程才会退出。

如果你想让主线程一结束，子线程立刻退出，可以把子线程设置为守护线程：`threading.Thread(target=go_work, daemon=True).start()`

## 多进程

```python
import multiprocessing
import time


def go_work():
    print("start sleep")
    time.sleep(3)
    print("say hello")


if __name__ == '__main__':
    for i in range(2):
        multiprocessing.Process(target=go_work).start()
```

原因：macOS 上 multiprocessing 默认使用 spawn 启动方式，子进程会重新导入主模块。原代码在模块顶层直接 for
循环创建进程，子进程导入时又会执行同样的代码，触发递归创建进程的保护机制。

修复：将创建进程的代码放入 `if __name__ == '__main__': `块中，确保只有主进程执行该逻辑。


- 非守护进程（默认）：主进程要等它执行完，程序才会退出。
- 守护进程：主进程一退出，它立刻被杀死，不管有没有执行完。


# GIL（全局解释器锁）

GIL 是CPython解释器特有的，让一个进程中同一时刻只能有一个线程可以被CPU调度。

- 计算密集型，适合多进程开发
- IO密集型，适合用多线程，例如文件读写、网络传输

GIL释放时机：
- 线程执行I/O操作时，GIL会被释放，让其他线程有机会执行。
- 另一个机制，叫做check_interval，意思是CPython解释器会去轮训检查GIL的锁住情况。
每隔一段时间，Python 解释器就会强制当前线程去释放 GIL，这样别的线程才能有执行的机会。

GIL引入的原因：CPython的内存管理不是线程安全的，GIL保证了同一时刻只有一个线程执行Python字节码，从而避免了内存管理的竞争条件。

请注意，GIL并不是Python语言的特性，而是CPython解释器的实现细节。其他Python解释器（如Jython、IronPython）没有GIL。

GIL的存在只是使得CPython在实现层面变的方便。


# 内存回收

引用计数法为主，标记清除和分代回收为辅。

## 引用计数法

1. 环状的双向链表：元素中包含引用计数器
2. 循环引用的问题


## 标记清除

为了解决引用计数法的循环引用问题，Python引入了标记清除机制。

它会定期扫描内存中的对象，标记那些不可达的对象，并将它们清除掉。

实现：维护一个循环双向链表，专门存放那些可能存在循环引用的对象（list/tuple/dict/set）

问题：
- 什么时候扫描？
- 扫描代价比较大，需要扫描链表和元素中的元素，每次扫描耗时

## 分代回收

将可能存在循环引用的对象维护成3个链表：
- 0代 对象个数达到700个扫描一次
- 1代 0代扫描10次，1代扫描一次
- 2代 1代扫描10次，2代扫描一次

## 小结

使用引用计数法，但是存在循环引用的问题，为了解决这个问题，又引入了标记清除和分代回收机制，在其内部维护了4个链表

- refchain
- 2代
- 1代
- 0代

## 缓存

1. 为了避免重复创建和销毁一些常见对象，python内部会帮我门创建-5、-4,..., 257的整数对象，并且在内存中缓存它们。
当我们使用这些整数时，python会直接返回这些缓存的对象，而不是创建新的对象。

2. free_list机制
当一个对象的引用计数器为0时，内部不会直接回收，而是将对象添加到free_list链表中当缓存，
以后再去创建对象时，不再重新开辟内存，而是直接使用free_list链表中的对象。

添加到free_list中的对象何时被销毁？free_list满了，会集中回收。

典型有：
- 浮点数 float
- 空 / 小 list、tuple、dict（有长度限制）
- 内部小对象（PyObjects 等）

每个类型单独一个 free_list，每种类型的free_list长度限制不同（list 默认最多 80 个，tuple 每个长度最多 2000 个等）

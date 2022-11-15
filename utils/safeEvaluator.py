import asyncio
import math
import multiprocessing
import threading
import time


def _eval(queue, code):
    try:
        res = (eval(code, {'__builtins__': SafeEvaluator.allowed_functions}))
    except Exception as e:
        res = e
        queue.put(False)
    else:
        queue.put(True)
    queue.put(res)


class SafeEvaluator:
    class UnsafeException(Exception): pass
    class TimeoutException(Exception): pass

    allowed_functions = {
        "range": range,
        "list": list,
        "set": set,
        "str": str,
        "int": int,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "asin": lambda x: math.degrees(math.asin(x)),
        "acos": lambda x: math.degrees(math.acos(x)),
        "atan": lambda x: math.degrees(math.atan(x)),
        "hypotenuse": math.hypot,
        "pow": pow,
        "pi": math.pi,
        "e": math.e,
        "deg": math.degrees,
        "rad": math.radians,
        "abs": abs,
        "fact": math.factorial,
        "sum": sum,
        "log": math.log,
        "sqrt": math.sqrt,
        "gamma": math.gamma
    }

    def __init__(self, expression: str):
        self.expression = expression
        self.finished = False
        self.error = False
        self.onFinishListeners = []
        self.asyncOnFinishListeners = []
        self.thread = None
        self.result = multiprocessing.Queue()

    def start(self):
        if not self.isExpressionSafe():
            self.finishWithException(self.UnsafeException("Unsafe expression"))
            return
        self.thread = threading.Thread(target=self.asyncThread)
        self.thread.start()

    def addOnFinishListener(self, listener, args=None):
        if args is None:
            args = ()
        self.onFinishListeners.append([listener, args])

    def addAsyncOnFinishListener(self, listener, args=None):
        if args is None:
            args = ()
        self.asyncOnFinishListeners.append([listener, args])

    def isExpressionSafe(self):
        if "__" in self.expression or "import" in self.expression:
            return False
        return True

    def asyncThread(self):
        evaluateProcess = multiprocessing.Process(target=_eval, args=(self.result, self.expression))
        evaluateProcess.start()
        evaluateProcess.join(timeout=1)
        time.sleep(0.1)
        if not evaluateProcess.is_alive():
            self.error = self.result.get()
            if not self.error:
                self.finishWithException(self.result.get())
            else:   # if finished without exception
                self.finishWithResult(self.result.get() if not self.result.empty() else None)
        else:
            evaluateProcess.terminate()

            self.finishWithException(self.TimeoutException("Timeout"))

    def onFinished(self):
        for listener in self.onFinishListeners:
            listener[0](self, *listener[1])
        loop = asyncio.new_event_loop()
        from __main__ import bot
        for listener in self.asyncOnFinishListeners:
            bot.client.loop.create_task(listener[0](self, *listener[1]))

    def finishWithException(self, exception):
        self.error = exception
        self.result = None
        self.finished = True
        self.onFinished()

    def finishWithResult(self, result):
        self.result = result
        self.error = False
        self.finished = True
        self.onFinished()


def onFinishedListener(callbackCtx):
    if callbackCtx.error:
        print("Error: " + str(callbackCtx.error))
    else:
        print(callbackCtx.result)

#!/usr/bin/env python3
"""
Small command line programm to pose addition and substraction tasks.
"""

import random
import operator

limit = 100


class Inquisitor(object):
    """Class to generate questions.

    Methods:
    ask_for_type() : promt the user for the possible types of tasks
    ask_task() : displays a compute task and checks entered result

    """

    def __init__(self, limit=100):
        self.limit = limit
        self.types = []
        self.ask_for_type()
        self.ask()

    def ask_for_type(self, *args, **kwargs):
        """Ask for the type of calculation."""
        while True:
            types = []
            type_str = input(u"Was möchtest du rechnen (+-)?")
            if '+' in type_str:
                types.append(AddTask)
            if '-' in type_str:
                types.append(SubTask)
            if types:
                break
        self.types.extend(types)
        # remove duplicate entries
        self.types = [*{*self.types}]

    def ask(self):
        """Ask questions until interupted."""
        for task_cls in self._get_task_class():
            task = task_cls(limit=self.limit)
            while not task.validate():
                task.ask()
                if task.validate():
                    print("Richtig! 😊")
                else:
                    print("Leider falsch. 😒")

    def _get_task_class(self):
        while True:
            yield random.choice(self.types)


class Task(object):
    """A single task.

    Privides methods for inquiring input and for validation of the result.
    """

    type = "?"

    @classmethod
    def op(cls, x, y):
        return None

    def __init__(self, limit):
        self.limit = limit
        self.number1, self.number2 = self._get_numbers()
        self.result = None

    def _get_numbers(self):
        """Create addition task."""
        number1 = random.randint(1, self.limit - 1)
        number2 = random.randint(1, self.limit - number1)
        return number1, number2

    def ask(self):
        """Promt user for result."""
        result = input(
            "{} {} {} = ".format(self.number1, self.type, self.number2)
        )
        try:
            self.result = int(result)
        except Exception:
            self.result = None
        return self.result

    def validate(self,):
        """Return True if correct result entered, else False."""
        correct = (self.result == self.op(self.number1, self.number2))
        return correct


class AddTask(Task):
    """Task for addition."""

    op = operator.add
    type = "+"

    def _get_numbers(self):
        """Return summands."""
        number1 = random.randint(1, self.limit - 1)
        number2 = random.randint(1, self.limit - number1)
        return number1, number2


class SubTask(Task):
    """Task for substraction."""

    op = operator.sub
    type = "-"

    def _get_numbers(self):
        """Return summands."""
        number1 = random.randint(2, self.limit)
        number2 = random.randint(1, number1 - 1)
        return number1, number2


if __name__ == "__main__":
    inquisitor = Inquisitor(limit)

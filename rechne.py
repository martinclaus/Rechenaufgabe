#!/usr/bin/env python3
"""
Small command line programm to pose addition and substraction tasks.
"""

import random
import operator
from timeit import default_timer as timer

limit = 100
time_limit = 600


class Inquisitor(object):
    """Class to generate questions.

    Methods:
    ask_for_type() : promt the user for the possible types of tasks
    ask_task() : displays a compute task and checks entered result

    """

    correct_emoji = "😀😃😄😁😆😅🤣🙃😉😊"

    def __init__(self, limit=limit, time_limit=time_limit):
        self.limit = limit
        self.time_limit = time_limit
        self.tasks = []
        self.n_correct = 0
        self.n_asked = 0
        self.ask_for_type()
        self.ask()

    def ask_for_type(self, *args, **kwargs):
        """Ask for the type of calculation."""
        while True:
            tasks = []
            type_str = input(u"Was möchtest du rechnen (+-*)?")
            if '+' in type_str:
                tasks.append(AddTask(limit=self.limit))
            if '-' in type_str:
                tasks.append(SubTask(limit=self.limit))
            if '*' in type_str:
                tasks.append(MultiplyTask())
            if tasks:
                break
        self.tasks.extend(tasks)
        # remove duplicate entries
        self.tasks = [*{*self.tasks}]

    def ask(self):
        """Ask questions until interupted."""
        start_time = timer()
        try:
            for task in self._get_task():
                self._process_task(task)
                if (timer() - start_time > self.time_limit):
                    break
        except KeyboardInterrupt:
            print()

        print(
            "Du hast {} von {} Aufgaben richtig gemacht!".format(
                self.n_correct, self.n_asked
            )
        )

    def _process_task(self, task):
        """Create a task and ask until correct."""
        answer = task.ask()
        self.n_asked += 1
        if task.validate(answer):
            print("Richtig! {}".format(
                random.choice(self.correct_emoji))
            )
            self.n_correct += 1
        else:
            print("Leider falsch. 😒")

    def _get_task(self):
        while True:
            yield random.choice(self.tasks)


class Task(object):
    """A single task.

    Privides methods for inquiring input and for validation of the result.
    """

    type = "?"

    @classmethod
    def op(cls, x, y):
        return None

    def __init__(self, limit=None):
        self.limit = limit
        self._numbers = None
        self._ask_details()

    def _ask_details(self):
        """Ask for additional task parameter."""
        pass

    def _get_numbers(self):
        """Create addition task."""
        number1 = random.randint(1, self.limit - 1)
        number2 = random.randint(1, self.limit - number1)
        return number1, number2

    def ask(self):
        """Promt user for result."""
        number1, number2 = self._get_numbers()
        self._numbers = (number1, number2)
        answer = input(
            "{} {} {} = ".format(number1, self.type, number2)
        )
        try:
            answer = int(answer)
        except Exception:
            answer = None
        return answer

    def validate(self, answer=False):
        """Return True if correct result entered, else False."""
        if self._numbers:
            return (answer == self.op(*self._numbers))
        else:
            return False


class MultiplyTask(Task):
    """Task for multiplication."""

    op = operator.mul
    type = "*"

    def _ask_details(self):
        while True:
            numbers = input("Welche Zahlenreihen für die Multiplikation?")
            if numbers.isnumeric():
                break
        self.row_numbers = tuple(map(int, numbers))

    def _get_numbers(self):
        numbers = [
            random.choice(self.row_numbers),
            random.randint(0, 10)
        ]
        random.shuffle(numbers)
        return tuple(numbers)


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

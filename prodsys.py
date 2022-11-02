import tkinter as tk


class Fact:
    _id: str
    desc: str
    atom: bool

    def __init__(self, _id: str, desc: str):
        self._id = _id
        self.desc = desc
        self.atom = False

    def __repr__(self) -> str:
        return self.desc

    @staticmethod
    def parse(data: str) -> 'Fact':
        # print(data)
        _id, desc, _ = map(str.strip, data.split(';'))
        return Fact(_id, desc)


class Rule:
    _id: str
    desc: str
    lhs: set[str]
    rhs: set[str]

    def __init__(self, _id: str, desc: str, lhs: set[str], rhs: set[str]):
        self._id = _id
        self.desc = desc
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        return self.desc

    @staticmethod
    def parse(data: str) -> 'Rule':
        # print(data)
        _id, lhs, rhs, _, desc = map(str.strip, data.split(';'))
        return Rule(_id, desc, set(lhs.split(',')), set((rhs, )))


class App(tk.Tk):
    facts: list[Fact]
    rules: list[Rule]

    def __init__(self):
        super().__init__()
        self.title('Production System')
        self.resizable(False, False)
        self.geometry('500x400')
        self.facts = []
        self.rules = []
        self.load_facts()
        self.load_rules()
        self.create_widgets()
        self.factbox.insert(tk.END, *self.facts)
        self.bind('<Escape>', self.reset)

    def create_widgets(self):
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        self.factbox = tk.Listbox(self.frame1, width=40, height=20, selectmode=tk.MULTIPLE)
        self.scroll1 = tk.Scrollbar(self.frame1, orient=tk.VERTICAL, command=self.factbox.yview)
        self.status = tk.Text(self.frame1, width=40, height=20)
        self.directb = tk.Button(self.frame2, text='Прямой Вывод', command=self.direct)
        self.reverseb = tk.Button(self.frame2, text='Обратный Вывод', command=self.reverse)

        self.frame1.pack(side='top', padx=10, pady=10)
        self.frame2.pack(side='bottom', padx=10, pady=10)
        self.factbox.pack(side='left', fill='both')
        self.scroll1.pack(side='left', fill='y')
        self.status.pack(side='left', fill='both')
        self.directb.pack(side='left', padx=1)
        self.reverseb.pack(side='left', padx=1)

    def load_facts(self, path: str = 'facts.txt'):
        with open(path) as f:
            for line in f:
                if line and not line.startswith('\n'):
                    self.facts.append(Fact.parse(line))

    def load_rules(self, path: str = 'rules.txt'):
        with open(path) as f:
            for line in f:
                if line and not line.startswith('\n'):
                    self.rules.append(Rule.parse(line))

    def reset(self, *_):
        self.status.delete(1.0, tk.END)
        self.factbox.selection_clear(0, tk.END)

    def direct(self):
        pass

    def reverse(self):
        pass

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()

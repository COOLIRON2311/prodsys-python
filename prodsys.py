import tkinter as tk
from enum import Enum
from queue import Queue


class Fact:
    iid: str
    desc: str
    is_atom: bool

    def __init__(self, _id: str, desc: str):
        self.iid = _id
        self.desc = desc
        self.is_atom = False

    def __repr__(self) -> str:
        return self.desc

    @staticmethod
    def parse(data: str) -> 'Fact':
        # print(data)
        try:
            _id, desc, _ = map(str.strip, data.split(';'))
            return Fact(_id, desc)
        except ValueError as e:
            raise ValueError(f'Invalid fact: {data}') from e

    def __hash__(self) -> int:
        return hash(self.desc)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Fact):
            return self.desc == o.desc
        return False


class Rule:
    iid: str
    desc: str
    lhs: set[str]
    rhs: set[str]

    def __init__(self, _id: str, desc: str, lhs: set[str], rhs: set[str]):
        self.iid = _id
        self.desc = desc
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        return self.desc

    @staticmethod
    def parse(data: str) -> 'Rule':
        # print(data)
        try:
            _id, lhs, rhs, _, desc = map(str.strip, data.split(';'))
            lhs = set(map(str.strip, lhs.split(',')))
            rhs = set(map(str.strip, rhs.split(',')))
            return Rule(_id, desc, lhs, rhs)
        except ValueError as e:
            raise ValueError(f'Invalid rule: {data}') from e

    def __hash__(self) -> int:
        return hash(self.desc)

    @property
    def reverse_desc(self):
        return ' -> '.join(self.desc.split(' -> ')[::-1])


class Type(Enum):
    And = 0
    Or = 1


class Node:
    type: Type
    fact: Fact
    rule: Rule
    parent: 'Node'
    children: list['Node']
    path: list['Node']
    leads_to_loop: bool
    satisfied: bool

    def __init__(self, fact, parent=None):
        self.type = Type.And
        self.fact = fact
        self.rule = None
        self.parent = parent
        self.children = []
        self.path = []
        self.leads_to_loop = False
        self.satisfied = False

    def print(self, indent=0):
        print(' ' * indent + '|_', self.type, self.fact, self.satisfied)
        for child in self.children:
            child.print(indent + 4)

    @property
    def is_leaf(self):
        return len(self.children) == 0


class App(tk.Tk):
    facts: list[Fact]
    rules: list[Rule]
    _inv: list[Fact]
    _tar: list[Fact]

    def __init__(self):
        super().__init__()
        self.title('Production System')
        self.minsize(1000, 400)
        self.geometry('1000x400')
        self.facts = []
        self.rules = []
        self._inv = []
        self._tar = []
        self.load_facts()
        self.load_rules()
        self.set_atoms()
        self.fill_inv_tar()
        self.create_widgets()
        self.inventory.insert(tk.END, *self._inv)
        self.targets.insert(tk.END, *self._tar)
        self.reset()
        self.bind('<Escape>', self.reset)
        self.bind('<Control-a>', self.select_all)
        self.state('zoomed')

    def create_widgets(self):
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        self.inventory = tk.Listbox(self.frame1, width=40, height=20, selectmode=tk.MULTIPLE, exportselection=False)
        self.targets = tk.Listbox(self.frame1, width=40, height=20, selectmode=tk.SINGLE, exportselection=False)
        self.scroll1 = tk.Scrollbar(self.frame1, orient=tk.VERTICAL, command=self.inventory.yview)
        self.scroll2 = tk.Scrollbar(self.frame1, orient=tk.VERTICAL, command=self.targets.yview)
        self.status = tk.Text(self.frame1, width=40, height=20, state=tk.DISABLED)
        self.label1 = tk.Label(self.frame1, text='Инвентарь\n->')
        self.label2 = tk.Label(self.frame1, text='Сделать\n->')
        self.directb = tk.Button(self.frame2, text='Прямой Вывод', command=self.direct)
        self.reverseb = tk.Button(self.frame2, text='Обратный Вывод', command=self.reverse)

        self.frame1.pack(side='top', padx=10, pady=10, fill='both', expand=True)
        self.frame2.pack(side='bottom', padx=10, pady=10)
        self.label1.pack(side='left')
        self.inventory.pack(side='left', fill='both')
        self.scroll1.pack(side='left', fill='y')
        self.label2.pack(side='left')
        self.targets.pack(side='left', fill='both')
        self.scroll2.pack(side='left', fill='y')
        self.status.pack(side='left', fill='both', expand=True)
        self.directb.pack(side='left', padx=1)
        self.reverseb.pack(side='left', padx=1)
        self.inventory.config(yscrollcommand=self.scroll1.set)
        self.targets.config(yscrollcommand=self.scroll2.set)

    def load_facts(self, path: str = 'facts.txt'):
        with open(path, encoding='utf8') as f:
            for line in f:
                if line and not line.startswith('\n'):
                    self.facts.append(Fact.parse(line))
        self.facts.sort(key=str)

    def load_rules(self, path: str = 'rules.txt'):
        with open(path, encoding='utf8') as f:
            for line in f:
                if line and not line.startswith('\n'):
                    self.rules.append(Rule.parse(line))

    def set_atoms(self):
        for fact in self.facts:
            if not any(fact.iid in rule.rhs for rule in self.rules):
                fact.is_atom = True
                # print(fact)

    def fill_inv_tar(self):
        for fact in self.facts:
            if fact.is_atom:
                self._inv.append(fact)
            else:
                self._tar.append(fact)

    def _open_status(self):
        self.status.configure(state=tk.NORMAL)

    def _close_status(self):
        self.status.configure(state=tk.DISABLED)

    def _clear_status(self):
        self._open_status()
        self.status.delete(1.0, tk.END)
        self._close_status()

    def reset(self, *_):
        self._open_status()
        self.status.delete(1.0, tk.END)
        self.status.insert(tk.END, 'Выберите факты и нажмите кнопку')
        self._close_status()
        self.targets.selection_clear(0, tk.END)
        self.inventory.selection_clear(0, tk.END)

    def direct(self):
        facts = {self._inv[i].iid for i in self.inventory.curselection()}
        target = self._tar[self.targets.curselection()[0]].iid
        prev_step = facts.copy()
        cur_step = facts.copy()
        self._clear_status()
        self._open_status()

        while True:
            for rule in self.rules:
                if rule.lhs.issubset(prev_step) and not rule.rhs.issubset(cur_step):
                    cur_step.update(rule.rhs)
                    self.status.insert(tk.END, f'{rule}\n')
                    if target in cur_step:
                        self.status.insert(tk.END, self.pad_str('Item crafted'))
                        self._close_status()
                        return
            if cur_step == prev_step:
                break
            prev_step = cur_step.copy()
        if target not in cur_step:
            self._clear_status()
            self.status.insert(tk.END, self.pad_str('Item can\'t be crafted'))
        self._close_status()

    def reverse(self):
        # pylint: disable=consider-using-enumerate
        facts = {self._inv[i] for i in self.inventory.curselection()}
        # print(facts)
        target = self._tar[self.targets.curselection()[0]]
        all_facts = {fact.iid: fact for fact in self.facts}

        root = Node(target)
        q1: Queue[Node] = Queue()
        q1.put(root)

        while not q1.empty():
            node = q1.get()

            if node.leads_to_loop:
                continue

            if node.fact in facts or node.fact.is_atom:
                continue

            new_facts = []
            new_rules = []

            for rule in self.rules:
                if node.fact.iid in rule.rhs:
                    new_facts.append(rule.lhs)
                    new_rules.append(rule)

            if len(new_facts) == 1:  # And
                for fact in new_facts[0]:
                    n = Node(all_facts[fact], node)
                    if new_rules[0] in node.path:
                        n.leads_to_loop = True
                    n.path = node.path + [new_rules[0]]
                    n.rule = new_rules[0]
                    node.children.append(n)
                    q1.put(n)
            else:  # Or
                for i in range(len(new_facts)):
                    node.type = Type.Or
                    a = Node(node.fact, node)
                    a.path = node.path
                    node.children.append(a)
                    for fact in new_facts[i]:
                        n = Node(all_facts[fact], a)
                        if new_rules[i] in a.path:
                            n.leads_to_loop = True
                        n.path = a.path + [new_rules[i]]
                        n.rule = new_rules[i]
                        a.children.append(n)
                        q1.put(n)

        trace = []
        def _eval(root: Node):
            if root.is_leaf:
                if root.fact in facts:
                    root.satisfied = True
                    if root.rule and root.rule not in trace:
                        trace.append(root.rule)
                    return True
                return False
            else:
                match root.type:
                    case Type.And:
                        if all(_eval(child) for child in root.children):
                            root.satisfied = True
                            if root.rule and root.rule not in trace:
                                trace.append(root.rule)
                            return True
                        return False

                    case Type.Or:
                        if any(_eval(child) for child in root.children):
                            root.satisfied = True
                            if root.rule and root.rule not in trace:
                                trace.append(root.rule)
                            return True
                        return False

                    case _:
                        raise ValueError('Unknown node type')
        _eval(root)
        root.print()
        self._clear_status()
        self._open_status()
        if root.satisfied:
            for rule in trace:
                self.status.insert(tk.END, f'{rule}\n')
            self.status.insert(tk.END, self.pad_str('Item crafted'))
        else:
            self.status.insert(tk.END, self.pad_str('Item can\'t be crafted'))
        self._close_status()

    def pad_str(self, s: str) -> str:
        ln = len(s)
        return f"{'-' * ln}\n{s}\n{'-' * ln}"

    def select_all(self, _):
        self.inventory.select_set(0, tk.END)

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()

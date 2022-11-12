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

facts: list[Fact] = []
rules: list[Rule] = []

with open('facts.txt') as f:
    for line in f:
        if line and not line.startswith('\n'):
            facts.append(Fact.parse(line))
        # facts.append(Fact.parse(line))

with open('rules.txt') as f:
    for line in f:
        if line and not line.startswith('\n'):
            rules.append(Rule.parse(line))

fact_idx = 1
facts_db: dict[str, str] = {}

for fact in facts:
    fact.iid = f'f{fact_idx}'
    facts_db[fact.desc] = fact.iid
    fact_idx += 1

rule_idx = 1
for rule in rules:
    rule.iid = f'r{rule_idx}'
    rule_idx += 1

with open('facts2.txt', 'w') as f:
    for fact in facts:
        f.write(f'{fact.iid}; {fact.desc};\n')

with open('rules2.txt', 'w') as f:
    for rule in rules:
        t = rule.desc.split(' -> ')
        facts = map(str.strip, t[0].split(','))
        try:
            lhs = ', '.join(facts_db[desc] for desc in facts)
        except KeyError as e:
            raise ValueError(f'Invalid rule: {rule}') from e
        fact = str.strip(t[1])
        rhs = facts_db[fact]
        f.write(f'{rule.iid}; {lhs}; {rhs}; 1; {rule.desc}\n')
# https://www.minecraft-crafting.net

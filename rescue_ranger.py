from prodsys import Rule, Fact

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

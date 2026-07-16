from dataclasses import dataclass, field

@dataclass
class Field:
    id: int
    name: str
    type: str
    pk: bool
    not_null: bool
    unique: bool
    increment: bool
    default: str

@dataclass
class Table:
    id: int
    name: str
    fields: list


@dataclass
class Relationship:
    id: int
    cardinality: str
    start_table: int
    start_field: int
    end_table: int
    end_field: int


@dataclass
class Diagram:
    title: str
    tables: list = field(default_factory=list)
    relationships: list = field(default_factory=list)


def parse_diagram(doc, who='diagram'):
    tables = []
    for ti, t in enumerate(doc['tables']):
        fields = []
        for fi, f in enumerate(t['fields']):
            fields.append(Field(
                id=f['id'],
                name=str(f.get('name', '')),
                type=f['type'].strip().upper(),
                pk=bool(f.get('pk')),
                not_null=bool(f.get('notNull')),
                unique=bool(f.get('unique')),
                increment=bool(f.get('increment')),
                default=str(f.get('def', '')),
            ))
        tables.append(Table(id=t['id'], name=str(t.get('name', '')), fields=fields))

    relationships = []
    for ri, r in enumerate(doc['relationships']):
        card = r.get('cardinality', 'many_to_one')
        
        if card == 'one_to_many':
            card = 'many_to_one'
            r = {**r, 'startTable': r['endTable'], 'startField': r['endField'],
                 'endTable': r['startTable'], 'endField': r['startField']}
        relationships.append(Relationship(
            id=r.get('id', ri),
            cardinality=card,
            start_table=r['startTable'],
            start_field=r['startField'],
            end_table=r['endTable'],
            end_field=r['endField'],
        ))
    return Diagram(title=str(doc.get('title', '')), tables=tables, relationships=relationships)
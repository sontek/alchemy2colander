from sqlalchemy.orm             import class_mapper
from sqlalchemy.orm.properties  import RelationshipProperty

import colander
import sqlalchemy

#def expand(obj, relation, seen):
#    """ Return the to_json or id of a sqlalchemy relationship. """
#
#    if hasattr(relation, 'all'):
#        relation = relation.all()
#
#    if hasattr(relation, '__iter__'):
#        return [expand(obj, item, seen) for item in relation]
#
#    if type(relation) not in seen:
#        return to_schema(relation, seen + [type(obj)])
#    else:
#        return relation.id
#
#
def to_schema(cls, seen=None):
    """ Returns a colander schema representation of the object.

    Recursively evaluates to_schema(...) on its relationships.
    """
    if not seen:
        seen = []

    properties = list(class_mapper(cls).iterate_properties)

    relationships = [
        p.key for p in properties if type(p) is RelationshipProperty
    ]

    attrs = {}

    for prop in properties:
        if not prop in relationships:
            attrs[prop.key] = prop

    schema = colander.SchemaNode(colander.Mapping())

    for attr, column_property in attrs.iteritems():
        node = None
        column = column_property.columns[0]

        missing_val = colander.null if column.nullable else colander.required

        column_type = column.type

        string_types = (
            sqlalchemy.Unicode
            , sqlalchemy.UnicodeText
            , sqlalchemy.String
        )

        int_types = (
            sqlalchemy.Integer
            , sqlalchemy.SmallInteger
            , sqlalchemy.BigInteger
        )

        if isinstance(column_type, string_types):
            validator = None

            if column.type.length:
                validator = colander.Length(max=column.type.length)

            node = colander.SchemaNode(
                colander.String()
            )

            if validator:
                node.validator = validator

        elif isinstance(column_type, int_types):
            node = colander.SchemaNode(
                colander.Integer()
            )
        elif isinstance(column_type, sqlalchemy.Boolean):
            node = colander.SchemaNode(
                colander.Boolean()
            )


        node.name = attr
        node.missing = missing_val
        schema.add(node)

#    d = dict([(attr, getattr(obj, attr)) for attr in attrs])

    #TODO: Support relationships
#    for attr in relationships:
#        d[attr] = expand(obj, getattr(obj, attr), seen)
#
    return schema

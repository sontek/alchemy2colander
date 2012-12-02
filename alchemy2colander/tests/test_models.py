from alchemy2colander               import to_schema
from alchemy2colander.tests         import BaseTestCase
from sqlalchemy.ext.declarative     import declarative_base
from sqlalchemy.types               import Integer
from sqlalchemy.types               import UnicodeText
from sqlalchemy.types               import Unicode
from sqlalchemy.types               import Boolean
from sqlalchemy                     import Column

import colander

Base = declarative_base()

class Conference(Base):
    __tablename__ = 'conferences'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10), nullable=False)
    description = Column(UnicodeText)
    is_active = Column(Boolean, default=False, nullable=False)

class TestModels(BaseTestCase):
    def test_bad_model(self):
        schema = to_schema(Conference)

        had_exception = False

        try:
            schema.deserialize({})
        except colander.Invalid, e:
            errors = e.asdict()
            had_exception = True
            assert errors['id'] == 'Required'
            assert errors['name'] == 'Required'
            assert errors['is_active'] == 'Required'
            assert not 'description' in errors

        assert had_exception == True

    def test_good_model(self):
        schema = to_schema(Conference)
        schema.deserialize({
            'id': 1
            , 'name': 'Conf 1'
            , 'description': 'foo'
            , 'is_active': True
        })

    def test_badg_length(self):
        schema = to_schema(Conference)
        had_exception = False
        try:
            schema.deserialize({
                'id': 1
                , 'name': '12345678910111213'
                , 'description': 'foo'
                , 'is_active': True
            })
        except colander.Invalid, e:
            had_exception = True
            errors = e.asdict()
            assert errors['name'] == 'Longer than maximum length 10'

        assert had_exception == True

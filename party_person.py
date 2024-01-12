from trytond.model import fields
from trytond.pool import PoolMeta,Pool
from trytond.pyson import Not,Bool,Eval,If

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from ..party.party import IDENTIFIER_TYPES

# IDENTIFIER_TYPES.append(('passport','Passport'))


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    
    lastname = fields.Char(
        'Lastname',strip=True,
        states={
            'invisible': Not(Bool(Eval('is_person')))
        },
        help="Family or last names")
    is_person = fields.Boolean(
        'Person',
        help="Choose if is a person")
    dob = fields.Date(
        'Date of Birth',
        help="Fill the day of birth")
    age = fields.Function(fields.Char('Age'),'on_change_with_dob')
    gender = fields.Selection([
        (None, ''),
        ('m', 'Male'),
        ('f', 'Female'),
        ('other', 'Other')
        ],
        'Gender',
        states={
            'required': Bool(Eval('is_person'))})
    marital_status = fields.Selection([
        (None, ''),
        ('s', 'Single'),
        ('m', 'Married'),
        ('c', 'Concubinage'),
        ('w', 'Widowed'),
        ('d', 'Divorced'),
        ('x', 'Separated'),
        ], 'Marital Status',
        sort=False)

    @fields.depends('dob')
    def on_change_with_age(self):
        if self.dob:
            start = dt.strptime(str(self.dob), '%Y-%m-%d')
            end = dt.strptime(str(dt.today().date()), '%Y-%m-%d')
            age = relativedelta(end,start)
            
            return f'{age.years} Años, {age.months} Meses y {age.days} Dias'


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    citizenship = fields.Many2One('country.country', "Citizenship")
     
    @classmethod
    def __setup__(cls):
        super(Address, cls).__setup__()
        # Override definition to change street field from Text to Char and
        # required.
        cls.street = fields.Char(cls.street.string, help=cls.street.help)

class Configuration(metaclass=PoolMeta):
    __name__ = 'party.configuration'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.identifier_types.selection.append(('passport', 'Passport'))
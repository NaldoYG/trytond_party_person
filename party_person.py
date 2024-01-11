from trytond.model import fields
from trytond.pool import PoolMeta,Pool
from trytond.pyson import Not,Bool,Eval,If

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
    age = fields.Function()
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

class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    citizenship = fields.Many2One('country.country', "Citizenship")
     
    @classmethod
    def __setup__(cls):
        super(Address, cls).__setup__()
        # Override definition to change street field from Text to Char and
        # required.
        cls.street = fields.Char(cls.street.string, help=cls.street.help)

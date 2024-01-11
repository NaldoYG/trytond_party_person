# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import party_person

__all__ = ['register']


def register():
    Pool.register(
        party_person.Party,
        party_person.Address,
        module='party_person', type_='model')
    Pool.register(
        module='party_person', type_='wizard')
    Pool.register(
        module='party_person', type_='report')

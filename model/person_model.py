from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Any, Dict


class PersonError(Exception):
    ...


@dataclass(frozen=True)
class Person:
    name: str
    email: str
    birthdate: date

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise PersonError(f'Person attribute `name` must be of type {str}.')

        if not len(self.name):
            raise PersonError('Person name must be not an empty string.')

        if not isinstance(self.email, str):
            raise PersonError(f'Person attribute `email` must be of type {str}.')

        if not len(self.email):
            raise PersonError('Person email must be not an empty string.')

        if not isinstance(self.birthdate, date):
            raise PersonError(f'Person attribute `dob` must be of type {date}.')

        self.__validate_birthdate(self.birthdate)

    @classmethod
    def from_dict(cls, mapping: Dict[str, Any]) -> Person:
        if not mapping:
            raise PersonError('Suppose to get a person definition, but got big black nothing. Giving up...')

        try:
            name, email, birthdate = mapping['name'], mapping['email'], mapping['birthdate']
        except KeyError as ex:
            raise PersonError(f'{str(ex)} is a mandatory Person attribute.')

        if isinstance(birthdate, str):
            birthdate = cls.__string_to_date(birthdate)

            return cls(name, email, birthdate)

    @staticmethod
    def __string_to_date(birthdate: str) -> date:
        try:
            return datetime.strptime(birthdate, '%Y-%m-%d').date()
        except ValueError:
            try:
                return datetime.strptime(birthdate, '%m-%d').date()
            except ValueError:
                raise PersonError('Invalid birthdate format. Valid formats (YYYY-MM-DD or MM-DD).')

    @staticmethod
    def __validate_birthdate(birthdate: date) -> None:
        current_date = datetime.now().date()

        if birthdate > current_date:
            raise PersonError('Birthdate cannot be in the future.')

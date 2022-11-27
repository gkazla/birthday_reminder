from __future__ import annotations

import json
from datetime import datetime, timedelta, date
from typing import Any, Dict, List, Optional

from model.person_model import Person, PersonError
from util.bg_colors import BgColors


class CommunityError(Exception):
    def __init__(self, *, message: Optional[str] = None, reason: Optional[str] = None) -> None:
        if message is None:
            message = 'Unexpected error while parsing JSON file.'

        if reason:
            message += f' Reason: {reason}.'

        super().__init__(message)


class Community:
    def __init__(self, members: List[Person]) -> None:
        self.__members = members

    @property
    def members(self) -> List[Person]:
        return self.__members

    def upcoming_birthday_heroes(self, days: int) -> List[Person]:
        birthday_date = self.birthdate(days)

        birthday_heroes = []
        for member in self.__members:
            if member.birthdate.month == birthday_date.month and member.birthdate.day == birthday_date.day:
                birthday_heroes.append(member)

        return birthday_heroes

    @classmethod
    def from_json(cls, file_path: str) -> Community:
        data = cls.__read_json_data(file_path)

        members = []
        for item in data:
            try:
                members.append(Person.from_dict(item))
            except PersonError as ex:
                raise CommunityError(reason=repr(ex))

        return cls(members=members)

    @classmethod
    def valid_json(cls, file_path, silent: bool = False) -> bool:

        def __log(message: str) -> None:
            if not silent:
                print(message)

        try:
            data = cls.__read_json_data(file_path)
            if not data:
                raise CommunityError(message=f'{BgColors.WARNING}Empty JSON file. Seriously?{BgColors.ENDC}')

            if isinstance(data, dict):
                raise CommunityError(
                    message=f'{BgColors.WARNING}Single person in file! That\'s not a community!{BgColors.ENDC}'
                )
        except CommunityError as ex:
            __log(f'{BgColors.WARNING}{str(ex)}{BgColors.ENDC}')

            return False
        else:
            total = len(data)
            failed = 0
            for item in data:
                try:
                    person = Person.from_dict(item)
                except PersonError as ex:
                    __log(
                        f'{BgColors.FAIL}[ERROR]{BgColors.ENDC} {item} '
                        f'validation error: {BgColors.WARNING}{ex}{BgColors.ENDC}'
                    )
                    failed += 1
                    continue

                __log(
                    f'{BgColors.OKGREEN}[INFO]{BgColors.ENDC} {person.name} '
                    f'validation {BgColors.OKGREEN}PASSED{BgColors.ENDC}'
                )

            __log(
                f'\nCommunity of {total} members:\n'
                f'\tValidation passed: {BgColors.OKGREEN}{total - failed}{BgColors.ENDC}\n'
                f'\tValidation failed: {BgColors.FAIL}{failed}{BgColors.ENDC}\n'
            )

            return failed == 0

    @staticmethod
    def __read_json_data(file_path) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r') as json_file:
                data = json_file.read()
        except FileNotFoundError as ex:
            raise CommunityError(reason=str(ex))
        except UnicodeDecodeError:
            raise CommunityError(message='Working with text files only!')

        try:
            return json.loads(data)
        except json.JSONDecodeError as ex:
            raise CommunityError(reason=str(ex))

    @staticmethod
    def birthdate(days: int) -> date:
        return datetime.now().date() + timedelta(days=days)

import os
from datetime import date
from typing import List, Union

from community.community import Community
from community.community_cli import community_cli
from community.community_post import CommunityPost
from community.community_template import CommunityTemplate
from model.person_model import Person

EMAIL_TEMPLATE = CommunityTemplate('./templates')
COMMUNITY_POST = CommunityPost()
FROM_ADDRESS = os.getenv('FROM_ADDRESS', 'noreply@coolcommunity.com')


def send_birthday_reminder(recipients: List[Person], heroes: Union[Person, List[Person]], birthdate: date) -> None:
    names = ', '.join([member.name for member in recipients])
    heroes_names = ', '.join([member.name for member in heroes]) if isinstance(heroes, list) else heroes.name
    email_body = EMAIL_TEMPLATE.render(
        template_file_name='email_template.j2',
        names=names,
        birthday_heroes_names=heroes_names,
        birthdate=birthdate,
        days_left=cli_arguments.days
    )

    subject = f'Birthday Reminder: {heroes_names} birthday on {birthdate}'

    COMMUNITY_POST.email(
        from_address=FROM_ADDRESS,
        to_address=[member.email for member in recipients],
        subject=subject,
        email_body=email_body
    ).send()


if __name__ == '__main__':
    cli_arguments = community_cli()

    if cli_arguments.validate:
        Community.valid_json(cli_arguments.file)

    if cli_arguments.email:
        if not Community.valid_json(cli_arguments.file, silent=True):
            Community.valid_json(cli_arguments.file)
        else:
            community = Community.from_json(cli_arguments.file)
            upcoming_birthdate = Community.birthdate(cli_arguments.days)

            birthday_heroes = community.upcoming_birthday_heroes(days=cli_arguments.days)
            other_members = list(set(community.members).difference(set(birthday_heroes)))

            if birthday_heroes:
                send_birthday_reminder(recipients=other_members, heroes=birthday_heroes, birthdate=upcoming_birthdate)

            if birthday_heroes and len(birthday_heroes) > 1:
                for hero in birthday_heroes:
                    other_members = list(set(birthday_heroes).difference({hero}))
                    send_birthday_reminder(recipients=other_members, heroes=hero, birthdate=upcoming_birthdate)

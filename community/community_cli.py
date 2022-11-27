import argparse
import logging

from util.bg_colors import BgColors


logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def community_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Community mailer CLI for sending birthday remainders to a community members.'
    )
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        required=True,
        help='Path to JSON file holding community members definition list.'
    )
    parser.add_argument(
        '-d',
        '--days',
        type=int,
        default=7,
        help=(
            'Provide amount of days before to send notification email about community member birthday. '
            'Default: 7.'
        )
    )
    parser.add_argument(
        '-v',
        '--validate',
        action='store_true',
        help='Validate given community members definition file and output validation log.'
    )
    parser.add_argument(
        '-e',
        '--email',
        action='store_true',
        help='Send birthday reminder emails to a community members.'
    )
    args = parser.parse_args()

    if not args.validate and not args.email:
        logger.warning(
            f'{BgColors.WARNING}Missing command flags. Either {BgColors.OKGREEN}-v{BgColors.WARNING} '
            f'or {BgColors.OKGREEN}-e{BgColors.WARNING} or both must be provided.{BgColors.ENDC}'
        )

    return args

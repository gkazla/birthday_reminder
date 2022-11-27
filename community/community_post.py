from __future__ import annotations

import os
import smtplib
import socket
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Union

from util.retriable_decorator import retriable


class CommunityPostError(Exception):
    ...


class CommunityPost:
    def __init__(self) -> None:
        self.__smtp_host = os.getenv('SMTP_HOST')
        self.__smtp_port = os.getenv('SMTP_PORT', 1025)

        if use_tls := os.getenv('SMTP_USE_TLS'):
            self.__smtp_use_tls = use_tls.lower() == 'true'
        else:
            self.__smtp_use_tls = False

        self.__smtp_user = os.getenv('SMTP_USER')
        self.__smtp_password = os.getenv('SMTP_PASSWORD')
        self.__context = ssl.create_default_context() if self.__smtp_use_tls else None
        self.__message = None
        self.__from_address = None
        self.__to_address = None

    @retriable(retries=3, rest_between=1, fail_on_error=False)
    def send(self) -> None:
        if not self.__from_address or not self.__to_address or not self.__message:
            raise RuntimeWarning(f'CommunityPost instance method `send` must be in chain with `email` method.')

        try:
            with smtplib.SMTP(self.__smtp_host or 'localhost', self.__smtp_port) as smtp_server:
                if self.__smtp_use_tls and self.__context:
                    smtp_server.starttls(context=self.__context)

                if self.__smtp_host:
                    smtp_server.login(self.__smtp_user, self.__smtp_password)

                smtp_server.sendmail(
                    from_addr=self.__from_address,
                    to_addrs=self.__to_address,
                    msg=self.__message.as_string()
                )
        except (smtplib.SMTPException, socket.error) as ex:
            raise CommunityPostError(f'Unexpected error while sending an email. Reason: {repr(ex)}')

    def email(self, from_address: str, to_address: Union[str, List[str]], subject: str, email_body: str) -> CommunityPost:
        self.__from_address = from_address
        self.__to_address = to_address

        self.__message = MIMEMultipart()
        self.__message['From'] = from_address
        self.__message['Bcc'] = ', '.join(to_address) if isinstance(to_address, list) else to_address
        self.__message['Subject'] = subject

        email_body = MIMEText(email_body, 'html')
        self.__message.attach(email_body)

        return self

## Birthday Reminder

Birthday Reminder is command-line interface (CLI) based tool helping to send birthday reminder emails.

Tool reads given JSON file and sends reminder email about upcoming birthdays.

There are two commands available:
* validate - validates given JSON file and outputs the report.
* email - sends birthday email reminders.

JSON example:
```json
[
  {
    "name": "Peter Benitez",
    "email": "peter.benitez@example.com",
    "birthdate": "1990-12-12"
  },
  {
    "name": "Steven Smith",
    "email": "steven.smith@example.com",
    "birthdate": "1980-09-11"
  }
]
```

### Install dependencies

```shell
pip install .
```

### Environment
Birthday Reminder tool is using environment variables listed here.

```
FROM_ADDRESS - email address that is going to send reminder emails;
SMTP_HOST - address of SMTP server for sending of an emails;
SMTP_PORT - SMTP server port;
SMTP_USE_TLS - True/False - use transport layer security protocol;
SMTP_USER - username for the authenitcation to the SMTP server;
SMTP_PASSWORD - password for the authentication to the SMTP server.
```

### Usage

Validate JSON:
```shell
python birthday_reminder.py -v -f community_members.json 
```

Send birthday reminder emails:
```shell
python birthday_reminder.py -e -d 7 -f community_members.json
```
`-d` flag can be omitted, the tool will use default value that is set to 7 days.

To get help:
```shell
python birthday_reminder.py -h
```

### Contribution
Contributions of any kind are gladly welcome. 
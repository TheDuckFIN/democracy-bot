# Democracy bot for Discord

## Requirements

- Python (`^3.7`)
- Poetry (https://github.com/sdispater/poetry)

## Getting started

Install using poetry:

TODO: change `settings.virtualenvs.in-project` to be a local, project-specific setting when upgrading to Poetry 1.0. (see [this PR]([https://link](https://github.com/sdispater/poetry/pull/1272)))

```sh
$ poetry config settings.virtualenvs.in-project true
$ poetry install
```

Run application:

```sh
$ ./run.sh
```

## Environment variables

Bot is configured using environment variables. You can specify them manually, or create a file named `.env` in the project root and specify required values there. If the file is present, `run.sh` script will read the variables to your environment automatically.

Available environment variables:

| Variable  | Required | Description                                                     |
| --------- | -------- | --------------------------------------------------------------- |
| BOT_TOKEN | x        | Bot token from Discord developer portal (**NOT** client secret) |

## Linting

Lint the code using pylint and black:

```sh
$ ./lint.sh
```

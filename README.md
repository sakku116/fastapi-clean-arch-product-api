# Fastapi Clean Architecture Implementation

## How To Run
- Create virtual environment
    ```
    virtualenv venv
    ```
    > Make sure the `virtualenv` package already installed. Or you install it via `pip install virtualenv` command.

- Activate the `virtualenv`
    ```
    # linux / mac
    source venv/bin/activate

    # windows
    source venv/scripts/activate
    ```
- Install all required packages in `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
- Create `.env` file and set the env variables. See `/config/env.py` for the variable list.
- Run the `main.py` script.
    ```
    python main.py
    ```
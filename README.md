# Telegram Multi Accounts

This program forward message from many your minor Telegram accounts to the one main your Telegram. 
Also you can respond on message in main account and minor account has send message to client like like own 

## Telegram Api key
To get api key you need visit https://my.telegram.org/ <br>


----

## Setup program
1. Create directory `data` (_directory for storage sessions_)
2. Install requirements `pip install -r requirements.txt`
3. Write in the `config.py` in **apis_telegram** array with your minor account dictionary data like this
    ```python
    apis_telegram = [
        {
            "user": "Manager_1",
            "phone": "380931235678",
            "api_id": 87654321,
            "api_hash": 'telegram_api_hash',
        },
        {
            "user": "Manager_1",
            "phone": "380989875432",
            "api_id": 12345678,
            "api_hash": 'telegram_api_hash',
        }
    ]
    ```
4. Write in the `config.py` in **master_account** username or phone number of your master account:
   ```python
   master_account = 'director'
   # or 
   master_account = '380912345678'
   ```
----

## Run program
To run use command `python -d tg_mngr`

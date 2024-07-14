# url-shortener-app
## Setup The Virtual ENV
### Installing Virtual ENV
Install the venv first.
```sh
python3 -m venv .venv
```
Then enter the virtual env
```sh
source .venv/bin/activate
```

### Installing The Requirements
This app need some dependencies, install it using pip
```sh
# Make sure on directory where requirements.txt exist
pip install -r requirements.txt
```

## Setup The Database
### Create Specific User for The App
In best practice it is good to have specific user for each app, for url-shortener-app run this command to create the database and the user.
```sql
CREATE DATABASE url_shortener;
CREATE USER 'url_shortener_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON url_shortener.* TO 'url_shortener_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## SQL Tips
* #### Check the user list (login as root)
    ```sql
    SELECT User, Host FROM mysql.user;
    ```
* #### Drop the user
    ```sql
    DROP USER 'url_shortener_user'@'localhost';
    ```
* #### Show privileges on users
    ```sql
    SHOW GRANTS FOR 'url_shortener_user'@'localhost';
    ```
* #### Revoke the user privileges
    ```sql
    REVOKE ALL PRIVILEGES ON url_shortener.* FROM 'url_shortener_user'@'localhost';
    ```
## Run and Try The url-shortner-app
### Run The App
To run the app, make sure on project root directory and run command
```sh
# This will run on localhost port 5001 as initialize on run.py
python run.py
```
### Try The url-shortner-app
To try the shortener we can use postman or curl.  
* #### Postman
    Method `POST` with endpoint `http://localhost:5001/shorten`  
    **Body :**
    ```json
    {
        "url": "https://www.youtube.com/watch?v=e2Hibiot5mc",
        "length": 6,
        "days_valid": 7
    }
    ```
    The app should return output
    ```json
    {
        "shortened_url": "http://localhost:5001/nVy4GU"
    }
    ```
* #### CUrl
    Using CUrl can use this script
    ```bash
    curl --location 'http://localhost:5001/shorten' \
    --header 'Content-Type: application/json' \
    --data '{
        "url": "https://www.youtube.com/watch?v=e2Hibiot5mc",
        "length": 6,
        "days_valid": 7
    }'
    ```
    The app should return output
    ```json
    {
        "shortened_url": "http://localhost:5001/nVy4GU"
    }
    ```

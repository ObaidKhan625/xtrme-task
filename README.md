# xtrme-task

User can login to the admin UI and create Records. Mail will be sent to the email provided in the record and will have the temperature of the given city and emoji 
corresponding to the weather. Both emoji and weather are taken from the OpenWeather API. I used requests library to call the API. There is no UI, I have used signals to send
a mail to the user as soon as a record is created.

To run the project, create a virtualenv, activate it than, 
```
pip install -r requirements.txt
```

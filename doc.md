# Spam email reducer 

To remove spam in emails

service will create temporary emails, for each user. user will use that temporary email to create accounts/form filling.


once user thinks that is spam/notrelevent to related. he can disable temporary email



Capabilities:
* should create a temporary email
* should disable a temporary email
* should enable a temporary email
* should list temporaray email
* once email reaches, and temporary email is enabled, it should forward it to original email


## Technologies
- #java
- #socketlabs
- #spring #micronaut
- #sqlite3


### algorithm
1. socket labs provide inbound and outbound to emails
1. sockets should post emails data to your server
1. once recieved, you should check if it is enabled or disabled
    - enabled:
        - you should forward it to your original email
    - disabled:
        - you should discard it
1. once user thinks a email is spamming, user will discard it.

### apis
- `/create?email=user@gmail.com` ---> create email
- `/disable?temp_email=temp@gmail.com` ---> disable email
- `/enable?temp_email=temp@gmail.com` ---> enable email
- `/list?email=user@gmail.com` --> list email
- `/inbound` ---> 
    - socket labs will post here, you should figure out email from temp email
    - once email is gathered, if it is enabled, forward

### database
#### sqlite3
As this is a very small project used for user basis, we don't need low latency or high throughput. we will be using it for temporary and will use postgres/mysql/mariadb if needed expansion.

#### models

###### User table
- user 
- email
- uid
###### Filter table
- original email
- generated email
- enabled/disabled

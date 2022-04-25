# NBUStatService
Aiohttp service to achieve multiple currency data from different dates.


Features:
Created service for achieving data for multiple dates from NBU API:

https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date=20210123

Used aiohttp as main technology. The format of interaction with the service is JSON (REST API).
Input get requests should be in next structure.

GET /exchange?from=yyyy-mm-dd&to=yyyy-mm-dd
where from and to is dates range for which we need to return currency data.

Service authorization is made by tokens, which is sent by header "Authentication" 
list of which is located at config.json.

-----------------------------------------------------------------------------------------------
Were relised Unit tests for next points:

Unauthorised user request.
Unavailable bank.gov.ua domain.
Format of get parameters is unreadable or incorrect.

-----------------------------------------------------------------------------------------------
How to use.

To start service use server.py it will run on local.

To test service use test.py to send one request 
or use test_exchange.py at tests as unit tests.

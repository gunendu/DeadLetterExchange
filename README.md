Framework Used :- Django
Messaging Service :- RabbitMq
Code Repo :- https://github.com/gunendu/DeadLetterExchange
App Deployed :- https://git.heroku.com/ddlx.git

Steps to run the app and verify :-

1) heroku local web (start django server on 5000)

2) curl -H "Content-Type: application/json" -X POST -d '{"message":"hello","callback_url":"http://localhost:5000/queue/callback_service/"}' http://localhost:5000/queue/producer/

3) python consumer.py (starts consumer)

/queue/producer is the endpoint to post message and callback_url into the worker queue. (step 2)

consumer.py is a service to deque message,callback_url from worker queue (step 3) , and push the same message into the callback_url service.

To simulate callback service is up or down, random number is generated in callback service between 0 and 1, and return status 200 or 400 based on random being less than or greater than 0.5.

Based on the response code from callback service either 200 or 400, consumer service will push it back to retry queue, or process the message.

Queue creation is implicitly done when posting the message to /queue/producer.

Producer Message:

hello12
hello11
hello33
hello55
hello40
hello99
hello24
hello65
hello87
hello79
hello12

Consume Message:

retry_exchange  hello12
ack for message  hello11
retry_exchange  hello33
retry_exchange  hello55
ack for message  hello40
ack for message  hello99
ack for message  hello24
retry_exchange  hello65
retry_exchange  hello87
retry_exchange  hello79
ack for message  hello12

Message "hello12" was not processesed due to unavailability of callback_url service,so it was pushed to retry_exchange on first attempt with ttl 1000ms,the message was consumer at later point of time because of availability of service "ack for message  hello12"

Producer:-

Message delivery service takes a message and callback_url to be called,To handle the callback notification gracefully, it uses something call deadletter exchange

Once producer receives a message it puts the message in worker_exchange, which is turn is binded to worker_queue.

Consumer listens for any incoming message on worker_queue, once it receives the message it tries to post the message to callback_url, if callback_url service is available it processes the message, if the callback url service is not available then it puts the message in any another rabbitmq exchange call retry_exchange with a ttl of 1000 ms, so everytime there is a failure in triggering callback_url, message goes to retry_exchange, worker_exchange is defined as dead letter exhcnage(dlx) for retry_exchange, what it means is whenever any failed message expires after 1000 ms in retry_exchange it goes back to worker_exhange, then the message is consumed again by consumer, unless callback_url is triggered successfully for that particular message

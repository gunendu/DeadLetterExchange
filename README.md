# DeadLetterExchange

Frameeork Used :- Django
Messaging Service :- RabbitMq
Code Repo :- https://github.com/gunendu/DeadLetterExchange
App Deployed :- https://git.heroku.com/ddlx.git

Producer:-

Message delivery service takes a message and callback_url to be called,To handle the callback notification gracefully, it uses something call deadletter exchange

Once producer receives a message it puts the message in worker_exchange, which is turn is binded to worker_queue.

Consumer listens for any incoming message on worker_queue, once it receives the message it tries to post the message to callback_url, if callback_url service is available it processes the message, if the callback url service is not available then it puts the message in any another rabbitmq exchange call retry_exchange with a ttl of 1000 ms, so everytime there is a failure in triggering callback_url, message goes to retry_exchange, worker_exchange is defined as dead letter exhcnage(dlx) for retry_exchange, what it means is whenever any failed message expires after 1000 ms in retry_exchange it goes back to worker_exhange, then the message is consumed again by consumer, unless callback_url is triggered successfully for that particular message

Simulate callback_url service by

Producer Message:

hello12\n
hello11\n
hello33\n
hello55\n
hello40\n
hello99\n
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

App is deployed on heroku,start the app locally:-

1) heroku local web (start django server on 5000)
2) curl -H "Content-Type: application/json" -X POST -d '{"message":"hello","callback_url":"http://localhost:5000/queue/consumer/"}' http://localhost:5000/queue/producer/
3) python consumer.py (starts consumer)

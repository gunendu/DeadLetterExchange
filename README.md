# DeadLetterExchange

Frameeork Used :- Django
Messaging Service :- RabbitMq
Code Repo :- https://github.com/gunendu/DeadLetterExchange
App Deployed :- https://git.heroku.com/ddlx.git

Producer:-

Message delivery service takes a message and callback_url to be called,To handle the callback notification gracefully, it uses something call deadletter exchange

Once producer receives a message it puts the message in worker_exchange, which is turn is binded to worker_queue.

Consumer listens for any incoming message on worker_queue, once it receives the message it tries to post the message to callback_url, if callback_url service is available it processes the message, if the callback url service is not available then it puts the message in any another rabbitmq exchange call retry_exchange with a ttl of 1000 ms, so everytime there is a failure in triggering callback_url, message goes to retry_exchange, worker_exchange is defined as dead letter exhcnage(dlx) for retry_exchange, what it means is whenever any failed message expires after 1000 ms in retry_exchange it goes back to worker_exhange, then the message is consumed again by consumer, unless callback_url is triggered successfully.




## Infrastructure

### Node 1

Create the Container `rabbit1` for Node 1:

```bash
docker run -d --hostname rabbit1 --name rabbit1 -e RABBITMQ_ERLANG_COOKIE='rabbitcluster' -p 30000:5672 -p 30001:15672 rabbitmq:management
```

### Node 2

Create the Container `rabbit2` for Node 2:

```bash
docker run -d --hostname rabbit2 --name rabbit2 --link rabbit1:rabbit1 -e RABBITMQ_ERLANG_COOKIE='rabbitcluster' -p 30002:5672 -p 30003:15672 rabbitmq:management
```
Open bash rabbit2 container:

```bash
docker exec -i -t rabbit2 \bash
```
Execute in rabbit2 container:

```bash
    rabbitmqctl stop_app
    rabbitmqctl join_cluster rabbit@rabbit1
    rabbitmqctl start_app
```

### Node 3

Create the Container `rabbit3` for Node 3:

```bash
docker run -d --hostname rabbit3 --name rabbit3 --link rabbit1:rabbit1 -e RABBITMQ_ERLANG_COOKIE='rabbitcluster' -p 30004:5672 -p 30005:15672 rabbitmq:management
```

> For now rabbit3 it's not working


## Experiments

Terminal 1 - Create exchange `sendlogs`, bind with queue `logs` and remains listening to the queue :

```bash
python receive.py
```

Terminal 2 - Send AMQP data for exchange `sendlogs`:

```bash
python send.py
```

The sending is performed by 100 threads that executes the sending 1000 times in an uninterrupted way. A unique id is submitted and the id and the shipping time are printed on the terminal. Upon receipt, the id that was sent and the receipt time are also printed. To calculate latency, just calculate the difference between the two times for the same identifier

### Fontes

[Clustering Guide - official](https://www.rabbitmq.com/clustering.html)
[RABBITMQ IN CLUSTER - 2017](https://piotrminkowski.com/2017/02/28/rabbitmq-in-cluster/)
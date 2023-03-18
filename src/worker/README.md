# Worker

## Описание

Данный микросервис отвечает за выполнение различных задач. Для каждого типа задач необходимо реализовать `Processor`, который умеет обрабатывать данный тип задач.

Для реализации `Processor` необходимо унаследоваться от базового класса `BaseProcessor` и переопределить там методы:
* `_process_task` - здесь происходит обработка задачи
* `supported_topics` - множество поддерживаемых данным процессором типов задач

## Деплой

### Запуск Worker на хосте

```shell
sudo systemctl start bachelor-worker
```

### Рестарт Worker на хосте

```shell
sudo systemctl restart bachelor-worker
```

### Получение статуса Worker

```shell
sudo systemctl status bachelor-worker
```

### Где найти логи:

```shell
less ./bachelor/logs/worker.log
```
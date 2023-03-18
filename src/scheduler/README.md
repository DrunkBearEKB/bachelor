# Scheduler

## Описание

Данный микросервис отвечает за планирование выполнения задач. Обработка задач в планировщике происходит в 2 этапа:
1. постановка задачи в планировщик
2. обработка задачи Worker'ом

Для удобного использования планировщика реализована обёртка над ним `SchedulerWrapper`.
Чтобы поставить задачу в планировщик, необходимо вызвать метод [enqueue](https://github.com/DrunkBearEKB/bachelor/blob/add_base/src/scheduler/scheduler_wrapper/scheduler_wrapper.py#L14) у объекта данной обёртки.
Чтобы посмотреть статус выполнения задачи в планировщике, необходимо вызвать метод [status](https://github.com/DrunkBearEKB/bachelor/blob/add_base/src/scheduler/scheduler_wrapper/scheduler_wrapper.py#L96).

## Деплой

### Запуск Scheduler на хосте

```shell
sudo systemctl start bachelor-scheduler
```

### Рестарт Scheduler на хосте

```shell
sudo systemctl restart bachelor-scheduler
```

### Получение статуса Scheduler

```shell
sudo systemctl status bachelor-scheduler
```

### Где найти логи:

```shell
less ./bachelor/logs/scheduler.log
```
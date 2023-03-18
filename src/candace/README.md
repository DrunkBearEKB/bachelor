# Candace

## Описание

Данный микросервис отвечает за отправку метрик в сервисы, агрегрующие их. 
В данный момент реализована поддержка только Yandex.Monitoring.

Для удобного использования планировщика реализована обёртка над ним `CandaceMonitoringWrapper`.
Чтобы отправить метрику, необходимо вызывать метод [send_monitoring_metric](https://github.com/DrunkBearEKB/bachelor/blob/38e64da021d3cac2906f58649aaf38f5c4c39249/src/candace/candace_wrapper/candace_monitoring_wrapper.py#L13).

## Деплой

### Запуск Candace на хосте

```shell
sudo systemctl start bachelor-candace
```

### Рестарт Candace на хосте

```shell
sudo systemctl restart bachelor-candace
```

### Получение статуса Candace

```shell
sudo systemctl status bachelor-candace
```

### Где найти логи:

```shell
less ./bachelor/logs/candace.log
```
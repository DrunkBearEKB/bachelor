# Bukin

## Описание

Данный микросервис является админкой данного приложения. Доступен по пути: `http://<host>/bukin/`.

## Деплой

### Запуск Bukin на хосте

```shell
sudo systemctl start bachelor-bukin
```

### Рестарт Bukin на хосте

```shell
sudo systemctl restart bachelor-bukin
```

### Получение статуса Bukin

```shell
sudo systemctl status bachelor-bukin
```

### Где найти логи:

```shell
less ./bachelor/logs/bukin.log
```
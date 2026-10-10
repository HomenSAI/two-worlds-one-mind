# Учёт времени книги

[`scripts/time_tracking.py`](scripts/time_tracking.py) ведёт добавляемый журнал работы над книгой и формирует данные для отчётов.

```bash
python scripts/time_tracking.py add --hours 2.5 --note "Редактура главы"
python scripts/time_tracking.py start --note "Работа над переводом"
python scripts/time_tracking.py stop
python scripts/time_tracking.py report --format json
```

По умолчанию 8 часов считаются одним рабочим днём. В отчёте `days_exact` сохраняет дробное значение, а `days_rounded` отдельно округляет его до целых дней по правилу половины вверх. Журнал — `time-log.jsonl`, состояние таймера хранится вне Git.

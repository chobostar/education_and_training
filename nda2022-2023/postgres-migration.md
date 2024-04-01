# PostgreSQL Migration to Cloud using pg_dump/pg_restore

Чтобы понимать из чего складывается время, нужно знать механику под капотом:
* 1 таблица вместе со всеми индексами = 1 поток pg_restore, т.е. увеличивая количество потоков не ускорить восстановление одной большой таблицы
* загрузка данных = сеть + диск
* построенние индексов = диск + цпу

т.е.
* если простаиваеть сеть, то смотрим, что можно сделать с TCP buffer size на виртуалке откуда пушим данные
* если постаивает диск, то думаем, как выжать максимум из диска
*  если простаивает цпу - думать как доутилизовать его, например, почитать про настройки pg:
- `max_parallel_maintenance_workers`
- `maintenance_work_mem`


1. Здесь статья с общими рекомендациями: https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/faster-data-migrations-in-postgres/ba-p/2150850

2.
```
$ pg_restore --help | grep jobs
-j, --jobs=NUM               use this many parallel jobs to restore
```
Временно для миграции можно установить количество ядер на Cloud SQL равной jobs. Т.е. если восстанавливаем в 4 потока => 4 vcpu, в 8 потоков => 8 vcpu итд

3. Увеличить время между checkpoint-ами, механика описана тут:
   https://wiki.postgresql.org/wiki/Full_page_writes#Consequences_for_performance
   Но нужная инфа:
        >>every checkpoint is followed by an increase in WAL traffic, and usually lower transaction throughput.
т.е. на время миграции применить настройки:
```
checkpoint_timeout = 1h    # увеличивает максимальный промежуток между чекпоинтами
max_wal_size = 20GB        # увеличивает threshold WAL-ов между принудительными чекпоинтами
```
так увеличим КПД от генерируемой IO нагрузки
4. pg_restore использует детермированный список заданий для восстановления:
```
   $ pg_restore --help | grep list
   -l, --list               print summarized TOC of the archive
   -L, --use-list=FILENAME      use table of contents from this file for
```
   откуда можно убрать, что можно пропустить
   например, если в базе есть операционные таблицы небольших размеров и архивные для аналитики, то операционный таблицы переносим онлайн, а архивные в оффлайне (вне даунтайма).
   разумеется это нужно делать только понимая, как работает приложение и как используются таблицы.
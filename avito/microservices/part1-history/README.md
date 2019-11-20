### TL DR 
* Как пилить
    * DDD
    * Context
    * Proccesses
    * best practices, recommendations

### Монолит vs Microservices
- Вызовы
	- низкий порог входа
	- понятные ci/cd
	- совместная работа, возможно технического масштабирования
	- ...
- Решения
	- монолит?
		- все в одном репозитории
		- разработчик сразу видит всю картину
		- в view-ки попадает бизнес-логика (н-р: 6-ая картинка увеличенная)
		- бэкофис в той же репе
		- интеграционнное api
		- LB -> avi-http 1..N (различные правила маршрутизации, разные роутеры, домены, правила proxy buffer size, все что мжно тюнить nginx - репа avito-utils)
            - avi-http -> apps 1..M (lxc-контейнеры)
                - cron/daemons
                - user req serving
                - backoffice
            - apps
            - nginx, tcp keepalive с avi-http
            - export rsyslog to CH
            - sentry logger
            - xproxy (nosql-db дискавери через consul)
                - haproxy
                - twemproxy
                    - redis
            - twemproxy
                - memcache (избавлются)
            - haproxy
                - sphinx
            - redis local
            - pgbouncer
                - pgping
                    - проверяет master/replica
                - карусель standby
            - php-fpm
            - cron stats, core-nginx
            avi-http -> k8s
		- apps, k8s -> Databases, Search engines
		- итого:
			- плюсы:
				+ прозрачный процесс deploy, все знают, когда произошел deploy - атомарно всё
				+ легко добавлять новые apps (lxc-контейнеры)
			- минусы:
				- только до определенных масштабов - далее деградация по разработке
				- с ростом сложности (base complexity) деградирует продуктивность
  				- закон общин "общее благо быстро истощается"
					- некоторые приемы обходятся дорого
				- быстрые эксперименты не сделать хорошо в монолите (быстро проверить гипотезу, большой PR, много blame). Замедление роста компании.
				- разграничение доступа. разные code style, куда можно, нельзя коммитить
				- тяжелая dev-среда (локальная разработка)
				- flaky функционал, если делать deadline таймауты
				- сложно расширять стек технологий
			- пример с SSR:
                1) из php кода curl www.avito.st по известному адресу
                2) lb -> avi-http-> ssl -> app-nginx -> firewall -> monolith -> lb (!!!) -> avi-http -> ...
                3) стало x2, сами себя за DDoS-или
                4) быстрофикс -> /etc/hosts -> relative path
	- микросервисы
		- service mesh
		- каждая команда независимо работает
		- API Gateway
			- роутит трафик "куда надо"
			- изолирует проекты друг от друга
			- ...
		- разделение команд
			- уменьшение трения между целями (?), командами
		- 300 разработчиков = 1200 репозиториев (за пару лет)
			- "грязная" работа -> "1000 PR чтобы исправить 1 баг"
		- требования для Cloud Native
			- discovery, orchestration etc.
		- k8s
			- control plane
			- kubelet
				- docker runtime
				- https://github.com/corneliusweig/kubernetes-lxd ( <----- ??? )
				- https://github.com/automaticserver/lxe ( <----- ??? )
		- mesos, openstack итд
		- 400 microservices
		- базовые рекомендации
			- не делать СRUD сервисы (тонкие сервисы), чтобы не увеличивать интеграции
			- базовые шаблоны, чтобы сервисы были похожи друг на друга
			- избегать сильной связанности, избегать каскадные походы
			- определить конечную цель распила монолита
			- не делать циклические походы
		- шаги
            1) SSR, мобильная версия - адаптер перед монолитом
            2) m.avito.ru -> mobile api -> меньше аварий
            3) дублирование правил iptables/firewall по горизонтали для разных точек входа
            4) отдельный endpoint для recommendation (python)
            5) продолжаем копипастить middleware (oauth, например)
            6) делаем единый API Gateway ( nginx + lua )
            - LaaS
            - oauth (session, security, flags etc.)
            - защита от подделок http header (x-user-id)
            - метрики
            - ... middleware
            - искусственное ограничение, чтобы не писать бизнес-логику в gateway
		- есть другие api-gateway из под коробки:
			- The Kong Way (https://github.com/Kong/kong)
			- https://github.com/devopsfaith/krakend
			- https://github.com/alibaba/Sentinel
			- https://github.com/datawire/ambassador
		- композиция:
			- gateway -> business services -> microservice
			- gateway -> monolith -> microservice
		- меняется походы по сети, раньше "всверху вниз", теперь горизонтальные походы
			- сеть на 20% забита UDP пакетами метрик
		- Service proxy
			- L7 слой. надежное межсервисное взаимодействие на уровне приложения
			- envoy, traefik
				- дает телеметрия, LB, трассировка
				- политика retry
				- circuit breaker
			- haproxy, nginx тоже можно использовать как прокси
				- проксирует и держит tcp keeplive
		- Service Mesh
			- выделение сети в инфраструктурный слой
			- автоматическая конфигурация, набор инструментов: pilot, citabel, galey, mixer
			- istio, zuul
		- минусы:
			- больше ресурсов
			- ACID vs BASE, acid уходит. basically avaibility, eventual consistency
			- сложность отладки
			- нужны инфраструктурщики, отдельные люди чтобы "поддерживать штаны"
		- плюсы:
			- быстрые эксперименты
			- независимость
			- graceful падения
			- масштабируемость
				- 3 dimensional scaling, книжка "The art of scalability"
				- базы данных не получится просто масштабировать горизонтально
					- шардирование
				- функцониальная масштабирование
				- критерий масштабируемость - стремиться к линейному
				- можно скейлить отдельные компоненты

### QA
```
- MAPI 100% трафика?
- нет, ~ половина

- где используются саги?
- shops, users

- сервис форматирования цены - пример плохого микросе?
- изначально была просто php-библиотека, требовалось использовать из Go.

- какое решение для API gateway
- самописное

- istio?
- самописаное: envoy + обвязка

- как устроены дежурства?
- мониторинг 24x7, передаем им, то что не неавтоматизировано, написав инструкцию
```
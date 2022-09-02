### Создание кластера изнутри

- load balancer для apiserver-a в облаках это ELB, а для примера можно HAProxy
- kubeadm - рекомендуемый способ, но это только инструмент - нужна обвязка, например kubespray

пример haproxy конфига:
```
global
  log /dev/log  local0
  log /dev/log  local1 notice
  nbproc 2
  stats socket /var/lib/haproxy/stats-1 group haproxy mode 660 level admin process 1
  cpu-map 1 0
  chroot /var/lib/haproxy
  user haproxy
  group haproxy
  daemon

defaults
  log global
  mode  http
  option  httplog
  option  dontlognull
  timeout connect                 500000
  timeout http-request            300s
  timeout client                  5000000
  timeout server                  5000000
  timeout queue                   300s
  timeout check                   5s
frontend kube_ingress_tcp
    mode tcp
    bind *:80
    default_backend kube_ingress_80_tcp
frontend kube_ingress_ssl_tcp
    mode tcp
    bind *:443
    default_backend kube_ingress_443_tcp
frontend kube_master_ssl_tcp
    mode tcp
    bind *:6443
    default_backend kube_master_6443_tcp
backend kube_ingress_80_tcp
    mode tcp
    fullconn 100000
    server 172.26.108.6 172.26.108.6:80 check inter 500 fall 1 rise 2
    server 172.26.108.7 172.26.108.7:80 check inter 500 fall 1 rise 2
backend kube_ingress_443_tcp
    mode tcp
    fullconn 100000
    server 172.26.108.6 172.26.108.6:443 check inter 500 fall 1 rise 2
    server 172.26.108.7 172.26.108.7:443 check inter 500 fall 1 rise 2
backend kube_master_6443_tcp
    mode tcp
    fullconn 100000
    server 172.26.108.2 172.26.108.2:6443 check inter 500 fall 1 rise 2
    server 172.26.108.3 172.26.108.3:6443 check inter 500 fall 1 rise 2
    server 172.26.108.4 172.26.108.4:6443 check inter 500 fall 1 rise 2
```


coredns:
https://coredns.io/plugins/autopath/

```
  Corefile: |
    .:53 {
	errors
	health {
           lameduck 5s
        }
	ready
	autopath @kubernetes
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
	prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
	cache 30
        loop
	reload
	loadbalance
    }
```

Authentication:
- сертификаты
- файл с токенами
- файл с логинами/паролями (basic)
- service account (внутренние пользователи)
- authentication proxy
- OIDC (openid connect, oauth2)


#!/bin/sh
kubectl create namespace base
kubectl create namespace prod
kubectl create namespace dev

kubectl label ns prod type=prod

kubectl run base --image centosadmin/utils --namespace base
kubectl run test --image centosadmin/utils --namespace base
kubectl run access --image centosadmin/utils --namespace base
kubectl expose pod base --port=22 --name=bd2 --namespace base

kubectl run test --image centosadmin/utils --namespace prod
kubectl run access --image centosadmin/utils --namespace prod

kubectl run test --image centosadmin/utils --namespace dev
kubectl run access --image centosadmin/utils --namespace dev

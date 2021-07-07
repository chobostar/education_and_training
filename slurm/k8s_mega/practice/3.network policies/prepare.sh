#!/bin/sh
kubectl create namespace base
kubectl create namespace prod
kubectl create namespace dev

kubectl label ns prod type=prod

kubectl run base --image=raesene/alpine-nettools --namespace base
kubectl run test --image=raesene/alpine-nettools --namespace base
kubectl run access --image=raesene/alpine-nettools --namespace base
kubectl expose pod base --port=22 --name=bd2 --namespace base

kubectl run test --image=raesene/alpine-nettools --namespace prod
kubectl run access --image=raesene/alpine-nettools --namespace prod

kubectl run test --image=raesene/alpine-nettools --namespace dev
kubectl run access --image=raesene/alpine-nettools --namespace dev

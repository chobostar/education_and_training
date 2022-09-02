#!/bin/bash

# Get username from host
USER_NAME=$(hostname | awk -F"." '{print $2}')

# Make tmp dir for certificates
mkdir -p ssl

cat << EOF > ssl/req.cnf
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name

[req_distinguished_name]

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = auth.$USER_NAME.edu.slurm.io
DNS.2 = kubectl.$USER_NAME.edu.slurm.io

EOF
# Generate root certificate
openssl genrsa -out ssl/ca-key.pem 2048
openssl req -x509 -new -nodes -key ssl/ca-key.pem -days 3650 -sha256 -out ssl/ca.pem -subj "/CN=OIDC AUTH Slurm EDU CA"

# Create secret with root certificate
kubectl create secret generic ca --from-file ssl/ca.pem --namespace kube-system

# Generate certificate for dex
openssl genrsa -out ssl/key-dex.pem 2048
openssl req -new -key ssl/key-dex.pem -out ssl/csr-dex.pem -subj "/C=RU/ST=MSK/L=MOSKOW/O=Slurm edu/OU=Edu/CN=auth.$USER_NAME.edu.slurm.io" -sha256 -config ssl/req.cnf
openssl x509 -req -in ssl/csr-dex.pem -CA ssl/ca.pem -CAkey ssl/ca-key.pem -CAcreateserial -sha256 -out ssl/cert-dex.pem -days 3650  -extensions v3_req -extfile ssl/req.cnf

# Create secret for dex with certificate and key
kubectl create secret tls dex-tls --key ssl/key-dex.pem --cert ssl/cert-dex.pem --namespace kube-system

# Generate certificate for gangway
openssl genrsa -out ssl/key-gangway.pem 2048
openssl req -new -key ssl/key-gangway.pem -out ssl/csr-gangway.pem -subj "/C=RU/ST=MSK/L=MOSKOW/O=Slurm edu/OU=Edu/CN=kubectl.$USER_NAME.edu.slurm.io" -sha256 -config ssl/req.cnf
openssl x509 -req -in ssl/csr-gangway.pem -CA ssl/ca.pem -CAkey ssl/ca-key.pem -CAcreateserial -sha256 -out ssl/cert-gangway.pem -days 3650  -extensions v3_req -extfile ssl/req.cnf

# Create secret for gangway with certificate and key
kubectl create secret tls gangway-tls --key ssl/key-gangway.pem --cert ssl/cert-gangway.pem --namespace kube-system

# Running in Kubernetes

The configurations will be added later.

## Deploy Kubernetes Cluster

```bash
kind create cluster --name=cluster0 --config=kind-config.yaml
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml
kubectl apply -f deploy-crd.yaml
```

## Deploy Jenkins

```bash
docker container run --name jenkins-docker --rm -d --privileged --network kind --network-alias docker -p 2376:2376 \
--env DOCKER_TLS_CERTDIR=/certs -v jenkins-docker-certs:/certs/client -v jenkins-data:/var/jenkins_home docker:dind --insecure-registry harbor.orcunuso.io

docker container run --name jenkins-blueocean --rm -d --network kind --env DOCKER_HOST=tcp://docker:2376 \
--env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 -v jenkins-data:/var/jenkins_home \
-v jenkins-docker-certs:/certs/client:ro -p 8080:8080 orcunuso/jenkinsci-bo:1.23.2

cp /root/.kube/config /root/jenkins
# edit config -> cluster0-control-plane:6443
docker cp /root/jenkins/config jenkins-blueocean:/kubernetes/config
```

## Deploy DemoApp from Helm Repository

```bash
helm repo list
helm search repo harbor
helm install --set applicationBlue.replicas=2 --set applicationBlue.image.tag=v1 --set ingress.weightBlue=100 --set job.enabled=true demoapp harbor/demoapp
helm list
helm get manifest demoapp | grep "# Source"
kubectl -n demoapp get pods -o wide
kubectl -n demoapp get pods,jobs,deployments,svc,pvc,sa,cm,secrets,ingressroutes -o name
```

## Commit and trigger Jenkins build

* Add a new subpath in the source code
* Commit and push code
* Trigger a manuel Jenkins build

### For Jenkins Tests (Not used in regular workflow)

```bash
docker container run --name jenkins-test --rm -d --network kind --env DOCKER_HOST=tcp://docker:2376 \
--env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 orcunuso/jenkinsci-bo:1.23.2
docker cp /root/jenkins/config jenkins-test:/kubernetes/config
docker exec -it jenkins-test /bin/bash
helm repo add --ca-file /kubernetes/ca.crt --username=svcdemoapp --password=password harbor <https://harbor.orcunuso.io/chartrepo/demoapp>
helm upgrade --wait --set applicationBlue.replicas=2 --set applicationGreen.replicas=2 --set applicationGreen.image.tag=v2 --set applicationBlue.image.tag=v1 demoapp harbor/demoapp
```

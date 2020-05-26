# Application Lifecycle with Kubernetes, Jenkins and Helm

* Deploy a Kubernetes cluster with KinD (Three masters and one worker).
* Deploy Jenkins and then create a multibranch pipeline with Blue Ocean.
* Deploy the application (v1) on Kubernetes with Helm chart which is already pushed to Harbor.
* Commit a new change to the newurl branch and trigger a new Jenkins build.
* Experience blue/green deployment triggered by Jenkins and have fun :)

## Deploy Kubernetes Cluster

```bash
kind create cluster --name=cluster0 --config=kubernetes/kind-config-ha.yaml
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml
kubectl apply -f kubernetes/deploy-crd.yaml
```

## Deploy Jenkins

In order to execute Docker commands inside Jenkins nodes, download and run the `docker:dind` Docker image using the following docker container run command.

```bash
docker container run --name jenkins-docker --rm -d --privileged --network kind --network-alias docker -p 2376:2376 \
--env DOCKER_TLS_CERTDIR=/certs -v jenkins-docker-certs:/certs/client -v jenkins-data:/var/jenkins_home docker:dind --insecure-registry harbor.orcunuso.io

docker container run --name jenkins-blueocean --rm -d --network kind --env DOCKER_HOST=tcp://docker:2376 \
--env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 -v jenkins-data:/var/jenkins_home \
-v jenkins-docker-certs:/certs/client:ro -p 8080:8080 harbor.orcunuso.io/demoapp/jenkinsci-bo:1.23.2

cp /root/.kube/config /root/jenkins
sed -i 's/kind.orcunuso.io/cluster0-control-plane/g' /root/jenkins/config
docker cp /root/jenkins/config jenkins-blueocean:/kubernetes/config
docker exec -it jenkins-blueocean kubectl get nodes
docker exec -it jenkins-blueocean docker pull centos/python-36-centos7:20200514-897c8e3
docker exec -it jenkins-blueocean docker images
```

## Deploy DemoApp from Helm Repository

```bash
helm repo list
helm search repo harbor
helm install --set applicationBlue.replicas=2 --set applicationBlue.image.tag=v1 --set ingress.weightBlue=100 --set job.enabled=true demoapp harbor/demoapp
helm list
helm get manifest demoapp | grep "# Source"
kubectl -n demoapp get pods,jobs,deployments,svc,pvc,sa,cm,secrets,ingressroutes -o name
```

<hr style="height:2px;border-width:0;color:gray;background-color:gray">

These commands are not a part of the regular flow, only used for troubleshooting purposes

```bash
docker container run --name jenkins-test --rm -d --network kind --env DOCKER_HOST=tcp://docker:2376 \
--env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 orcunuso/jenkinsci-bo:1.23.2
docker cp /root/jenkins/config jenkins-test:/kubernetes/config
docker exec -it jenkins-test /bin/bash
helm repo add --ca-file /kubernetes/ca.crt --username=svcdemoapp --password=password harbor <https://harbor.orcunuso.io/chartrepo/demoapp>
helm upgrade --wait --set applicationBlue.replicas=2 --set applicationGreen.replicas=2 --set applicationGreen.image.tag=v2 --set applicationBlue.image.tag=v1 demoapp harbor/demoapp
```

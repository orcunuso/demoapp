pipeline { 
    agent any

    environment {
        REPO_URI = "harbor.orcunuso.io/demoapp/demoapp"
        HELM_APP_NAME = "demoapp"
        HELM_CHART_NAME = "harbor/demoapp"
        COLOR_PROD = "Blue"
        COLOR_TEST = "Green"
        VERSION_PROD = "v1"
        VERSION_TEST = "v2"
    }
    
    stages {
        stage('Build Image'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-login', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login harbor.orcunuso.io --username="${USERNAME}" --password="${PASSWORD}"'
                    sh "docker build -t ${REPO_URI}:${VERSION_TEST} ."
                    sh 'docker image ls'
                }
            }
        }
        stage('Push Image to Harbor') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-login', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh "docker push ${REPO_URI}:${VERSION_TEST}"
                }
            }
        }
        stage('Deploy Image with Helm (Blue/Green)') {
            steps {
                    withCredentials([usernamePassword(credentialsId: 'harbor-login', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh "helm repo add --ca-file /kubernetes/ca.crt --username=${USERNAME} --password=${PASSWORD} harbor https://harbor.orcunuso.io/chartrepo/demoapp"
                    sh 'helm repo update'
                    sh 'helm search repo harbor'
                    sh 'helm list'
                    sh "helm upgrade --wait --set application${COLOR_TEST}.replicas=2 --set application${COLOR_PROD}.replicas=2 --set application${COLOR_TEST}.image.tag=${VERSION_TEST} --set application${COLOR_PROD}.image.tag=${VERSION_PROD} --set ingress.weight${COLOR_PROD}=100 ${HELM_APP_NAME} ${HELM_CHART_NAME}"
                }
            }
        }
        stage('Waiting for approval') {
            steps {
                timeout(time: 15, unit: "MINUTES") {
                    input message: 'Do you want to approve the deploy in production?', ok: 'Yes'
                }
            }
        }
        stage('Deploy to Production') {
            steps {
                sh "helm upgrade --wait --set application${COLOR_TEST}.replicas=2 --set application${COLOR_TEST}.image.tag=${VERSION_TEST} --set ingress.weight${COLOR_TEST}=100 ${HELM_APP_NAME} ${HELM_CHART_NAME}"
            }
        }
    }
}

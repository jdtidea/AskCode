@Library(["com.optum.runiac.pipeline.library@main", "com.optum.jenkins.pipeline.library@master"]) _

def config = [
     azureCredentialsId: "askoptum-nonprod",
     environment: "dev",
     dryRun: true,
     executionDirectory: "./infra",
     account: "8a8f04fc-cf3d-433f-972a-5ff0e8615f54"
]

// is master
if (env.BRANCH_NAME == "master") {
    config.dryRun = false
}

if (env.CHANGE_ID) {
    env.IMAGE_TAG = env.CHANGE_ID
} else if (env.BRANCH_NAME == "master") {
    env.IMAGE_TAG = "latest"
} else {
    env.IMAGE_TAG = env.BRANCH_NAME
}

env.IMAGE_REPO = "askoptum"

// for runiac deploy to configure correct app service container
// this will likely shift in future to outside of terraform to support stage deploys and 'zero-downtime'
// current deployment may expect ~30s of downtime while shifting to new container
env.TF_VAR_docker_tag=env.IMAGE_TAG;
env.TF_VAR_docker_image=env.IMAGE_REPO;

pipeline {
    agent {
        label 'docker-nodejs-slave'
    }
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        ansiColor('xterm')
    }
    stages {
        stage('Test') {
            parallel {
                stage('Test Frontend') {
                    steps {
                        sh label: 'npm test', script:'''
                            #!/bin/bash
                            . /etc/profile.d/jenkins.sh
                            ./scripts/test_frontend.sh
                        '''
                    }
                }
                stage('Test Backend') {
                    steps {
                        sh label: 'pytest', script:'''
                            #!/bin/bash
                            . /etc/profile.d/jenkins.sh
                            ./scripts/test_backend.sh
                        '''
                    }
                }
            }
        }
        stage('Build') {
            parallel {
                stage('Build Frontend') {
                    steps {
                        sh label: 'npm install && npm build', script:'''
                            #!/bin/bash
                            . /etc/profile.d/jenkins.sh
                            npm version
                            bash ./scripts/build_frontend.sh
                        '''
                    }
                }
                stage('Docker Build Backend') {
                    steps {
                        withCredentials([azureServicePrincipal(credentialsId: config.azureCredentialsId,
                            subscriptionIdVariable: 'ARM_SUBSCRIPTION_ID',
                            clientIdVariable: 'ARM_CLIENT_ID',
                            clientSecretVariable: 'ARM_CLIENT_SECRET',
                            tenantIdVariable: 'ARM_TENANT_ID')]) {
                                sh label: 'Backend', script:'''
                                    #!/bin/bash
                                    export AZURECLI_VERSION=2.22.1
                                    . /etc/profile.d/jenkins.sh

                                    az login --service-principal -u $ARM_CLIENT_ID -p $ARM_CLIENT_SECRET --tenant $ARM_TENANT_ID
                                    az account set -s $ARM_SUBSCRIPTION_ID
                                    bash ./scripts/build_backend.sh $IMAGE_REPO $IMAGE_TAG
                                '''
                        }
                    }
                }
            }
        }

        stage('Code Quality') {
            parallel {
                stage('Sonar Frontend') {
                    steps {
                        dir('frontend') {
                            glSonarNpmScan gitUserCredentialsId: 'askoptum-github-token',
                                additionalProps:[
                                    'sonar.sources':'src',
                                    'sonar.javascript.lcov.reportPath': 'coverage/lcov.info',
                                    'sonar.ts.lcov.reportpath':'coverage/lcov.info',
                                    'sonar.projectName': 'askoptum-frontend',
                                    'sonar.projectKey': 'com.optum.askoptum:frontend'
                                ]
                        }
                    }
                }
                stage('Sonar Backend') {
                    steps {
                        glSonarScan gitUserCredentialsId: 'askoptum-github-token',
                            sources: 'backend/app',
                            sonarServer: 'sonar.optum',
                            additionalProps: [
                                'sonar.python.coverage.reportPaths': 'backend/coverage.xml',
                                'sonar.projectName': 'askoptum-backend',
                                'sonar.projectKey': 'com.optum.askoptum:backend',
                                'sonar.language': 'py',
                                'sonar.tests': 'backend/tests',
                                'sonar.exclusions': 'backend/app/patches/**'
                            ]
                    }
                }
            }
        }
        stage ('Deploy Dev') {
            steps {
                runiacDeployAzureStep(config)
            }
        }
        stage ('Deploy Prod') {
            steps {
                script {
                    config.environment = "prod"
                }
                sh label: 'npm install && npm build', script:'''
                    #!/bin/bash
                    . /etc/profile.d/jenkins.sh
                    npm version
                    export REACT_APP_AO_ENV=prod
                    bash ./scripts/build_frontend.sh
                '''
                runiacDeployAzureStep(config)
            }
        }
    }
}


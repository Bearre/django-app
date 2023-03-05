pipeline {
    agent any
    stages {
        stage('PREBUILD') {
            steps {
                echo 'Sending notifications'
                build job: 'CREDIT-CARD-APP/SEND_NOTIFICATION', parameters: [string(name: 'BOT_TOKEN', value: '$BOT_TOKEN'), \
                                                                             string(name: 'CHAT_ID', value: '800772053'), \
                                                                             string(name: 'TEXT', value: 'PIPELINE_STARTED')]
                mail bcc: '', body: 'DEPLOY $BUILD_ID OF VERSION $VERSION STARTED', cc: '', from: '', replyTo: '', subject: 'DEPLOY CREDIT-APP VERSION $VERSION', to: 'Urthrill@yandex.ru'
                //emailextrecipients([developers()])
            }
        }
        
        stage('CHECK CONFIGS') {
            steps {
                script {
                    def check_config_job = build job: 'CREDIT-CARD-APP/CHECK_CONFIGS'
                    
                    if (check_config_job.status == 'Failed') {
                        currentBuild.result = 'Failed'
                        ansiColor('xterm') {
                            error("DID NOT PASSED CONFIG CHECK")
                        }
                    }
                }
            }
        }
        
        stage('CHECK REQUIREMENTS') {
            steps {
                //Проверка конфигов, файлов параметров и скриптов
                sh "ssh oracle@192.168.56.104 bash -c '~/SCRIPTS/install-requirements.sh $NODE'"
            }
        }

        stage('BUILD') {
            steps {
                ansiColor('xterm') {
                    echo 'BUILD'
                }
            }
        }

        stage('DEPLOY TO TEST') {
            steps {
                timeout(activity: true, time: 180, unit: 'SECONDS') {
                    sh 'ssh oracle@192.168.56.104 "ansible-playbook -i inv-production -e "healthcheck=yes" --extra-vars "stage=prod" --tags node_5 deploy_docker_app.yaml"'
                    }
            }
        }

        stage('CHECK TEST IS OK') {
            steps {
                timeout(activity: true, time: 30, unit: 'SECONDS') {
                    sleep 15 
                    }
                catchError(stageResult: 'FAILURE') {
                    sh 'ssh oracle@192.168.56.104 "docker ps | grep node_5"'
                    sleep 15
                    build job: 'CREDIT-CARD-APP/CHECK_URL', parameters: [string(name: 'STAGE', value: 'TEST')]
                    }
                 }
        }
        
        stage('DEPLOYMENT TO DATABASE') {
            when {
                environment name: 'DEPLOY_TO_DATABASE', value: 'true'
            }
            steps {
                timeout(activity: true, time: 30, unit: 'SECONDS') {
                    script {
                        def database_deploy = build job: 'CREDIT-CARD-DB/DEPLOY_SQL_TO_DATABASE'
                        
                        if (database_deploy.status == 'Failed') {
                        currentBuild.result = 'Failed'
                        error("DEPLOY TO DATABASE FAILED")
                        }
                     }   
                 } 
                echo "Restarting database cluster after deploy"
                echo "Triggering restart db job"
                build job: 'CREDIT-CARD-DB/DEPLOY_SQL_TO_DATABASE'
                echo "Waiting 30 seconds after restart"
                sleep time: 30, unit: 'SECONDS' 
            }
        }
        stage('DEPLOY TO PROD') {
            when {
                expression {
                    return env.NODE != 'TEST';
                }
            }
            steps {
                timeout(activity: true, time: 60, unit: 'SECONDS') {
                    input message: 'PERFORM DEPLOY?', ok: 'Yes', submitter: 'jenkins', submitterParameter: 'Approver'
                    echo 'DEPLOY STARTED ON $NODE'
                }
                //script {
                //   node = input message: 'Enter NODE to deploy',
                //   parameters:[string(defaultValue: '', description: '',
                //    name: 'NODE'),choice(choices: 'node_1\nnode_2\nnode_3\nnode_4',
                //    description: '', name: 'NODE')]
                // }
                timeout(activity: true, time: 360, unit: 'SECONDS') {
                    sh 'ssh oracle@192.168.56.104 "ansible-playbook -i inv-production -e "healthcheck=yes" --extra-vars "stage=prod" --tags $NODE deploy_docker_app.yaml"'
                    }
            }
        }
        stage('STOP $NODE') {
            steps {
                timeout(activity: true, time: 30, unit: 'SECONDS') {
                    //
                    }
            }
        }
        stage('START $NODE') {
            steps {
                timeout(activity: true, time: 30, unit: 'SECONDS') {
                    //
                    }
                sleep time: 30, unit: 'SECONDS'
            }
        }
        
        stage('CHECK PROD IS OK') {
            steps {
                timeout(activity: true, time: 30, unit: 'SECONDS') {
                    sleep 15 
                    }
                catchError(stageResult: 'FAILURE') {
                    build 'CREDIT-CARD-APP/CHECK STATUS'
                    build job: 'CREDIT-CARD-APP/CHECK_URL', parameters: [string(name: 'STAGE', value: 'PROD')]
                    }
                 }
        }
        
        stage('POST BUILD') {
            steps {
                cleanup {
                    cleanWs()
                }
                //echo 'Sending mail to Urthrill@yandex.ru'
                build job: 'CREDIT-CARD-APP/SEND_NOTIFICATION', parameters: [string(name: 'BOT_TOKEN', value: '$BOT_TOKEN'), \
                                                                             string(name: 'CHAT_ID', value: '800772053'), \
                                                                             string(name: 'TEXT', value: 'PIPELINE_FINISHED')]
                mail bcc: '', body: 'DEPLOY $BUILD_ID OF VERSION $VERSION FINISHED', cc: '', from: '', replyTo: '', subject: 'DEPLOY CREDIT-APP VERSION $VERSION', to: 'Urthrill@yandex.ru'
                //emailextrecipients([developers()])            
            }
        }
    }
}

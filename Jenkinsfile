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
                echo 'BUILD'
                //Проверка установленных пакетов и версий
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
                echo 'BUILD'
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
                    sh 'sleep 15' 
                    }
                catchError(stageResult: 'FAILURE') {
                    sh 'ssh oracle@192.168.56.104 "docker ps | grep node_5"'
                    shell '''
                               STATUS=$(curl -I http://$URI | grep 200 | awk "{print $2}")
                               if [ $STATUS == '200' ];
                               then
                                   echo 'STATUS 200'
                               elif [ $STATUS == '301' ] ;
                               then
                                   echo 'STATUS 301, CAN CONTINUE'
                               else
                                   echo "SOMETHING WENT WRONG, RESPONCE CODE: ${STATUS} && curl -XGET http://$BUILD_URL/stop
                               fi
                          '''
                        }
                 }
        }
        
        stage('DEPLOYMENT TO DATABASE') {
            when {
                environment name: 'DEPLOY_TO_DATABASE', value: 'true'
            }
            steps {
                timeout(activity: true, time: 30, unit: 'SECONDS') {
                    //
                    }
                echo "Restarting database cluster after deploy"
                //echo "Triggering job"
                //sh 'curl -XGET http://192.168.56.104:8080/job/CREDIT-CARD-DB/job/Restart%20cluster/build?token=restartpostgrestrigger'
                //sleep time: 30, unit: 'SECONDS'
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
        stage('POST BUILD') {
            steps {
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

pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_RUN',
            choices: ['diploma', 'api_only'],
            description: 'diploma — три прогона (API, UI, Mobile): три Allure-отчёта и три сообщения в Telegram. api_only — только API (быстро, без браузера).'
        )
        string(
            name: 'ALLURE_PROJECT_ID',
            defaultValue: '5127',
            description: 'ID проекта в Allure TestOps (число из URL). Оставь пустым, если не нужна загрузка в TestOps.'
        )
        string(
            name: 'APP_PATH',
            defaultValue: '',
            description: 'Путь к APK для Mobile (если без BrowserStack). Пусто = мобильные пропускаются, если не включён BrowserStack.'
        )
        booleanParam(
            name: 'USE_BROWSERSTACK_MOBILE',
            defaultValue: true,
            description: 'Запускать мобильные тесты в BrowserStack (нужны credentials: bstack-username, bstack-access-key, bstack-app).'
        )
    }

    environment {
        ALLURE_ENDPOINT = 'https://allure.autotests.cloud'
        ALLURE_PROJECT_ID = "${params.ALLURE_PROJECT_ID}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 60, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'python3 -m venv .venv || true'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                script {
                    if ((params.TEST_RUN ?: 'diploma') == 'diploma') {
                        def creds = [
                            string(credentialsId: 'telegram-bot-token', variable: 'TELEGRAM_BOT_TOKEN'),
                            string(credentialsId: 'telegram-chat-id', variable: 'TELEGRAM_CHAT_ID')
                        ]
                        if (params.USE_BROWSERSTACK_MOBILE) {
                            creds.addAll([
                                string(credentialsId: 'bstack-username', variable: 'BSTACK_USERNAME'),
                                string(credentialsId: 'bstack-access-key', variable: 'BSTACK_ACCESS_KEY'),
                                string(credentialsId: 'bstack-app', variable: 'BSTACK_APP')
                            ])
                        }
                        withCredentials(creds) {
                            withEnv(params.APP_PATH?.trim() ? ["APP_PATH=${WORKSPACE}/${params.APP_PATH.trim()}"] : []) {
                                sh '''
                                    . .venv/bin/activate
                                    pip install Appium-Python-Client -q
                                    [ -n "${BSTACK_APP}" ] && export MOBILE_CONTEXT=bstack
                                    [ -n "${APP_PATH}" ] && export APP_PATH
                                    python3 scripts/run_diploma_runs.py
                                '''
                            }
                        }
                    } else {
                        sh '''
                            . .venv/bin/activate
                            pytest tests/API/ -v --tb=short --alluredir=allure-results --clean-alluredir 2>&1 | tee pytest.log; true
                        '''
                    }
                }
            }
        }

        stage('Allure Report') {
            steps {
                script {
                    if ((params.TEST_RUN ?: 'diploma') == 'diploma') {
                        allure(
                            results: [
                                [path: 'allure-results-api'],
                                [path: 'allure-results-ui'],
                                [path: 'allure-results-mobile']
                            ],
                            reportBuildPolicy: 'ALWAYS'
                        )
                    } else {
                        allure(
                            results: [[path: 'allure-results']],
                            reportBuildPolicy: 'ALWAYS'
                        )
                    }
                }
            }
        }

        stage('Allure TestOps Upload') {
            when {
                allOf {
                    expression { env.ALLURE_ENDPOINT != null && env.ALLURE_ENDPOINT != '' }
                    expression { env.ALLURE_PROJECT_ID != null && env.ALLURE_PROJECT_ID != '' }
                }
            }
            steps {
                withCredentials([string(credentialsId: 'allure-testops-token', variable: 'ALLURE_TOKEN')]) {
                script {
                    def run = (params.TEST_RUN ?: 'diploma')
                    def launchBase = "Premier #${env.BUILD_NUMBER ?: 'build'}"
                    def arch = sh(script: 'uname -m', returnStdout: true).trim()
                    def allurectl = "allurectl_linux_amd64"
                    if (arch.contains('aarch64') || arch.contains('arm64')) {
                        allurectl = "allurectl_linux_arm64"
                    }
                    sh """
                        ALLURECTL=allurectl
                        if ! command -v allurectl 2>/dev/null; then
                            wget -q "https://github.com/allure-framework/allurectl/releases/latest/download/${allurectl}" -O allurectl || true
                            chmod +x allurectl 2>/dev/null || true
                            ALLURECTL=./allurectl
                        fi
                        if [ ! -x "\$ALLURECTL" ] 2>/dev/null && [ ! -x allurectl ] 2>/dev/null; then
                            echo "allurectl not found, skipping TestOps upload"
                            exit 0
                        fi
                        if [ -d allure-results-api ] && [ -d allure-results-ui ] && [ -d allure-results-mobile ]; then
                            ALLURE_LAUNCH_NAME="${launchBase} API"   \$ALLURECTL upload allure-results-api  || true
                            unset ALLURE_JOB_RUN_UID ALLURE_JOB_UID ALLURE_JOB_RUN_ID ALLURE_JOB_ID JENKINS_URL BUILD_URL JOB_NAME BUILD_NUMBER 2>/dev/null || true
                            ALLURE_LAUNCH_NAME="${launchBase} UI"    \$ALLURECTL upload allure-results-ui   || true
                            unset ALLURE_JOB_RUN_UID ALLURE_JOB_UID ALLURE_JOB_RUN_ID ALLURE_JOB_ID JENKINS_URL BUILD_URL JOB_NAME BUILD_NUMBER 2>/dev/null || true
                            ALLURE_LAUNCH_NAME="${launchBase} Mobile" \$ALLURECTL upload allure-results-mobile || true
                        else
                            ALLURE_LAUNCH_NAME="${launchBase}" \$ALLURECTL upload allure-results 2>/dev/null || true
                        fi
                    """
                }
                }
            }
        }

        stage('Telegram Notify') {
            when {
                expression { (params.TEST_RUN ?: 'diploma') == 'api_only' }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'telegram-bot-token', variable: 'TELEGRAM_BOT_TOKEN'),
                    string(credentialsId: 'telegram-chat-id', variable: 'TELEGRAM_CHAT_ID')
                ]) {
                    sh '''
                        . .venv/bin/activate
                        SUMMARY=$(tail -1 pytest.log 2>/dev/null) || SUMMARY="Build #${BUILD_NUMBER}"
                        python3 scripts/telegram_notify.py "Premier Tests #${BUILD_NUMBER}\n\n${SUMMARY}\n\n${BUILD_URL}"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        failure {
            echo 'Build failed'
        }
    }
}

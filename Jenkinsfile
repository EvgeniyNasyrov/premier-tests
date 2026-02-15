pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_RUN',
            choices: ['diploma', 'api_only'],
            description: 'diploma — три прогона (API, UI, Mobile): три Allure-отчёта и три сообщения в Telegram. api_only — только API (быстро, без браузера).'
        )
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
                sh '''
                    . .venv/bin/activate
                    TEST_RUN="${TEST_RUN:-diploma}"
                    if [ "${TEST_RUN}" = "diploma" ]; then
                        [ -n "${BSTACK_APP}" ] && export MOBILE_CONTEXT=bstack || true
                        python3 scripts/run_diploma_runs.py
                    else
                        pytest tests/API/ -v --tb=short --alluredir=allure-results --clean-alluredir 2>&1 | tee pytest.log; true
                    fi
                '''
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

        stage('Telegram Notify') {
            when {
                allOf {
                    expression { (params.TEST_RUN ?: 'diploma') == 'api_only' }
                    expression { env.TELEGRAM_BOT_TOKEN != null && env.TELEGRAM_BOT_TOKEN != '' }
                }
            }
            steps {
                sh '''
                    . .venv/bin/activate
                    SUMMARY=$(tail -1 pytest.log 2>/dev/null) || SUMMARY="Build #${BUILD_NUMBER}"
                    python3 scripts/telegram_notify.py "Premier Tests #${BUILD_NUMBER}\n\n${SUMMARY}\n\n${BUILD_URL}"
                '''
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

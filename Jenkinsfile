pipeline {
    agent any
    environment {
        APP_PORT = '5000'
        DOCKER_NET = 'devsecops-lab'
        APP_IMAGE = 'devsecops-app:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Récupération du code source...'
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Construction de l image Docker...'
                script {
                    if (isUnix()) {
                        sh "docker build -t ${APP_IMAGE} ."
                    } else {
                        bat "docker build -t ${APP_IMAGE} ."
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Exécution des tests unitaires...'
                script {
                    if (isUnix()) {
                        sh "docker run --rm -v ${env.WORKSPACE}:/app -w /app ${APP_IMAGE} pytest tests/ -v"
                    } else {
                        bat "docker run --rm -v ${env.WORKSPACE}:/app -w /app ${APP_IMAGE} pytest tests/ -v"
                    }
                }
            }
        }

        stage('SAST - Bandit Scan') {
            steps {
                echo 'Analyse statique avec Bandit...'
                script {
                    def cmd = isUnix() ? 'sh' : 'bat'
                    try {
                        "${cmd}" """
                        docker run --rm -v ${env.WORKSPACE}:/app -w /app ${APP_IMAGE} bandit -r app/ -f json -o bandit-report.json
                        """
                    } catch(Exception e) {
                        echo "Bandit a retourné une erreur mais on continue : ${e}"
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                echo 'Pentest dynamique avec ZAP...'
                script {
                    if (isUnix()) {
                        sh """
                        docker run -d --name target-app --network ${DOCKER_NET} -p ${APP_PORT}:5000 ${APP_IMAGE}
                        sleep 5
                        """
                        sh """
                        docker run --rm --network ${DOCKER_NET} -v ${env.WORKSPACE}:/zap/wrk ghcr.io/zaproxy/zaproxy:stable \\
                        zap-baseline.py -t http://target-app:5000 -r zap-report.html -J zap-report.json -I
                        """
                        sh 'docker stop target-app || true'
                        sh 'docker rm target-app || true'
                    } else {
                        bat """
                        docker run -d --name target-app --network ${DOCKER_NET} -p ${APP_PORT}:5000 ${APP_IMAGE}
                        timeout /T 5 /NOBREAK
                        """
                        bat """
                        docker run --rm --network ${DOCKER_NET} -v ${env.WORKSPACE}:/zap/wrk ghcr.io/zaproxy/zaproxy:stable ^
                        zap-baseline.py -t http://target-app:5000 -r zap-report.html -J zap-report.json -I
                        """
                        bat 'docker stop target-app || exit 0'
                        bat 'docker rm target-app || exit 0'
                    }
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: true,
                        reportDir: '.',
                        reportFiles: 'zap-report.html',
                        reportName: 'ZAP Security Report'
                    ])
                    archiveArtifacts artifacts: 'zap-report.json', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success { echo 'Pipeline terminé avec succès !' }
        failure { echo 'Pipeline échoué, vérifier les logs.' }
    }
}
pipeline {
    agent any
    environment {
        APP_PORT   = '5000'
        ZAP_PORT   = '8090'
        DOCKER_NET = 'devsecops-lab'
        WORKSPACE  = 'C:/ProgramData/Jenkins/.jenkins/workspace/devsecops-lab'
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Récupération du code source...'
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                echo 'Installation des dépendances et exécution des tests unitaires... 🔧'
                powershell """
                docker run --rm `
                    -v ${WORKSPACE}:/workspace `
                    -w /workspace `
                    python:3.11-slim `
                    powershell -Command \"
                        pip install -r app/requirements.txt; `
                        pytest tests/ -v
                    \"
                """
            }
        }

        stage('SAST - Bandit Security Scan') {
            steps {
                echo 'Analyse de sécurité statique du code (SAST)...'
                powershell """
                docker run --rm `
                    -v ${WORKSPACE}:/workspace `
                    -w /workspace `
                    python:3.11-slim `
                    powershell -Command \"
                        pip install bandit; `
                        bandit -r app/ -f json -o bandit-report.json; `
                        bandit -r app/
                    \"
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Construction de l image Docker...'
                powershell 'docker build -t devsecops-app:latest .'
            }
        }

        stage('DAST - OWASP ZAP Pentest') {
            steps {
                echo 'Lancement du pentest dynamique avec OWASP ZAP...'
                powershell """
                docker run -d `
                    --name target-app `
                    --network ${DOCKER_NET} `
                    -p ${APP_PORT}:5000 `
                    devsecops-app:latest
                Start-Sleep -Seconds 5
                """
                powershell """
                docker run --rm `
                    --network ${DOCKER_NET} `
                    -v ${WORKSPACE}:/zap/wrk `
                    ghcr.io/zaproxy/zaproxy:stable `
                    zap-baseline.py `
                    -t http://target-app:5000 `
                    -r zap-report.html `
                    -J zap-report.json `
                    -I
                """
            }
            post {
                always {
                    powershell 'docker stop target-app; docker rm target-app'
                    publishHTML([
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
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
        success {
            echo 'Pipeline terminé ! Consulte les rapports de sécurité. ✅'
        }
        failure {
            echo 'Pipeline échoué. Regarde les logs pour plus de détails. ❌'
        }
    }
}
// Jenkinsfile DevSecOps Pipeline optimisé
pipeline {
    agent any
    environment {
        APP_PORT = '5000'
        ZAP_PORT = '8090'
        DOCKER_NET = 'devsecops-lab'
        APP_IMAGE = 'devsecops-app:latest'
    }

    stages {
        // ── STAGE 1 : Checkout ──
        stage('Checkout') {
            steps {
                echo 'Récupération du code source...'
                checkout scm
            }
        }

        // ── STAGE 2 : Build Docker image complète ──
        stage('Docker Build') {
            steps {
                echo 'Construction de l image Docker complète (app + dépendances)...'
                script {
                    def cmd = isUnix() ? 'sh' : 'bat'
                    "${cmd}" "docker build -t ${APP_IMAGE} ."
                }
            }
        }

        // ── STAGE 3 : Tests unitaires avec pytest ──
        stage('Unit Tests') {
            steps {
                echo 'Exécution des tests unitaires avec pytest...'
                script {
                    def cmd = isUnix() ? 'sh' : 'bat'
                    "${cmd}" """
                    docker run --rm -v ${env.WORKSPACE}:/app -w /app ${APP_IMAGE} pytest tests/ -v
                    """
                }
            }
        }

        // ── STAGE 4 : SAST avec Bandit ──
        stage('SAST - Bandit Security Scan') {
            steps {
                echo 'Analyse de sécurité statique (Bandit)...'
                script {
                    def cmd = isUnix() ? 'sh' : 'bat'
                    "${cmd}" """
                    docker run --rm -v ${env.WORKSPACE}:/app -w /app ${APP_IMAGE} bandit -r app/ -f json -o bandit-report.json || true
                    docker run --rm -v ${env.WORKSPACE}:/app -w /app ${APP_IMAGE} bandit -r app/ || true
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }

        // ── STAGE 5 : DAST avec OWASP ZAP ──
        stage('DAST - OWASP ZAP Pentest') {
            steps {
                echo 'Lancement du pentest dynamique avec OWASP ZAP...'
                script {
                    def cmd = isUnix() ? 'sh' : 'bat'

                    // Démarrer l'application cible
                    "${cmd}" """
                    docker run -d --name target-app --network ${DOCKER_NET} -p ${APP_PORT}:5000 ${APP_IMAGE}
                    sleep 5
                    """

                    // Lancer ZAP Baseline Scan
                    "${cmd}" """
                    docker run --rm --network ${DOCKER_NET} -v ${env.WORKSPACE}:/zap/wrk ghcr.io/zaproxy/zaproxy:stable \\
                    zap-baseline.py -t http://target-app:5000 -r zap-report.html -J zap-report.json -I
                    """
                }
            }
            post {
                always {
                    script {
                        def stopCmd = isUnix() ? 'sh' : 'bat'
                        "${stopCmd}" 'docker stop target-app || true'
                        "${stopCmd}" 'docker rm target-app || true'
                    }
                    // Publier les rapports
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
        success {
            echo 'Pipeline terminé ! Consulte les rapports de sécurité.'
        }
        failure {
            echo 'Pipeline échoué. Vérifie les logs pour plus de détails.'
        }
    }
}
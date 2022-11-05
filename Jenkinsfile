pipeline {
	agent any
	stages {

		stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP-Dependency-Check'
			}
		}

		stage('Build') {
			steps {
				script {
					 sh 'python -m venv venv' 
					 sh 'pip install -r requirements.txt'
				}
			}
		}

		stage('Test') {
			steps {
				script {
					 sh 'python tests.py' 
				}
			}
		}
	}	
	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
}

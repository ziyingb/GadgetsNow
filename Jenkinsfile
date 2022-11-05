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
					echo ('Building...')
					sh '''
					python -m venv venv
					pip install -r requirement.txt
					'''
				}
			}
		}

		stage('Test') {
			steps {
				script {
					echo 'Testing...'
				}
			}
			post {
				always {junit 'test-reports/*.xml'}
			}
		}
	}	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
}

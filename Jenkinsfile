pipeline {
	agent any
	stages {
		stage('Build') {
			
			steps {
				sh 'echo "building the repo"'
				sh 'python3 -m venv venv'
				sh '. venv/bin/activate'
				sh 'pip install -r requirements.txt'
				git branch: 'main', url: 'https://github.com/ziyingb/GadgetsNow.git'
			}
		}

		stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP-Dependency-Check'
			}
		}

		stage('Test') {
			steps {
				script {
					 sh 'python3 tests.py' 
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

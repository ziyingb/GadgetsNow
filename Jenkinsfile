pipeline {
	agent any
	stages {
		stage('Checkout SCM') {
			steps {
				git 'https://github.com/ziyingb/GadgetsNow.git'
			}
		}

		stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
				dependencyCheck additionalArguments: 'scan="https://github.com/ziyingb/GadgetsNow.git" --formatHTML --formatXML', odcInstallation: 'OWASP-Dependency-Check'
			}
		}
	}	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
}

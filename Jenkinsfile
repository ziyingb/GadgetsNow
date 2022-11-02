pipeline {
	agent any
	stages {

		stage('OWASP DependencyCheck') {
			steps {
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

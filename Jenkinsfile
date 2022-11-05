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
					echo 'Building...'
					sh '''
					python -m venv venv
					pip install -r requirements.txt
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
				always {
					junit 'test-reports/*.xml'
				}
			}
		}	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
}

pipeline {
  agent any
  stages {
  stage('Build') {
        steps {
          script {
            echo 'Building...'
            try{ 
              //Killing previous gunicorn instance
              sh "kill cat gunicorn.pid"
            } catch (Exception e) {
              echo 'No Previous Gunicorn Instance'
            }
            
            sh '''
          #!/bin/bash 
          python3 -m venv jenkinsenv
          pip install -r requirements.txt
            '''
          }
        }
   }
    stage('OWASP DependencyCheck') {
      steps {
             dependencyCheck additionalArguments: ' --format HTML --format XML --enableExperimental', odcInstallation: 'Dependency Check'
                     dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
      }
    }
      stage('Test') {
     steps {
        script{
          echo 'Testing...'          
        }
     }
     post {
      always {junit 'test-reports/*.xml'}
     }
   }
    
    
    
  }  

}
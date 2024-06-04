pipeline {
  agent any
  stages {
    stage('Check out code') {
      steps {
        git(url: 'https://github.com/jazzpujols34/build-an-interview-bot-with-aoai', branch: 'main')
      }
    }

    stage('Log') {
      steps {
        sh 'ls -la'
      }
    }

    stage('Build') {
      steps {
        sh 'docker build -f frontend_recorder/Dockerfile .'
      }
    }

  }
}
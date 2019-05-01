node {
    properties([
        [$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator', artifactDaysToKeepStr: '', artifactNumToKeepStr: '2', daysToKeepStr: '', numToKeepStr: '2']]
    ])

    stage 'checkout'
    checkout scm

    stage 'tests'


    stage 'build docker'
      sh "docker build -t translate-bot:${env.BUILD_NUMBER} ."
      sh "docker tag translate-bot:${env.BUILD_NUMBER}"
}

pipeline {
    agent { dockerfile true }
    parameters {
        booleanParam(name: 'MIDNIGHT', defaultValue: false)
        booleanParam(name: 'NOON', defaultValue: false)
    }
    triggers {
        parameterizedCron('''
            TZ=Asia/Seoul
            00 0 * * * %MIDNIGHT=true;
            00 12 * * * %NOON=true
        ''')
    }
    stages {
        stage('Update DB') {
            when {
                expression { params.MIDNIGHT }
            }
            steps {
                sh 'python update_db_command.py'
            }
        }
        stage('Send mail to receivers') {
            when {
                expression { params.NOON }
            }
            steps {
                sh 'python send_link_command.py'
            }
        }
    }
}

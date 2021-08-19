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
        stage('Update days to close') {
            when {
                expression { params.MIDNIGHT }
            }
            steps {
                sh 'python update_days_to_close.py'
            }
        }
        stage('Send mail to receivers') {
            when {
                expression { params.NOON }
            }
            steps {
                sh 'python send_link_to_receivers.py'
            }
        }
    }
}

PASSWORD='alpine'
IP='127.0.0.1'
PORT='2222'
USER='root'

sshpass -p "alpine" ssh -p $PORT $USER@$IP "mkdir tmp"
sshpass -p "alpine" ssh -p $PORT $USER@$IP "mkdir tmp/log/"

sshpass -p "alpine" scp -P $PORT "$(dirname "$0")/run.sh" $USER@$IP:~/tmp/
sshpass -p "alpine" ssh -p $PORT $USER@$IP "chmod +x tmp/run.sh"
sshpass -p "alpine" scp -P $PORT "$(dirname "$0")/print.sh" $USER@$IP:~/tmp/
sshpass -p "alpine" ssh -p $PORT $USER@$IP "chmod +x tmp/print.sh"
sshpass -p "alpine" ssh -p $PORT $USER@$IP "bash tmp/run.sh & bash tmp/print.sh &"
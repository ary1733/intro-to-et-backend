cd ~/btp-backend-flask
tmux kill-server

tmux new-session -d -s  mtp_server
tmux send-keys -t  mtp_server 'cd ~/btp-backend-flask' Enter 'source ./venv/bin/activate' Enter
tmux send-keys -t  mtp_server 'git pull' Enter
tmux send-keys -t  mtp_server 'python3 app.py' Enter

tmux new-session -d -s  mtp_ngrok
tmux send-keys -t  mtp_ngrok 'ngrok http --domain=united-crawdad-thankfully.ngrok-free.app 8080' Enter
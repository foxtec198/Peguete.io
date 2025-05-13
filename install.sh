sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv autoconf libtool pkg-config zlib1g-dev cmake libffi-dev libssl-dev
echo "export PATH=$PATH:~/.local/bin/" >> ~/.bashrc
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
echo "Instalado com sucesso!"
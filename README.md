# gitllama

A github repo reader powered by llm.

## setup

```shell
# create a new env 
conda create --name gitllama
conda activate gitllama
conda install pip

# python server
cd ./backend
pip install -r ./requirements.txt

# web server 
cd .. # if you cd into llm-server
cd ./web

# node version >= 18
pnpm i
```

## Dev

```shell
chmod +x ./serverx.sh
chmod +x ./webx.sh

# split two terminal 
./serverx.sh
./webx.sh
```

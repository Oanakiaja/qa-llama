# gitllama

A github repo reader powered by llm.

## setup

### python env

```shell
# create a new env 
conda create --name gitllama
conda activate gitllama
conda install pip
```

### backend (fastapi)

```shell
# python server
cd ./backend
pip install -r ./requirements.txt
```

### llm (ollama & llama3)

```shell
# ollama & llama3
# ! ollama is downloaded from https://ollama.com/
ollama pull llama3
```

### web (nextjs)

```shell
# web server 
cd .. # if you cd into llm-server
cd ./web
# node version >= 18
pnpm i
```

## Dev

LLM Server

``` shell
# run ollama server
```

Backend

```shell
conda activate gitllama
./serverx.sh
```

WebServer

```shell
./webx.sh
```

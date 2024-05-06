# gitllama

> but now it's a  Q&A **local** program powered by `ollama` `llama3` `chromadb`.

A github repo reader powered by llm. (wip)

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

### LLM Server

``` shell
# run ollama server
```

### Backend

```shell
conda activate gitllama
./serverx.sh
```

### WebServer

```shell
./webx.sh
```

## TODO

### chat 基本功能

- [ ] 自定义chain
- [ ] 自定义 stream 输出
- [ ] 实现答案 References ，提供相关文档链接
- [ ] 实现会话 和 连续提问

### git 功能

- [ ] 实现拉取仓库作为上下文（ 区分各种 格式文件 readme）

### ci/cd

- [ ] 提供 docker 部署

### experience

- [ ] http2/3
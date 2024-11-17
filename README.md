# Building a Voice-Interactive Chatbot with STT, TTS, and Local LLMs
We are building a voice-interactive chatbot that leverages cutting-edge technologies such as Speech-to-Text (STT), Text-to-Speech (TTS), and local Large Language Models (LLMs), with a focus on Ollama's local LLM capabilities. This system will enable real-time conversations with users through a privately deployed, Dockerized setup, making it a versatile and secure solution for various applications. We hope the system has the following features:

#### 1. Speech-to-Text (STT) Module:
- Implement a high-efficiency speech recognition system to convert user voice input into text in real-time.
- Multilingual support is a significant plus!
#### 2. Text-to-Speech (TTS) Module:
- Integrate a natural and smooth TTS system that converts chatbot text responses into voice.
- Prioritize support for multiple languages, especially Chinese and English, with a focus on natural and emotionally responsive outputs.

#### 3.Local LLM (Ollama):
- Deploy a local LLM using Ollama to understand and generate text responses based on user voice input.
- Ensure the model operates efficiently with fast response times suitable for real-time voice interactions.
- Support context retention for understanding the logical flow of continuous conversations.

#### 4.User Interaction:

- Implement button-triggered voice input and termination, allowing users to easily control the start and end of conversations.
- Minimize latency in voice input and output to ensure a smooth interaction experience.


## Local Ollama 

First of all we need install [Jetson Container](https://github.com/dusty-nv/jetson-containers "Jetson Container") by going through the bellow codes and Refer to the [System Setup](https://github.com/dusty-nv/jetson-containers/blob/master/docs/setup.md "System Setup") page for tips about setting up your Docker daemon and memory/storage tuning.

    # install the container tools
    git clone https://github.com/dusty-nv/jetson-containers
    bash jetson-containers/install.sh

After installing Jetson Container you can use pull ollama docker and simply create a ollama microservice in order to access the LLM models on Ollama library. you can use SLM for first try to download smaller model to test the configs.

     jetson-containers run --name ollama $(autotag ollama)
	 ollama run llama3.2:1b
    

Here I used llama3.2:1b for testing the workflow Ollama supports a list of models available on [ollama.com/library](https://ollama.com/library 'ollama model library')

Here are some example models that can be downloaded:

| Model              | Parameters | Size  | Download                         |
| ------------------ | ---------- | ----- | -------------------------------- |
| Llama 3.2          | 3B         | 2.0GB | `ollama run llama3.2`            |
| Llama 3.2          | 1B         | 1.3GB | `ollama run llama3.2:1b`         |
| Llama 3.2 Vision   | 11B        | 7.9GB | `ollama run llama3.2-vision`     |
| Llama 3.2 Vision   | 90B        | 55GB  | `ollama run llama3.2-vision:90b` |
| Llama 3.1          | 8B         | 4.7GB | `ollama run llama3.1`            |
| Llama 3.1          | 70B        | 40GB  | `ollama run llama3.1:70b`        |
| Llama 3.1          | 405B       | 231GB | `ollama run llama3.1:405b`       |
| Phi 3 Mini         | 3.8B       | 2.3GB | `ollama run phi3`                |
| Phi 3 Medium       | 14B        | 7.9GB | `ollama run phi3:medium`         |
| Gemma 2            | 2B         | 1.6GB | `ollama run gemma2:2b`           |
| Gemma 2            | 9B         | 5.5GB | `ollama run gemma2`              |
| Gemma 2            | 27B        | 16GB  | `ollama run gemma2:27b`          |
| Mistral            | 7B         | 4.1GB | `ollama run mistral`             |
| Moondream 2        | 1.4B       | 829MB | `ollama run moondream`           |
| Neural Chat        | 7B         | 4.1GB | `ollama run neural-chat`         |
| Starling           | 7B         | 4.1GB | `ollama run starling-lm`         |
| Code Llama         | 7B         | 3.8GB | `ollama run codellama`           |
| Llama 2 Uncensored | 7B         | 3.8GB | `ollama run llama2-uncensored`   |
| LLaVA              | 7B         | 4.5GB | `ollama run llava`               |
| Solar              | 10.7B      | 6.1GB | `ollama run solar`               |

by running above code you can chat on terminal with a local LLM or SLM. If you are working with Nvidia Jetson AGX you can use bigger LLM but if you are using other Jetson modules you can use smaller models.
running jetson-container starts ollama server and now you can use ollama_run.py code or if you want you can modify it in python coding.
![ran ollama in terminal](https://github.com/kouroshkarimi/local_chatbot_jetson/blob/main/Files/terminal_ollama.gif)


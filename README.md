# Building a Voice-Interactive Chatbot with STT, TTS, and Local LLMs

We are building a voice-interactive chatbot that leverages cutting-edge technologies such as Speech-to-Text (STT), Text-to-Speech (TTS), and local Large Language Models (LLMs), with a focus on Ollama's local LLM capabilities. This system will enable real-time conversations with users through a privately deployed, Dockerized setup, making it a versatile and secure solution for various applications. We hope the system has the following features:

#### 1\. Speech\-to\-Text \(STT\) Module:

* Implement a high-efficiency speech recognition system to convert user voice input into text in real-time.
* Multilingual support is a significant plus!

#### 2\. Text\-to\-Speech \(TTS\) Module:

* Integrate a natural and smooth TTS system that converts chatbot text responses into voice.
* Prioritize support for multiple languages, especially Chinese and English, with a focus on natural and emotionally responsive outputs.

#### 3.Local LLM (Ollama):

* Deploy a local LLM using Ollama to understand and generate text responses based on user voice input.
* Ensure the model operates efficiently with fast response times suitable for real-time voice interactions.
* Support context retention for understanding the logical flow of continuous conversations.

#### 4.User Interaction:

* Implement button-triggered voice input and termination, allowing users to easily control the start and end of conversations.
* Minimize latency in voice input and output to ensure a smooth interaction experience.

## Local Ollama

First of all we need install [Jetson Container](https://github.com/dusty-nv/jetson-containers "Jetson Container") by going through the bellow codes and Refer to the [System Setup](https://github.com/dusty-nv/jetson-containers/blob/master/docs/setup.md "System Setup") page for tips about setting up your Docker daemon and memory/storage tuning.

```
# install the container tools
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh
```

After installing Jetson Container you can use pull ollama docker and simply create a ollama microservice in order to access the LLM models on Ollama library. you can use SLM for first try to download smaller model to test the configs.

```
 jetson-containers run --name ollama $(autotag ollama)
 ollama run llama3.2:1b
```

Here I used llama3.2:1b for testing the workflow Ollama supports a list of models available on [ollama.com/library](https://ollama.com/library "ollama model library")

Here are some example models that can be downloaded:

| Model | Parameters | Size | Download |
| ----- | ---------- | ---- | -------- |
| Llama 3.2 | 3B | 2.0GB | `ollama run llama3.2` |
| Llama 3.2 | 1B | 1.3GB | `ollama run llama3.2:1b` |
| Llama 3.2 Vision | 11B | 7.9GB | `ollama run llama3.2-vision` |
| Llama 3.2 Vision | 90B | 55GB | `ollama run llama3.2-vision:90b` |
| Llama 3.1 | 8B | 4.7GB | `ollama run llama3.1` |
| Llama 3.1 | 70B | 40GB | `ollama run llama3.1:70b` |
| Llama 3.1 | 405B | 231GB | `ollama run llama3.1:405b` |
| Phi 3 Mini | 3.8B | 2.3GB | `ollama run phi3` |
| Phi 3 Medium | 14B | 7.9GB | `ollama run phi3:medium` |
| Gemma 2 | 2B | 1.6GB | `ollama run gemma2:2b` |
| Gemma 2 | 9B | 5.5GB | `ollama run gemma2` |
| Gemma 2 | 27B | 16GB | `ollama run gemma2:27b` |
| Mistral | 7B | 4.1GB | `ollama run mistral` |
| Moondream 2 | 1.4B | 829MB | `ollama run moondream` |
| Neural Chat | 7B | 4.1GB | `ollama run neural-chat` |
| Starling | 7B | 4.1GB | `ollama run starling-lm` |
| Code Llama | 7B | 3.8GB | `ollama run codellama` |
| Llama 2 Uncensored | 7B | 3.8GB | `ollama run llama2-uncensored` |
| LLaVA | 7B | 4.5GB | `ollama run llava` |
| Solar | 10.7B | 6.1GB | `ollama run solar` |

by running above code you can chat on terminal with a local LLM or SLM. If you are working with Nvidia Jetson AGX you can use bigger LLM but if you are using other Jetson modules you can use smaller models.
running jetson-container starts ollama server and now you can use ollama\_run.py code or if you want you can modify it in python coding.

Run ollama in terminal:
<img src="https://github.com/kouroshkarimi/local_chatbot_jetson/blob/main/Files/terminal_ollama.gif" alt="Description of GIF" width="700">
Run ollama in python with script ollama\_run.py. be aware for accessing the ollama server run it with jetson-container.
<img src="https://github.com/kouroshkarimi/local_chatbot_jetson/blob/main/Files/ollama_python.gif" alt="Description of GIF" width="700">

## TTS and STT with Riva Server
In order to creating a chatbot we need to convert the  users voice into text that the we can feed it to model and after model inference the output turn the created text back to voice. So we need Automated Speech Recognition and Text To Speech (TTS) modules. 
NVIDIA® Riva is a set of GPU-accelerated multilingual speech and translation microservices for building fully customizable, real-time conversational AI pipelines. Riva includes automatic speech recognition (ASR), text-to-speech (TTS), and neural machine translation (NMT) and is deployable in all clouds, in data centers, at the edge, and on embedded devices.
### Riva Installation

------------

Please refer [here](https://docs.nvidia.com/deeplearning/riva/user-guide/docs/quick-start-guide.html#embedded "here") for more detailed information.
1. Create Nvidia NGC API key:
First of all you need NGC API that you can acquere it by logging in and create one in [Nvidia NGC ](https://catalog.ngc.nvidia.com/collections?filters=&orderBy=weightPopularDESC&query=&page=&pageSize= "Nvidia NGC ")website. after creating it save it somewhere in your laptop.
2. Configure NGC on Jetson:
Now you have NGC key to have access to the services provided by the Nvidia NGC. for configure it in the Jetson execute the below commands on your terminal command line:
```
cd ~ && mkdir ngc_setup && cd ngc_setup
wget --content-disposition https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/3.36.0/files/ngccli_arm64.zip && unzip ngccli_arm64.zip 
chmod u+x ngc-cli/ngc
echo "export PATH=\"\$PATH:$(pwd)/ngc-cli\"" >> ~/.bash_profile && source ~/.bash_profile
ngc config set
```
Confige ngc with your API key and below information:
<img src="https://files.seeedstudio.com/wiki/reComputer/Application/Local_Voice_Chatbot/setup_riva_3.png" alt="Description of GIF" width="700">
with these commands NGC have setup in our Jetson and now we can use Riva services.
3. Install Riva on Jetson:
Riva needs access to NGC services and we have done those steps. now we are ready for install and run Riva on our reComputer. be aware i am working on Jetpack 6.0 and the compatible Riva version for this JP6 is 2.16.0. you can find your compatible Riva version in the its [Support Matrix](https://docs.nvidia.com/deeplearning/riva/user-guide/docs/support-matrix.html "Support Matrix").
Download the Riva with the following commands:
```
    cd ~ && mkdir riva_setup && cd riva_setup
    ngc registry resource download-version nvidia/riva/riva_quickstart_arm64:2.16.0
    cd riva_quickstart_v2.13.1
```
In the Riva folder you can see a config.sh file. based on your needs you can config it. in this project we just needs ASR and TTS so we disable other services in order to not download the models of other application and just download and configure services of ASR and TTS. So disable nlp and nmt in that config file:
```
service_enabled_nlp=true ==> service_enabled_nlp=false
service_enabled_nmt=true ==> service_enabled_nmt=false
```
Before go tho the next step be sure you have configured your nvidia container toolkit in default mode.It means change the file /etc/docker/daemon.json with below lines:
```
{   
    "default-runtime": "nvidia",
        "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```
restart the docker service:
```
sudo systemctl restart docker
```
now we are ready to pull the Riva container and run it in the reCopmuter. execute below code wait to pull and download the models and after that the Riva service is running over the system.
```
sudo bash riva_init.sh
sudo bash riva_start.sh
```























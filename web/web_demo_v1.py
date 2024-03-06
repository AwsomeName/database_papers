# coding=utf-8
# 这个做一个简单的API，一个简单的输入框，返回几个结果
import time
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM,  TextIteratorStreamer
from transformers import StoppingCriteria, StoppingCriteriaList
import streamlit as st
from streamlit_chat import message
from threading import Thread
from transformers.utils import logging
import torch
from transformers.generation.logits_process import LogitsProcessor
# from vllm import LLM

# import logging
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer, util

from api_translate import tran_en, tran_zh, tran_auto, tran_auto_2_zh
# from transformers.generation.utils import LogitsProcessorList, StoppingCriteriaList, GenerationConfig, ModelOutput

acc_token = "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"

logger = logging.get_logger(__name__)
st.set_page_config(
    page_title="bigcode/starcoder 演示",
    page_icon=":robot:"
)


# import logging
# logging.basicConfig(filename="es.log", level=logging.DEBUG)
cafile1 = "/etc/elasticsearch/certs/http_ca.crt"
# @st.cache_resource
es = Elasticsearch(hosts=["https://127.0.0.1:9200"], basic_auth=("elastic", "abc12345"), ca_certs=cafile1, verify_certs=True)
print("es_ping:", es.ping())
acc_token = "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"
sentences = ["auto generate prompt using gpt for special task"]
model = SentenceTransformer('all-MiniLM-L6-v2', use_auth_token=acc_token)

model_path = "/home/lc/models/codellama/CodeLlama-7b-Instruct-hf"

def es_emb_search(query):
    # embeddings = model.encode(sentences)[0]
    embeddings = model.encode(query)[0]

    res = es.knn_search(
        index = "paper_title_emb",
        source = ["title", "abstract"],
        knn = {
            "field": "ab_emb",
            "k": 3,
            "num_candidates": 4,
            "query_vector": embeddings
        }
    )

    title = [[x['_source'], x["_score"]]  for x in res['hits']['hits']] 
 
    items = []
    for item in title:
        print(item)
        items.append(item[0])
    # print("--------")
    res = es.knn_search(
        index = "paper_title_emb",
        source = ["title", "abstract"],
        knn = {
            "field": "title_emb",
            "k": 3,
            "num_candidates": 6,
            "query_vector": embeddings
        }
    )
    title = [[x['_source'], x["_score"]]  for x in res['hits']['hits']] 
    for item in title:
        # print(item)
        items.append(item[0])

    return items


@st.cache_resource
def get_model():
    logger.info("get tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side="left")
    tokenizer.pad_token = tokenizer.eos_token
    logger.info("get model...")
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", load_in_4bit=True)
    model = model.eval()
    streamer = TextIteratorStreamer(tokenizer)
    logger.info("init done")
    return tokenizer, model, streamer


MAX_TURNS = 20
MAX_BOXES = MAX_TURNS * 2

system_token = "<|system|>"
user_token = "<|user|>"
assistant_token = "<|assistant|>"
end_token = "<|end|>"

system_msg = "Below is a dialogue between a human and an AI assistant called StarChat."
system_msg = "Below are a series of dialogues between various people and an AI assistant.\
The AI tries to be helpful, polite, honest, sophisticated, emotionally aware, and humble-but-knowledgeable.\
The assistant is happy to help with almost anything, and will do its best to understand exactly what is needed.\
It also tries to avoid giving false or misleading information, and it caveats when it isn’t entirely sure about the right answer.\
That said, the assistant is practical and really does its best, and doesn’t let caution get too much in the way of being useful.\
-----\n"
system_msg = "根据下面搜索的结果，回复用户的答案"
system_msg = "Reply to the user_query based on the search_results below. "
system_msg = "Based on the search results below, briefly answer the user's questions"
system_msg = "read the paper's title, abstract. "

def predict(input, max_length, top_p, temperature, history=None):
    tokenizer, model, streamer = get_model()
    stop_token_ids = [tokenizer.eos_token_id, tokenizer(end_token)["input_ids"][0], tokenizer(user_token)["input_ids"][0]]
    class StopOnTokens(StoppingCriteria):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
            for stop_id in stop_token_ids:
                if input_ids[0][-1] == stop_id:
                    return True
            return False

    # if history is None:
    history = []

    with container:
        if len(history) > 0:
            if len(history)>MAX_BOXES:
                history = history[-MAX_TURNS:]
            for i, (query, response) in enumerate(history):
                message(query, avatar_style="big-smile", key=str(i) + "_user")
                message(response, avatar_style="bottts", key=str(i))

        message(input, avatar_style="big-smile", key=str(len(history)) + "_user")
        st.write("AI正在回复:")
        # input = "Human: " + input + "\n\n\nAssistant: "
        en_input = tran_auto(input)
        st.write(en_input + "\n")

        search_item = es_emb_search([en_input])
        print("==============================")
        print(search_item)
        search_str = ""
        for item in search_item:
            for key in item:
                st.write(item[key] + "\n")
                # time.sleep(1)
                # zh_ab = tran_en(item[key])
                # st.write(zh_ab + "\n")
                
        for item in search_item:
            for key in item:
                search_str += key
                # st.write("title: ", key + "\n")
                search_str += ": "
                search_str += item[key] + "。\n"
                # st.write("abstract: ", item[key] + "\n")
            break
                
        print("Len: ", len(search_str))
                
        
        with st.empty():
            # input = system_token + "\n" + system_msg + end_token + "\n" + user_token + "\nuser questions: " + input + "\n search results:" + search_str + end_token + "\n" + assistant_token + "\n"
            m_input = system_msg + "\n" + search_str + "\n Based on the above content, answer the user's questions below:  \n" + en_input + "\n "
            stop = StopOnTokens() 
            logger.info("input:---- \n" + m_input)
            chosen_token = tokenizer(
                m_input,
                # max_length=max_length,
                # padding="max_length",
                # truncation=True,
                return_tensors="pt"
            )
        
            input_ids = torch.tensor(chosen_token["input_ids"]).cuda()
            attention_mask = torch.tensor(chosen_token['attention_mask']).cuda()
            outputs = model.generate(
                    input_ids,
                    attention_mask=attention_mask,
                    # max_new_tokens=max_length,
                    max_length=max_length,
                    do_sample=True,
                    top_k = 50,
                    top_p=0.95,
                    num_beams = 3,
                    repetition_penalty = 1.5,
                    # temperature=0.2,
                    # temperature=temperature,
                    num_return_sequences=1,
                    stopping_criteria=StoppingCriteriaList([stop]))
            # outputs = model.generate(inputs)
            response = tokenizer.decode(outputs[0])    
            # response = response.replace("<|endoftext|>", "")
            # response = response.replace("<|end|>", "")
            # response = response.split("<|assistant|>")[-1]
            st.write("==================================\n")
            st.write(response + "\n")
            print("response:---- \n" + response)
            st.write("==================================\n")
            response = tran_auto_2_zh(response)
            print("response:---- \n" + response)
            st.write(response)

    return history


container = st.container()

# create a prompt text for the text generation
prompt_text = st.text_area(label="用户命令输入",
            height = 100,
            placeholder="请在这儿输入您的命令")

do_sample = st.sidebar.slider(
    "do_sample", 0, 1, 0, step=1
)

max_length = st.sidebar.slider(
    'max_length', 0, 4096, 2048, step=1
)
top_p = st.sidebar.slider(
    'top_p', 0.0, 1.0, 0.95, step=0.01
)
temperature = st.sidebar.slider(
    'temperature', 0.0, 1.0, 0.2, step=0.01
)

if 'state' not in st.session_state:
    st.session_state['state'] = []

if st.button("发送", key="predict"):
    with st.spinner("AI正在思考，请稍等........"):
        # text generation
        st.session_state["state"] = predict(prompt_text, max_length, top_p, temperature, st.session_state["state"])

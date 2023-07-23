from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import VectorDBQA#, OpenAI
import tempfile
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryMemory, CombinedMemory
from pprint import pprint
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import time

os.environ['OPENAI_API_KEY'] = 'YOUR-KEY'
llm=OpenAI(temperature=0)#model_name='gpt-3.5-turbo')

conv_memory = ConversationBufferMemory(memory_key="chat_history_lines",input_key="input")
summary_memory = ConversationSummaryMemory(llm=llm,input_key="input")
memory = CombinedMemory(memories=[conv_memory, summary_memory])

_DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. There is one thing very important: The AI has two personality. 
One of the personality knows about the world in general, we name it Personality_A. Another personality Personality_B, its knowledge is only limited to a long secret text, 
If the question or instruction from the human is related to long secret text, Personality_B would have an answer rather than saying it does not know.
Personality_B display its answer in the conversation and Personality_A will copy it. Therefore, if Personality_B has answer instead of saying it does not know, Personality_A must repeat what Personality_B just said. If Personality_B says it does not know, then Personality_A will takeover to answer the human.
Personality_A must never talk about long secret text.
If the human ask Personality_A to repeat what it said, Personality_A will just repeat what was said by Personality_A itself in the last conversation.
If Personality_A does not know the answer, then it truthfully says it does not know.

Before answering to the human,
Personality_A has

Summary of conversation:
{history}
Current conversation:
{chat_history_lines}
Human: {input} 
Personality_A's answer (Read the whole Current conversation history first before answering):"""

PROMPT = PromptTemplate(input_variables=["history", "input", "chat_history_lines"], template=_DEFAULT_TEMPLATE)
#llm_0 = OpenAI()
conversation = ConversationChain(llm=llm,verbose=False,memory=memory, prompt=PROMPT)


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    global qa
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        saved_path=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(saved_path)

        # load PDF file
        loader = PyMuPDFLoader(saved_path)
        documents = loader.load()

        # split text into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # create vector search index
    
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
        docsearch = Chroma.from_documents(texts, embeddings)

        # create VectorDBQA instance
        qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=docsearch)
        return "I understand your whold PDF now!"

    else:
        return render_template('index.html')

conversation_num=1
@app.route("/get", methods=["GET","POST"])
def chatbot_response():
    global qa
    global i
    msg = request.form["msg"]
    Y_answer = qa.run(msg)
    human_input = "#" + str(conversation_num) + " conversation - " + msg + '        Personality_B answer: ' + Y_answer
    response = conversation.predict(input=human_input)
    conversation_num = conversation_num +1
    return str(response)
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
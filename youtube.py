#First Step -saari libraries import karwayenge
import streamlit as st
from google import genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse,parse_qs

#second Step - Google k servers nk saath connection bnayenge
client=genai.Client(api_key=os.environ.get("Gemini Key here"))

#Third step- Web interface banyege streamlit k madad se(page k design)
st.set_page_config(page_title="Youtube Summarizer", page_icon="🎥")
st.title("Here comes your Youtube Video Summarizer")
st.markdown("***Your Personal youtube summarizer- summarize any youtube video*** ")

#Fouth Step - ab video k link lenge user se uske liye hum streamlit k text_input wala function use krenge
video_url=st.text_input("Paste your Youtube URL here")

#Fifth Step-ab hum video k link se video id nikalenge aur YoutubeTranscriptApi ko denge,
# yaad rakhna YoutubeTranscriptApi kewal video id hi accept krti hai URL's nhi 
# kyunki same video k URL's different types k ho skte hai but video id same video k same hi rhegi different url
# mai aur video id nikalne k liye hum python k inbuilt library urllib k istemal krenge 

if video_url:
    video_parts=urlparse(video_url)
    video_id=parse_qs(video_parts.query)["v"][0]
    
    #Sixth Step- ab video id k madad se YouTubeTranscriptApi youtube k server pr request kregi ,
    # woh request fetch krti hai
    
    fetcher = YouTubeTranscriptApi()
    transcript_data = fetcher.fetch(video_id, languages=["hi","en"])
    
    #Seventh Step- Jo transcript aayegi woh list k form mai aayegi jiske ander har ek element dictionary k form
    # mai hai. Ab transcript k ander do elements hai text aur start time. Humko text wala part chahiye. toh hum 
    #woh text nikalenge transcript mai se 
    
    transcript_text=" ".join([item.text for item in transcript_data])
    
    #Eighth step- ab iske baad yehi text hum gemini model ko bhejenge summarize krne k liye. uske liye humko 
    # gemini ko model ko batana pdega prompt dekr k tumko kis tarah se jawab dena hai. ismai humne jo step 2 mai
    # google k server k saath connection banaya tha woh istemal krenge jo ki humko google k server k saath connect krwayega.
    # uske baad generate_function request bhejega k mera pass jo contents woh apne is model se process krwakr jawab do
    
    system_prompt="Act like an expert in summarizing the content. Do not miss the important part and give whole context in simple , shorter words. Avoid jargons"
    
    response=client.models.generate_content(model="gemini-2.5-flash",contents=system_prompt + "\n\n" + transcript_text)
    st.markdown(response.text)
    
    #Ninth Step- ab hum chat history dikhe humko aur hum follow up question kr paaye summary niklne k baad woh feature hum add kr rhe hai 
    if "messages" not in st.session_state:#agr messages naam k string agr nhi hai session_state k ander
        st.session_state.messages=[] #toh ek key bnao messages naam k jo ki ek list create krta hai empty
        
    for message in st.session_state.messages: # yahan for loop chala ek ek krkr jo messages key mai chize hai woh message variable k ander store hoga
        with st.chat_message(message["role"]): #st.chat_message appka ek chat bubble banayega aur with aapka container bnayega jismai content store ho skta hai , message["role"] se aapka role k value nikalkr aayegi
            st.markdown(message["content"])   # yahan aapka content key mai jo value hai woh screen pr print ho jayegi
            
    user_question=st.chat_input("Ask a question about a video") # iss line se hum user k input lenge  
    
    if user_question: #agr user ne input diya 
        with st.chat_message("user"): #user k chat bubble bnega aur uska container bhi
            st.markdown(user_question) #user k input user wale bubble pr print hoga aur screen pr dikhega
          
        st.session_state.messages.append({
            "role":"user",  #messages wali key mai "role":"user" store ho jayega
            "content":user_question #similarly content key mai user k input store ho jayega
        })
        response2=client.models.generate_content( # client jo hai woh google k server k saath connection banaya hai. toh basically mtlb hai uss server mai jo model hai usse content generate krwana hai yeh line k mtlb hai
            model="gemini-2.5-flash", #model k naam specify kiya hai -iss model se content nikalwao
            contents=system_prompt + "\n\n" + transcript_text + "\n\nUser Question: " + user_question # #contents wali chiz model k pass jayegi aur usko batyegi k tumko kiss tarah act krkr jawab dena , kiska jawab dena aur kis mai se jawab dena hai aur \n\n se — System prompt ← alag section ,Transcript    ← alag section  ,User Question ← alag section ,Gemini clearly samajhta hai — kya role hai, kya content hai, kya sawaal hai! 
        )
        with st.chat_message("assistant"): #ab assistant wala chat bubble container bnega
            st.markdown(response2.text) #jo gemini k response aayega usmai text wala part nikalo
            
        st.session_state.messages.append({
            "role":"assistant", #yeh wala part as it is store hoga messages wali key k ander
            "content":response2.text #yeh wala part mai joh gemini se response aaya woh store content wali key k ander and content wali messages wali key k ander store hoga
        })
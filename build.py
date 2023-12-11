import re
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import openai


# Khởi tạo ChatGPT API key
openai.api_key = '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'

# Khởi tạo chatbot
chatbot = ChatBot('MyChatBot')

# Khởi tạo trainer và train chatbot với dữ liệu tiếng Anh mặc định
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Hàm gửi câu hỏi và nhận câu trả lời từ ChatGPT
def get_chatgpt_response(question):
    response = openai.Completion.create(
        engine='davinci-codex',
        prompt=question,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Hàm xử lý câu hỏi và trả lời từ chatbot
def get_chatbot_response(question):
    chatgpt_response = get_chatgpt_response(question)
    response = chatbot.get_response(question).text

    if chatgpt_response:
        # So sánh độ tương đồng giữa câu trả lời từ ChatGPT và câu trả lời từ chatbot
        similarity = similarity_score(response, chatgpt_response)
        if similarity < 0.7:
            response = chatgpt_response

    return response

# Hàm tính độ tương đồng giữa hai câu
def similarity_score(sentence1, sentence2):
    # Đưa về lowercase và xóa các ký tự đặc biệt
    sentence1 = sentence1.lower().replace('[^a-zA-Z0-9]', '')
    sentence2 = sentence2.lower().replace('[^a-zA-Z0-9]', '')

    # Tính độ tương đồng dựa trên số từ giống nhau
    words1 = set(sentence1.split())
    words2 = set(sentence2.split())
    similarity = len(words1 & words2) / float(len(words1 | words2))

    return similarity

# Hàm chạy chatbot
def run_chatbot():
    print("Chatbot: Xin chào! Hãy nhập câu hỏi của bạn hoặc gõ 'exit' để thoát.")
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() == 'exit':
            break

        response = get_chatbot_response(user_input)
        print("Chatbot:", response)

# Chạy chatbot
run_chatbot()

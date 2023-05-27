import os
import openai
openai.api_key = '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'

def friend_chat(all_text,prompt0,call_name = '我妻ゆの'):
  start_sequence = '\n'+str(call_name)+':'
  restart_sequence = "\nYou: "
  all_text = all_text + restart_sequence
  if prompt0 == '':
     prompt0 = input(restart_sequence) #当期prompt
  if prompt0 == 'quit':
     return prompt0
  prompt = all_text + prompt0 + start_sequence


  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    stop=["\nYou:"]
  )
  audio_text = response['choices'][0]['text'].strip()
  print(start_sequence + response['choices'][0]['text'].strip())
  all_text = prompt + response['choices'][0]['text'].strip()
  return prompt0,all_text,audio_text

if __name__ == '__main__':
  all_text = input('输入初始设定文本:')
  while 1 == 1:
    resualt,all_text,audio_text = friend_chat("",'')
    # print(all_text)
    if resualt == 'quit':
      break
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
import os
from openai import OpenAI
import time
from typing import Any
from AudioRecorder import play_audio


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))   

assitant_id = 'asst_T1eE49A0qoSU8oBlHqgM5URb'
the_nurse = client.beta.assistants.retrieve(assitant_id)

thread = client.beta.threads.create()

speech_file_path = Path(__file__).parent / "speech.mp3"

def get_response(current_thread: Any, message: str) -> str:
    """ Gets a response from the assistant given a message
    """
    message_obj = client.beta.threads.messages.create(
        thread_id=current_thread.id,
        role="user",
        content=message
    )
    run = client.beta.threads.runs.create(
        thread_id=current_thread.id,
        assistant_id=the_nurse.id,
    )
    while run.status == "queued" or run.status == 'in_progress':
        time.sleep(5)
        run = client.beta.threads.runs.retrieve(
            thread_id=current_thread.id,
            run_id=run.id
        )
    thread_messages = client.beta.threads.messages.list(current_thread.id)
    return thread_messages.data[0].content[0].text.value

def have_full_conversation() -> str:
    output = ""
    while not ("question_all_finished"  in output or "summary" in output) or "?" in output:
        userText = input('Write your message: ')
        output = get_response(thread, userText)
        if "question_all_finished" not in output:
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=output
            )
            response.stream_to_file(speech_file_path)
            play_audio('speech.mp3')
    return output


if __name__ == '__main__':
    analysis = have_full_conversation()
    print(f"Here is the full analysis: \n \n {analysis}")


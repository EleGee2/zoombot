import asyncio
import time
import subprocess
import os

import pyautogui
import pyaudio
import cv2

from dotenv import load_dotenv

load_dotenv()


async def joinMeeting(meeting_id, password):
    # Open up the Zoom app
    subprocess.call(os.getenv('PATH_TO_ZOOM_EXE'))

    time.sleep(10)

    # clicks the join button
    join_button = pyautogui.locateCenterOnScreen('join_button.png')
    pyautogui.moveTo(join_button)
    pyautogui.click()

    # Type the meeting ID
    meeting_id_button = pyautogui.locateCenterOnScreen('meeting_id.png')
    pyautogui.moveTo(meeting_id_button)
    pyautogui.click()
    pyautogui.write(meeting_id)

    # Disables both the camera and the mic
    media_buttons = pyautogui.locateAllOnScreen('media_btn.png')
    for button in media_buttons:
        pyautogui.moveTo(button)
        pyautogui.click()
        time.sleep(2)

    # Hits the join button
    join_button = pyautogui.locateCenterOnScreen('join_btn.png')
    pyautogui.moveTo(join_button)
    pyautogui.click()
    time.sleep(9)

    # Types the password and hit enter
    meeting_pswd_btn = pyautogui.locateCenterOnScreen('meeting_pswd.png')
    pyautogui.moveTo(meeting_pswd_btn)
    pyautogui.click()
    time.sleep(9)
    pyautogui.write(password)
    pyautogui.press('enter')


async def capture_audio_video_streams():
    audio = pyaudio.PyAudio()
    audio_streams = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    video_streams = cv2.VideoCapture(0)
    video_streams.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_streams.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("video.mp4", fourcc, 30.0, (640, 480))

    audio_writer = open("audio.wav", "wb")

    while True:
        # Read a chunk of audio from the audio stream
        audio_data = audio_streams.read(1024)
        audio_writer.write(audio_data)

        # Read a from the video stream
        ret, frame = video_streams.read()
        video_writer.write(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_writer.release()
    audio_writer.close()
    audio_streams.stop_stream()
    audio_streams.close()
    audio.terminate()
    video_streams.release()
    cv2.destroyAllWindows()


async def main():
    # Join the created meeting
    meeting_id = input('Input meeting ID:')
    password = input('Password:')

    # Join the Zoom meeting
    await joinMeeting(meeting_id, password)

    # Capture the audio and video streams
    await capture_audio_video_streams()


# Call the main function
if __name__ == "__main__":
    asyncio.run(main())

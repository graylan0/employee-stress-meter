import tkinter as tk
import pennylane as qml
from pennylane import numpy as np
import openai
import speech_recognition as sr
from textblob import TextBlob
from datetime import datetime, timedelta
import re
import asyncio
import json

openai.api_key = 'YOUR_OPENAI_API_KEY'

class ChromaticQuantumZonesClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chromatic Quantum Zones Clock")
        self.geometry("800x600")
        self.voice_to_text_label = self.create_label("", ("Helvetica", 14))
        self.breaktime_label = self.create_label("Next Break: --:--", ("Helvetica", 14))
        self.chromatic_guide_label = self.create_label("Chromatic Guide: Loading...", ("Helvetica", 12))
        self.active_zone_label = self.create_label("Active Zone Color: Loading...", ("Helvetica", 12))
        self.voice_to_text_status = False
        self.last_break_time = datetime.now()
        self.zone_colors = {
            "Employee Active Zone": "#FFFFFF",
            "Employee Wind Down": "#ADD8E6",
            "Employee Clock Out Zone": "#90EE90"
        }
        self.update_clock()
        self.load_and_process_conversations()

    def create_label(self, text, font):
        label = tk.Label(self, text=text, font=font)
        label.pack()
        return label

    def update_clock(self):
        self.update_quantum_state()
        self.update_voice_to_text()
        self.update_breaktime()
        self.after(1000, self.update_clock)

    def update_quantum_state(self):
        try:
            current_time = datetime.now()
            self.current_time_param = (current_time.hour + current_time.minute / 60) * np.pi / 12
            asyncio.run(self.generate_emotion_data("happy", "task1", "task2", "task3"))
        except Exception as e:
            print(f"Error updating quantum state: {e}")

    async def generate_emotion_data(self, emotion, task1_label, task2_label, task3_label):
        task1_prompt = f"Please generate an HTML color code that best represents the emotion: {emotion}."
        task1_response = openai.ChatCompletion.create(
            model="gpt-4.0-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": task1_prompt}
            ]
        )
        color_code = re.search(r'#[0-9a-fA-F]{6}', task1_response.choices[0].message['content'])
        amplitude = None
        if color_code:
            amplitude = self.sentiment_to_amplitude(emotion)
        if color_code:
            quantum_state = self.quantum_circuit(color_code.group(0), amplitude).numpy()
        else:
            quantum_state = None
        self.update_chromatic_guide(quantum_state)

    def quantum_circuit(self, color_code, amplitude):
        qml_model = qml.device("default.qubit", wires=4)
        @qml.qnode(qml_model)
        def circuit(color_code, amplitude):
            r, g, b = [int(color_code[i:i+2], 16) for i in (1, 3, 5)]
            r, g, b = r / 255.0, g / 255.0, b / 255.0
            qml.RY(r * np.pi, wires=0)
            qml.RY(g * np.pi, wires=1)
            qml.RY(b * np.pi, wires=2)
            qml.RY(amplitude * np.pi, wires=3)
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            qml.CNOT(wires=[2, 3])
            return qml.state()
        return circuit(color_code, amplitude)
      
    def sentiment_to_amplitude(self, text):
        analysis = TextBlob(text)
        return (analysis.sentiment.polarity + 1) / 2

    def update_chromatic_guide(self, quantum_state):
        if quantum_state < -0.33:
            color = "Red"
        elif -0.33 <= quantum_state <= 0.33:
            color = "Yellow"
        else:
            color = "Green"
        self.chromatic_guide_label.config(text=f"Chromatic State: {color}")

    def update_breaktime(self):
        current_time = datetime.now()
        hours_since_last_break = (current_time - self.last_break_time).total_seconds() / 3600
        if hours_since_last_break >= 2:
            self.last_break_time = current_time
            next_break_time = current_time + timedelta(hours=1)
            self.breaktime_label.config(text=f"Next Break: {next_break_time.strftime('%H:%M')}")

    def update_voice_to_text(self):
        if not self.voice_to_text_status:
            self.capture_and_analyze_voice()

    def capture_and_analyze_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                self.voice_to_text_label.config(text=f"Voice to Text: {text}")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Error making the request: {e}")

    def load_and_process_conversations(self):
        try:
            with open('employee.json', 'r') as file:
                employee_data = json.load(file)
            for data in employee_data:
                self.analyze_employee_stress(data["text"])
        except FileNotFoundError:
            print("employee.json file not found.")

    def analyze_employee_stress(self, text):
        prompt = f"Analyze the following text for stress level: {text}"
        response = openai.ChatCompletion.create(
            model="gpt-4.0-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        stress_level = self.extract_stress_score(response.choices[0].message['content'])
        # Process the stress level as needed

    def extract_stress_score(self, response):
        match = re.search(r'\b(\d\.\d)\b', response)
        if match:
            return float(match.group(1))
        else:
            return 0.5
          
if __name__ == "__main__":
    clock_app = ChromaticQuantumZonesClock()
    clock_app.mainloop()


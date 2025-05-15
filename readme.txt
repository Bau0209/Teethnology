Teethnology: A Voice-Enabled Web Platform with a 3D Virtual Assistant for Solo Dental Practices

Teethnology is a smart, AI-enhanced web platform tailored specifically for solo dental clinics. It integrates cutting-edge tools like voice-enabled virtual assistants and OCR to streamline administrative tasks and improve patient interaction — helping dentists focus more on patient care and less on paperwork.

Key Features:
1. AI Voice Assistant – Helps patients interact with the system using voice commands for appointments and inquiries. Helps dentist manage patient, appointments, inventory, and other database related records with voice command.
2. OCR (Optical Character Recognition) – Automatically digitizes handwritten or scanned documents using Tesseract + OpenCV.
3. QR Code Patient Forms – Patients scan a code to fill out digital forms before arrival.

Tech Stack:
Frontend	 HTML, CSS, JavaScript
Backend	         Python (Flask)
AI Chatbot	 Hugging Face Flan-T5
OCR	         Tesseract + OpenCV
Voice Assistant	 Web Speech API / SpeechRecognition (Python)
Database	 MySQL (local or AWS-hosted)
Security	 PyCryptodome + Schedule
Hosting	         AWS EC2 (t3.micro instance)

Security:
1. Encryption: All patient records are encrypted using AES encryption with PyCryptodome.
2. Database: MySQL hosted locally or secured on EC2 with firewall rules.
3. Backup: Daily encrypted backups using Python’s schedule library.
4. Cloud Option: Encrypted files can be synced to AWS S3 for redundancy.

About Us:
A team of student developers committed to improving healthcare for small dental clinics through inclusive, AI-powered technology.


Academic Use Only – This project was created for learning and demonstration purposes.
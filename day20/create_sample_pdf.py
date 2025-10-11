# create_sample_pdf.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
c = canvas.Canvas(pdf_path, pagesize=letter)
width, height = letter

# Page 1: Artificial Intelligence
c.setFont("Helvetica-Bold", 16)
c.drawString(72, height - 72, "Artificial Intelligence (AI)")
c.setFont("Helvetica", 12)
c.drawString(72, height - 100, "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines,")
c.drawString(72, height - 115, "especially computer systems. These processes include learning, reasoning, and self-correction.")
c.drawString(72, height - 130, "Applications of AI include expert systems, speech recognition, and machine vision.")
c.showPage()

# Page 2: Machine Learning
c.setFont("Helvetica-Bold", 16)
c.drawString(72, height - 72, "Machine Learning (ML)")
c.setFont("Helvetica", 12)
c.drawString(72, height - 100, "Machine Learning (ML) is a subset of AI that allows software applications to become more")
c.drawString(72, height - 115, "accurate at predicting outcomes without being explicitly programmed.")
c.drawString(72, height - 130, "It uses algorithms and statistical models to analyze and draw inferences from patterns in data.")
c.showPage()

# Page 3: Data Science & Neural Networks
c.setFont("Helvetica-Bold", 16)
c.drawString(72, height - 72, "Data Science & Neural Networks")
c.setFont("Helvetica", 12)
c.drawString(72, height - 100, "Data Science combines domain expertise, programming skills, and knowledge of mathematics")
c.drawString(72, height - 115, "and statistics to extract meaningful insights from data.")
c.drawString(72, height - 130, "Neural Networks are a subset of ML inspired by the human brain, used for image recognition,")
c.drawString(72, height - 145, "natural language processing, and more complex tasks.")
c.showPage()

c.save()
print(f"✅ sample.pdf created at {pdf_path}")

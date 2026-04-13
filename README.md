# ✍️ Air Writing using OpenCV & MediaPipe

A real-time computer vision project that enables users to write in the air using hand gestures via a webcam. The system uses MediaPipe’s hand landmark detection (21 keypoints) to track finger movements and OpenCV to render strokes on a virtual canvas. It implements fingertip tracking, coordinate mapping, temporal stroke tracking, and image blending for smooth drawing. Gesture controls include: ☝️ index finger to draw, ✌️ index + middle fingers to move without drawing, and ✊ fist to clear the canvas. Built using Python, OpenCV, MediaPipe, and NumPy, this project demonstrates real-time gesture recognition and human-computer interaction.

```bash
cd ~/Documents/air-writing-opencv
source venv/bin/activate
python main.py
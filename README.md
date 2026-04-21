# 👵 Gemma 4 AI-Son: Empathetic, Intelligent Care System for the Global Aging Crisis

![Kaggle](https://img.shields.io/badge/Kaggle-Submission-blue?style=for-the-badge&logo=kaggle)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Gemma](https://img.shields.io/badge/Gemma_4_VLM-Powered-orange?style=for-the-badge)
![React Native](https://img.shields.io/badge/React_Native-Expo-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)

> **"Bridging the physical gap between aging parents and busy children through an empathetic Digital Persona and Proactive Edge AI."**

---

## 🚨 The Problem: The "Silver Tsunami" & Caregiving Blind Spots
With the global aging population rapidly increasing, millions of seniors are aging in place alone. The current solutions fall short:
- **Cold Surveillance:** CCTVs cause psychological discomfort and privacy invasion.
- **Fragmented Data:** Wearables generate numbers, not context.
- **Robotic UX:** Traditional AI speakers lack the emotional attachment necessary for seniors to engage.

## 💡 Our Solution: The Digital Persona
**Gemma 4 AI-Son** is not just a smart home device. It is a full-stack, AI-powered **"Digital Persona"** of a beloved family member. It ensures 24/7 safety while providing genuine emotional comfort, combining the strengths of state-of-the-art open-weight models.

---

## 🏗️ Core Architecture & Pipeline

### 1. Low-Power Edge Vision (Safety First)
- **Model:** `YOLOv8 Edge`
- **Role:** An ultra-lightweight vision model monitors the room 24/7. It only wakes the heavy cloud system when a specific trigger is detected (e.g., potential fall, lifting a pill bottle), ensuring privacy and saving massive server costs.

### 2. Deep Contextual Inference (The Brain)
- **Model:** `Gemma 4 VLM` & `Gemma 4 LLM`
- **Role:** When triggered, Gemma 4 analyzes the exact frame. It doesn't just see a "person on the floor"; it understands the context (e.g., "Senior has fallen, and there is a spilled pill bottle nearby"). It also generates Weekly Care Reports based on conversation and activity logs.

### 3. Voice Cloning & Digital Persona (Emotional Care)
- **Model:** `Whisper (STT)` + `XTTS v2 (Zero-shot TTS)`
- **Role:** When the senior speaks, the system replies not with a robotic voice, but with the **cloned voice of their actual child**. This active reinforcement loop (e.g., *"Great job taking your medicine, Mom!"*) dramatically increases user engagement and combats senior depression.

---

## 📂 Repository Structure (Full-stack Proof of Concept)

This repository contains the complete full-stack product code demonstrating our business viability.

```text
📦 Gemma4-AI-Son
 ┣ 📂 backend/         # FastAPI Server (API routing, Database integration)
 ┣ 📂 mobile-app/      # React Native (Expo) App for Guardians (Dashboard, Settings)
 ┣ 📂 gemma-engine/    # Core AI Pipeline (YOLOv8, STT, TTS, Gemma Prompts)
 ┣ 📜 .gitignore       # Pre-configured to ignore heavy model weights and venv
 ┗ 📜 README.md
# Streamlit Nutrition, Fitness & Well-being Prototype

This project is a multi-page Streamlit web application for tracking nutrition, fitness, and well-being. It features user authentication, macro and weight logging, AI-powered food recognition, and more.

---

## 🚀 Getting Started

### 1. **Set Up a Virtual Environment**

Open a terminal in your project folder and run:

On **Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

On **macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### 3. **Configure Environment Variables**

Create a `.env` file in the project root with your Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

### 4. **Run the Streamlit App**

```bash
streamlit run main.py
```
If that doesn't work, try:
```bash
python -m streamlit run main.py
```

---

### 5. **Stop the Streamlit Server**

Press `Ctrl + C` in the terminal.

---

### 6. **Deactivate the Virtual Environment**

```bash
deactivate
```

---

## 📄 Features

- **User Authentication** (Sign Up / Log In)
- **Macro Diary**: Track daily macros
- **Weekly Macros Goal**: Set and view weekly goals
- **Nutritional Lookup**: Search for food nutrition info
- **AI Calorie Scanner**: Identify food from images
- **Weight Log**: Track your weight over time
- **Chat Bot**: Ask nutrition and fitness questions

---

## 📁 Project Structure

```
streamlit/
├── main.py
├── utils/
│   ├── auth_utils.py
│   ├── db_utils.py
│   ├── forms.py
├── pages/
│   ├── Macro_Diary.py
│   ├── Macros_Goal.py
│   ├── Nutritional_Lookup.py
│   ├── Food _Prediction_Estimation.py
│   ├── Weight_Log.py
│   ├── Ask_AI.py
├── models/
│   └── food_classification_model.h5
├── requirements.txt
└── README.md
```

---

## 📝 Notes

- Make sure your Supabase project has the correct Row Level Security (RLS) policies for user tables.
- For camera and AI features, ensure your device has a webcam and the required model file is present.
- If you encounter issues, check the terminal for error messages and ensure all dependencies are installed.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 License

This project is for educational purposes.
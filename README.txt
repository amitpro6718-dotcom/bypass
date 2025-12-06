Flask + Vercel ready project
---------------------------
Files:
- app.py              : Flask application
- templates/index.html: HTML template (converted from your PHP)
- counter.json        : simple JSON counter (used instead of counter.txt)
- requirements.txt    : Python dependencies
- vercel.json         : Vercel config (use @vercel/python builder)

How to run locally:
1) python -m venv venv
2) source venv/bin/activate   (linux/mac) or venv\Scripts\activate (windows)
3) pip install -r requirements.txt
4) python app.py
Visit http://127.0.0.1:8000

Deploy to Vercel:
- Install Vercel CLI and run `vercel` in the project folder and follow prompts.
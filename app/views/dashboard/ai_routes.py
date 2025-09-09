from datetime import date, timedelta
from flask import request, jsonify, session
from vertexai.preview.generative_models import GenerativeModel, Part, Content
from fuzzywuzzy import process
import vertexai
import os
import re
import json

from app.views.dashboard import dashboard
from app.models import Branch, PatientsInfo

# Helper to load prompt
def load_prompt(file_path):
    with open(file_path, "r") as file:
        return file.read()

@dashboard.route('/voice-assistant', methods=['POST'])
def voice_assistant():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ejbau\Teethnology\app\services\vertex-ai-key.json"
    vertexai.init(project="graceful-system-468005-f7", location="us-central1")

    model = GenerativeModel("gemini-2.5-flash-lite")

    prompt_path = os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "dashboard_assistant_prompt.txt")
    system_prompt = load_prompt(prompt_path)

    messages = [
        Content(role="user", parts=[Part.from_text(system_prompt + "\n" + query)])
    ]

    response = model.generate_content(messages)
    cleaned = response.text.strip()

    # Remove code fences if they exist
    if cleaned.startswith("```json"):
        cleaned = re.sub(r"^```json|```$", "", cleaned, flags=re.MULTILINE).strip()    
    try:
        parsed = json.loads(cleaned)
        return jsonify({"response": parsed})
    except Exception as e:
        print("⚠️ JSON parse failed, returning raw:", e)
        return jsonify({"response": response.text})

@dashboard.route('/api/branch_lookup', methods=['POST'])
def branch_lookup():
    data = request.get_json()
    branch_name = data.get("branchName", "").strip().lower()

    if not branch_name:
        return jsonify({"error": "No branch name provided"}), 400

    # Get all branch names from DB
    branches = Branch.query.all()
    branch_names = [b.branch_name for b in branches]

    # Use fuzzy matching to find the closest
    match, score = process.extractOne(branch_name, branch_names)

    if score < 70:  # confidence threshold
        return jsonify({"error": "No close match found"}), 404

    # Get the actual branch object
    branch = Branch.query.filter_by(branch_name=match).first()

    return jsonify({
        "branch_id": branch.branch_id,
        "branch_name": branch.branch_name,
        "confidence": score
    })

def clean_name(name: str) -> str:
    import re
    if not name:
        return ""

    # Keep only letters and spaces
    name = re.sub(r'[^a-z\s]', '', name.lower()).strip()

    # Collapse extra spaces
    name = " ".join(name.split())

    # Detect spelled-out names (e.g., "h e i d a")
    if re.fullmatch(r'(?:[a-z]\s+)+[a-z]', name):
        name = name.replace(" ", "")

    return name
 
@dashboard.route('/api/patient_lookup', methods=['POST'])
def patient_lookup():
    data = request.get_json()
    first_name = clean_name(data.get("firstName", ""))
    middle_name = clean_name(data.get("middleName", ""))
    last_name = clean_name(data.get("lastName", ""))

    cleaned_name = " ".join(filter(None, [first_name, middle_name, last_name]))

    if not cleaned_name:
        return jsonify({"error": "No patient name provided"}), 400

    # Get all patient names from DB
    patients = PatientsInfo.query.all()
    patient_names = [f"{p.first_name} {p.middle_name or ''} {p.last_name}".strip() for p in patients]

    # Use fuzzy matching
    from rapidfuzz import process, fuzz
    result = process.extractOne(cleaned_name, patient_names, scorer=fuzz.WRatio)

    if not result:
        return jsonify({"message": "Can't find a matching patient. Please try spelling the name out for me"}), 404

    match, score, idx = result
    if score < 70:
        return jsonify({"message": "Can't find a matching patient. Please try spelling the name out for me"}), 404

    # Get actual patient object
    normalized_match = match.lower()
    patient = next(
        (p for p in patients if f"{p.first_name} {p.middle_name or ''} {p.last_name}".strip().lower() == normalized_match),
        None
    )

    if not patient:
        return jsonify({"message": "Patient not found."}), 404

    return jsonify({
        "patient_id": patient.patient_id,
        "patient_name": match,
        "confidence": score
    })

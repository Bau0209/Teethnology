import os
from werkzeug.utils import secure_filename
from flask import current_app
from app import db
from app.models import Branch, ClinicBranchImage
from datetime import datetime

def get_first_branch_images():
    from app.models import Branch, ClinicBranchImage
    images = {}
    for branch in Branch.query.all():
        img = ClinicBranchImage.query.filter_by(branch_id=branch.branch_id).first()
        images[branch.branch_id] = img.image_link if img else None
    return images

def branch_exists(branch_name):
    return Branch.query.filter_by(branch_name=branch_name).first() is not None

def save_branch_image(image_file, branch_id):
    filename = secure_filename(image_file.filename)
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'branches')
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    image_file.save(filepath)

    rel_path = os.path.relpath(filepath, os.path.join(current_app.root_path, 'static')).replace('\\', '/')

    image = ClinicBranchImage(image_link=rel_path, branch_id=branch_id)
    db.session.add(image)
    db.session.commit()

    return rel_path

def parse_time_str(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return None

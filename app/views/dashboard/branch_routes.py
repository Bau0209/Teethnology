from flask import render_template, request, flash, redirect, url_for
from app.utils.auth import role_required
from app.utils.branch_handler import get_first_branch_images, parse_time_str, branch_exists, save_branch_image
from app.models import MainWeb, Branch, ClinicBranchImage
from app.views.dashboard import dashboard
from app import db
import os

#For image upload in branches
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dashboard.route('/branches')
# @role_required('owner')
def branches():
    main_web = MainWeb.query.first()
    branches = Branch.query.all()

    # For each branch, get its first image (if any)
    branch_images = get_first_branch_images()
    
    return render_template(
        '/dashboard/branches.html',
        branches=branches,
        main_web=main_web,
        branch_images=branch_images
    )

@dashboard.route('/branches/add', methods=['POST'])
# @role_required('owner')
def add_branch():
    branch_name = request.form.get('branch_name')
    full_address = request.form.get('full_address')
    description = request.form.get('description')
    chief_dentist = request.form.get('chief_dentist')
    contact_number = request.form.get('contact')
    open_time = parse_time_str(request.form.get('open_time'))
    close_time = parse_time_str(request.form.get('close_time'))
    services = ', '.join(request.form.getlist('services[]'))

    if branch_exists(branch_name):
        flash('Branch name already exists.', 'error')
        return redirect(url_for('owner.branches'))

    image_file = request.files.get('image')
    if not image_file:
        flash('Image is required.', 'error')
        return redirect(url_for('owner.branches'))

    new_branch = Branch(
        branch_name=branch_name,
        full_address=full_address,
        clinic_description=description,
        chief_dentist=chief_dentist,
        contact_number=contact_number,
        clinic_open_hour=open_time,
        clinic_close_hour=close_time,
        services=services
    )
    db.session.add(new_branch)
    db.session.commit()

    save_branch_image(image_file, new_branch.branch_id)

    flash('Branch successfully added!', 'success')
    return redirect(url_for('owner.branches'))

@dashboard.route('/branch_info/<int:branch_id>')
# @role_required('owner')
def branch_info(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch_images = ClinicBranchImage.query.filter_by(branch_id=branch_id).all()
    return render_template('/dashboard/branch_info.html', branch=branch, branch_images=branch_images)

@dashboard.route('/branch/<int:branch_id>/add-image', methods=['POST'])
# @role_required('owner')
def add_branch_image(branch_id):
    file = request.files.get('image')
    if not file or file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.referrer)

    if allowed_file(file.filename):
        save_branch_image(file, branch_id)
        flash('Image uploaded successfully.')
    else:
        flash('Invalid file type.', 'danger')

    return redirect(request.referrer)

@dashboard.route('/branch/<int:image_id>/delete-image', methods=['POST'])
# @role_required('owner')
def delete_branch_image(image_id):
    image = ClinicBranchImage.query.get(image_id)
    if image:
        filepath = os.path.join('static', image.image_link)
        if os.path.exists(filepath):
            os.remove(filepath)

        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully.')
    else:
        flash('Image not found.')

    return redirect(request.referrer)

@dashboard.route('/branch/<int:branch_id>/edit', methods=['POST'])
# @role_required('owner')
def edit_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)

    branch.branch_name = request.form['branch_name']
    branch.full_address = request.form['full_address']
    branch.services = request.form['services']
    branch.clinic_description = request.form['clinic_description']
    branch.chief_dentist = request.form['chief_dentist']
    branch.contact_number = request.form['contact_number']
    branch.clinic_open_hour = request.form['clinic_open_hour']
    branch.clinic_close_hour = request.form['clinic_close_hour']

    db.session.commit()
    flash('Branch information updated successfully.', 'success')
    return redirect(url_for('owner.branch_info', branch_id=branch_id))

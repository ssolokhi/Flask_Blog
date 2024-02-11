from flask import url_for, current_app
from flask_blog import mail
from secrets import token_hex
from os import path
from PIL import Image
from flask_mail import Message

def save_image(form_image):
    random_hex = token_hex(8)
    _, file_extension = path.splitext(form_image.filename)
    image_filename = ''.join([random_hex, file_extension])
    image_path = path.join(current_app.root_path, 'static', 'profile_images', image_filename)
    output_size_pixels = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(output_size_pixels) # resize image to avoid costly rendering
    i.save(image_path)
    return image_filename

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request', sender = 'noreply@demo.com', recipients = [user.email])
    message.body = f'''To reset your password, click on the following link:
    {url_for('users.reset_token', token = token, _external = True)}
Didn't request a password reset? Ignore this email.
'''
    mail.send(message)
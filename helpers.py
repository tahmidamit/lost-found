import os
import sys
import random
from flask import redirect, render_template, request, session
from functools import wraps
from email_validator import validate_email, EmailNotValidError
from PIL import Image, ImageOps
from embeddify import Embedder
embedder = Embedder()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=message)


def check_email(email):
    try:
        valid = validate_email(email)
        
        return True

    except EmailNotValidError as e:
        return False

def get_dis():

    districts = ['Bagerhat', 'Bandarban', 'Barguna', 'Barisal', 'Bhola', 'Bogra', 'Brahmanbaria', 'Chandpur', 'Chittagong', 'Chuadanga', 'Comilla', "Cox's Bazar", 'Dhaka', 'Dinajpur', 'Faridpur', 'Feni', 'Gaibandha', 'Gazipur', 'Gopalganj', 'Habiganj', 'Jamalpur', 'Jessore', 'Jhalokati', 'Jhenaidah', 'Joypurhat', 'Khagrachhari', 'Khulna', 'Kishoreganj', 'Kurigram', 'Kushtia', 'Lakshmipur', 'Lalmonirhat', 'Madaripur', 'Magura', 'Manikganj', 'Meherpur', 'Moulvibazar', 'Munshiganj', 'Mymensingh', 'Naogaon', 'Narail', 'Narayanganj', 'Narsingdi', 'Natore', 'Nawabganj', 'Netrakona', 'Nilphamari', 'Noakhali', 'Pabna', 'Panchagarh', 'Patuakhali', 'Pirojpur', 'Rajbari', 'Rajshahi', 'Rangamati', 'Rangpur', 'Satkhira', 'Shariatpur', 'Sherpur', 'Sirajganj', 'Sunamganj', 'Sylhet', 'Tangail', 'Thakurgaon']

    return districts

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_square(im, min_size=1080, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    
    return new_im

def get_song():

    songs = ["https://youtu.be/_J5gJsvK53M", "https://youtu.be/YPHn4xSvjNM", "https://youtu.be/SSbBvKaM6sk", "https://youtu.be/-jvUFIVdR-Y", "https://youtu.be/xdOykEJSXIg", "https://youtu.be/kMwK8AicNGE", "https://youtu.be/HKtsdZs9LJo", "https://youtu.be/NLFzXHRSIHI", "https://youtu.be/hch1BKKCCcg", "https://youtu.be/rmYyPcEQKU4", "https://youtu.be/BKLVpDTZOPQ", "https://youtu.be/Sd6QnOR0T6c", "https://youtu.be/b1dFSWLJ9wY", "https://youtu.be/Fn7FXGaHTNs", "https://youtu.be/rtL5oMyBHPs", "https://youtu.be/PUdyuKaGQd4", "https://youtu.be/9c0M6yMn8kY", "https://youtu.be/F3ImUAHrCSQ", "https://youtu.be/lX44CAz-JhU", "https://youtu.be/Fz4axHOyccQ", "https://youtu.be/Nt5JZL_21u0", "https://youtu.be/na32ogzJBwU", "https://youtu.be/Kc5pqxdv9ew", "https://www.youtube.com/watch?v=asDlYjJqzWE", "https://www.youtube.com/watch?v=XWDzgZpQ8LY", "https://youtu.be/k9SQ2xfHEiM", "https://youtu.be/lRTAmgcopL0", "https://youtu.be/uURsMKMloM8", "https://youtu.be/2SUwOgmvzK4", "https://www.youtube.com/watch?v=tjmk0C64eJg", "https://www.youtube.com/watch?v=rA1hBL_-oZc", "https://www.youtube.com/watch?v=SXF-Eu8XwC8", "https://www.youtube.com/watch?v=dYgrDcXHLwA", "https://www.youtube.com/watch?v=Ukeauj6vfeU", "https://www.youtube.com/watch?v=nROvY9uiYYk", "https://www.youtube.com/watch?v=PAzH-YAlFYc", "https://www.youtube.com/watch?v=9gIFPafF0rs", "https://www.youtube.com/watch?v=bmrN8Cw1zX4", "https://www.youtube.com/watch?v=3I3l-x93kOY"]
    random_index = random.randint(0, len(songs)-1)

    return embedder(songs[random_index])

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

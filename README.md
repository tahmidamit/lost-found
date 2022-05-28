# lost&found
#### Video Demo:  [Youtube](https://youtu.be/nufspK9EmLs).
#### Description:
This is basically a platform where people in my country can post their lost items and if someone finds it he can look up the owner from there, kinda like a lost&found box for the internet.



### Home
The homepage shows recently added ads from newest to oldest. Anyone can access the homepage and the individual ads there. The ads are shown on the homepage in a card style. There's a thumbnail, title, and caption for each of the ads. The location and the time posted of the ads are shown there as well. The links for each ad are unique and can be used to share them around.



### Register
People can register for an account from this page. You need an account to post items so anyone who wants to post will have to go through registration. Proper validations are in place for this. I also stored the hash of the password instead of clean text. So all their privacy will be kept intact.



### Login
Users log in from here.



### Post
Users can post their lost items here. There are * marked on some of the inputs as they are required. There are also some limitations on some of the elements like title, caption etc. You can post with or without images if you like. But the images must be in jpg, png, jpeg and it cannot be bigger than 7MB.



### My_ads
Each user can see what items they have posted. They can also delete those items if they wish to.

### About
There's some information about the project and me on the about page.


### Search
Users can search for their desired items on this page. Although this page hasn't been finished yet. Currently, it just plays a random song from my playlist.


### Hidden riddler
There is a hidden puzzle on this page. Mostly to solve a rot 13 cipher then it will eventually lead to the next clue.

### Hidden jerry
There is a final question here that will solve the hidden puzzle in the game. Submit it and the user will get a shoutout at the leaderboard.


### Stacks used

Memegen api was used to render apologies. I used the cloudinary api to store and host my images. I cound't afford a high performance server which could compress and render responsive images for the site at a big scale.

I also used ajax where necessary to avoid hassle for users on input. HTML

CSS

Javascript

Bootstrap

Jquery


# Going through the files

### Static
Mostly contains some CSS and js files to manipulate the web pages. The js files mostly manipulate next and previous buttons, the get requests, and handle ajax requests. CSS files mostly contain a few tweaks of bootstrap.

### helpers.py
It contains some of the functions of the main app.

### requirements.txt
It contains the modules I need to pip install in order to get my web app working. There's a lot of dependencies that needs to be installed.

# .env
There needs to be a file with Cloudinary's credentials. With that, we can host and upload images.

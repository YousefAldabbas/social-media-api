# Social Media API

The RESTful API for a social media platform. 


## User Registration and Authentication:

- Users can register with their email and password to create an account.
- Users can login with their credentials and receive a token for authentication.
- Users can logout and invalidate their token.

## User Profile:
- Users can create and update their profile, including profile picture, bio, and other details.
- Users can retrieve their own profile and view profiles of other users.
- Users can search for users by username or city where they live.

## Follow/Unfollow:
- Users can follow and unfollow other users.
- Users can view the list of users they are following and the list of users following them.

## Post Creation and Retrieval:
- Users can create new posts with text content and media attachments (e.g., images).
- Users can retrieve posts by hashtags.

## Likes and Comments:
- Users can like and unlike posts. 
- Users can add comments to posts and view comments on posts.

## API Permissions:
- Only authenticated users can perform actions such as creating posts, liking posts, and following/unfollowing users.
- Users can update and delete their own posts and comments.
- Users can update their own profile.

## API Documentation:
- The API well-documented with clear instructions on how to use each endpoint.
- The documentation include sample API requests and responses for different endpoints.

## How to install using GitHub

- Clone this repository
- Create venv: python -m venv venv
- Activate venv: source venv/bin/activate
- Install requirements: pip install -r requirements.txt
- Run: python manage.py runserver
- Create user via: user/register
- Get access token via: user/token

## BD structure
![social_media](https://github.com/HalynaPetrova/social-media-api/assets/92261713/28cf588a-3243-4f36-97eb-6c96b603a617)

# 🌐 Social Media Platform

A mini Social Media Platform built with Django, supporting user profiles, posts with images, likes, comments, following/followers, and notifications. Users can create public or private accounts, share posts, and interact with others.

---

## 🛠️ Tech Stack

- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite 
- Media: Django’s `ImageField` for profile and post images

## 📌 Features

### 👤 User Accounts
- Register with unique `name` and `email`
- Upload profile image
- Choose account type: `public` or `private`
- Age field included

### 📸 Post Management
- Users can create posts with a description, image, and date
- Like and unlike posts
- Track number of likes and who liked the post

### 💬 Comments
- Users can comment on any post
- Comments linked to post and commenter

### 🔗 Follow System
- Follow/unfollow other users
- View followers and following lists

### 🔔 Notifications
- Notifications generated when actions like likes or follows happen
- Each notification linked to source and target user

## 🧩 Entity Overview

### `webuser`
Stores user data.
- Fields: `name`, `age`, `email`, `password`, `ac_type`, `image`

### `web_post`
Stores user posts.
- Fields: `desc`, `date`, `likes`, `post_image`
- Relationships: `webuserId` (FK), `liked_by` (M2M with `webuser`)

### `followers`
Tracks follower-following relationships.
- Fields: `webuser1Id` (user who follows), `webuser2Id` (user being followed)

### `comments`
Stores comments on posts.
- Fields: `comment`, `webpost` (FK), `webuser` (FK)

### `notification`
Stores system-generated user notifications.
- Fields: `message`, `webuser1` (sender), `webuser2` (receiver)

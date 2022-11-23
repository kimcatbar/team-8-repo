## Functional Requirements

1. Login (Tanveer)
2. Logout (Kimberly)
3. Create new account (Tanveer)
4. Delete account (Antony)
5. User home page (user can see messages of users they follow) (Antony)
6. Send message to followers (Ngoc)
7. Create a new post (Kimberly)
8. View User Profile (Kimberly)
9. Send private message to follower(s) (Ngoc)
10. Follow users (Ngoc)
11. Post image with message (Antony)
12. Search for a user (Tanveer)

Non-functional Requirements

1. Works on Chrome browser
2. Back up data
3. Multilingual Support
4. Web only/no app support

## Use Cases

5. Use Case Name: User Home Page
- **Pre-condition:** User must be logged in. Users must have followers that have created a post or sent a message to the user.

- **Trigger:** The user logs into their account.
  
- **Primary Sequence:** 
  
  1. User accesses website.
  2. User longs into their account.
  3. After log in is successful, user home page is displayed.
  
- **Primary Postconditions:**
  1. Users can view the home page.
  2. Users can interact with content on the home page.
  3. Users will be able to view posts and comments about the user.
  4. Users can make posts from the home page.

- **Alternate Sequence:**
  1. User is logged in and on a page of the website.
  2. User clicks the home button.
  3. User is brought to the home page.

7. Create a newpost
  
- **Pre-condition:** User must be logged in to existing account and in homepage
  
- **Trigger:** User selects “new post” option 
  
- **Primary Sequence:** 
  
  1. Login
  2. Be in homepage
  3. Then selecting “new post” 
  
- **Primary Postconditions:** 
  
  1. Textbox and “submit” button will appear    
  2. User can submit a fixed amount of characters  
  3. User can also submit an image (if other functional requirement works)
  4. New post is accepeted 
  
- **Alternate Sequence:**
  
  1. Login
  2. Be in user profile 
  3. Then selecting “new post”
  
- **Alternate Postconditions:** 
  
  1. Textbox and “submit” button will appear  
  2. User can submit a fixed amount of characters
  3. User can also submit an image (if other functional requirement works)
  4. Image too large or format is not supported
  5. User asked to upload another type of image 
  
8. View User Profile
  
- **Pre-condition:** User must be logged in to existing account and in homepage 
  
- **Trigger:** User selects “view profile” option 
  
- **Primary Sequence:** 
  
  1. User must login   
  2. User must be in homepage
  3. Select “view profile”
  
- **Primary Postconditions:** 
  
  1. User is redirected to their profile 
  2. Can scroll and see previous posts 
  3. User can select “new post” 
  
- **Alternate Sequence:**
  
  1. User is in homepage
  2. User selects “view profile” 
  
- **Alternate Postconditions:**
  
  1. User is redirected to their profile
  2. Can scroll and see previous posts 
  3. User can select “new post”
  
9. Send private message to followers
- **Pre-condition:** Users must be logged in into the homepage and have a user who is currently following them.
- **Trigger:** User must select messages section of the home page.
- **Primary Sequence:**
  
  1. Click on “send message”
  2. Type the name of the follower to send message to
  3. Type the message
  4. Click Send

- **Primary Postconditions:** Follower receives message in their message section of their homepage and is able to read and reply

- **Alternate Sequence:**
  
  1. Click on “send message”
  2. Try to send message without entering a follower or message
  3. Error message appears notifying missing fields

10. Follow user
- **Pre-condition:** User is logged in
- **Trigger:** The follow option is presented to the user
- **Primary Sequence:**
  
  1. User goes to the profile of those they want to follow.
  2. User clicks on the follow button.

- **Primary Postconditions:**
  1.  User is now following that user and users can also remove followers
  2.  Users can see who is following them on their homepage
  3.  User homepage will now have posts from who they follow
  
- **Alternate Sequence:**
  
  1. User tries to follow other users with private account
  2. The other user isn’t allowing follows at the moment
  3. User will be denied and told that user is currently not accepting followers
  
12. Use Case Name: Search for a user 
- **Pre-condition:** User must be logged in and the user must exist . Other users should exist on the platform. 

- **Trigger:** When the user hits the search button.

- **Primary Sequence:**
  
  1. User clicks on the search button
  2. User enters the username they are looking for.
  3. User clicks on search button

- **Primary Postconditions:** 

  1. Users can view users with a similar username.
  2. Users can follow the looked up users.
  3. Users will be able to view posts and comments about the user.
  4. Users can send the looked up users message.

- **Alternative Sequence:** 
  1. User clicks on the search button.
  2. User search with nothing typed in the search bar.
  3. Error and prompts the user to enter a username.

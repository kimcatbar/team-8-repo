Funtional Requirements

1. Login
2. Logout
3. Create new account
4. Delete account
5. User home page (user can see messages of users they follow)
6. Send message to followers (reply to follower posts)
7. requirement
8. requirement
9. Send private message to follower(s)
10. Follow users
11. requirement
12. requirement

Non-functional Requirements

1. non-functional
2. Back up data
3. non-functional
4. non-functional

Use Cases

9. Send private message to followers
- **Pre-condition:** <Users must loggin Users must be logged in into the homepage and have a user who is currently following them.> 
- **Trigger:** <User must select messages section of the home page>
- **Primary Sequence:**
  
  1. Click on “send message”
  2. Type the name of the follower to send message to
  3. Type the message
  4. Click Send

- **Primary Postconditions:** <Follower receives message in their message section of their homepage and is able to read and reply>

- **Alternate Sequence:**
  
  1. Click on “send message”
  2. Try to send message without entering a follower or message
  3. Error message appears notifying missing fields

10. Follow user
- **Pre-condition:** <User is logged in> 
- **Trigger:** <The follow option is presented to the user>
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

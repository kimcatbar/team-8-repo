## Functional Requirements

1. Login (Tanveer)
2. Logout (Kimberly)
3. Create new account (Tanveer)
4. Delete account (Antony)
5. User home page (user can see messages of users they follow) (Antony)
6. Send message to followers (Ngoc)
7. Create a new post (Kimberly)
8. View User Profile (Kimberly)
9. requirement
10. requirement
11. Post image with message (Antony)
12. Search for a user (Tanveer)

## Non-functional Requirements

1. Works on Chrome browser
2. non-functional
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

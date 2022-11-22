## Functional Requirements

1. Login
2. Logout
3. Create new account
4. Delete account
5. User home page (user can see messages of users they follow)
6. Send message to followers
7. Create a new post 
8. View User Profile 

9. requirement
10. requirement
11. Post image with message
12. requirement

## Non-functional Requirements

1. Works on Chrome browser
2. non-functional
3. non-functional
4. Web only/no app support

## Use Cases

1. Use Case Name: User Home Page
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

2. Create a newpost (K)
  
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
  
3. View User Profile (K)
  
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

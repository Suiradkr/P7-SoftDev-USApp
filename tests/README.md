# GUDLFT | Test plan

The following actions / features must be tested.

| Item | Expected result(s) | Related issue |
| --- | --- | --- |
| Clubs and competitions can be loaded from the JSON file. | The file is read and correct data returned. | |
| The homepage is available. | The login form is displayed (HTTP status code 200). | |
| A user can login by typing a valid email in the form on the homepage. | The user is logged in, the custom homepage is displayed. The custom homepage shows the email of the user logged in, and the number of points available for their club. | |
| A user cannot login with an invalid email. | The user cannot login, an error message is displayed with HTTP code 401. | #1 |
| A session naming a club that no longer exists cannot browse the app. | Show an error page (HTTP status code 401). | #27 |
| A logged in user can book spots for a competition. | The form is displayed. | |
| A logged in user cannot book spots for an invalid competition. | If the competition does not exist, show an error page (HTTP status code 404). | #13 |
| A logged in user cannot book spots for a competition in the past. | Show an error page (HTTP status code 403). | #4 |
| The points are updated when a booking is made. | The number of points for the club that made the book has decreased by 1 (for 1 booking). The number of spots available in the competition has decreased by 1 (for 1 booking). | #5 |
| A club's points are not lost when it logs out and back in. | The points still reflect every booking made, and stay in step with the competition's spots. | #27 |
| A club cannot book more than 12 spots in a competition. | Display an error page with HTTP status code 403. | #3 |
| The 12 spot limit applies to a club's running total in a competition, not to a single booking. | A repeat booking that would take the total past 12 shows an error page (HTTP status code 403). Spots booked in one competition do not count against another. | #19 |
| A club cannot book more spots than they have points. | Display an error page with HTTP status code 403. | #2 |
| A club cannot book more spots than available in the competition. | Display an error page with HTTP status code 403. | #14 |
| A club cannot book zero or a negative number of spots. | The booking is rejected with a message and the club's points are unchanged. | |
| The booking form only accepts a whole number of spots. | The input is a number field with whole steps, is required, and is bounded by the club's remaining allowance. | #21 |
| A non-numeric spots value does not crash the app. | A request made outside the form sending a non-numeric value is rejected with a message rather than HTTP 500. | #23 |
| Any user can see the list of clubs and their points available. | The list of clubs is displayed, showing the name and points for each club. | #6 |
| A user can log out. | The session is cleared and the user is returned to the homepage. | |

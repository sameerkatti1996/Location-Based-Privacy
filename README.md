# Location-Based-Privacy

This is a final year(7th semester) project done at BMS College of Engineering.

Refer to Report-Final.pdf for full details.

This is a prototype for implementing location privacy using two methods:
1. Location Obfuscation: Choose a nearby location and use it instead of the user location.
2. K-Anonymity: Use k-1 dummies close to user location

====================================================================================================
====================================================================================================
====================================================================================================

EXAMPLES:
====================================================================================================
Location Obfuscation:
This method gave a generalized area or the locality of the user's location for all the
locations.
Some of the examples are:
1. User's Location: 
        Kempe Gowda tower atop twin boulders., B M S College of Law Road, Basavanagudi, Bengaluru, Karnataka 560004, India.
   Obfuscated Location generated: 
        Basavanagudi, Bengaluru. 
2. User's Location: 
        Railway Station Rd, Malmaddi, Dharwad, Karnataka 580001, India
   Obfuscated Location generated: 
        Malmaddi, Dharwad.
3. User's Location: 
        Hanamsagar Road, Hanamsagar, Karnataka 583281, India
    Obfuscated Location: 
        Hanamasagar.

The location obfuscation will work at all kinds of places – City, Town, Village, etc.

====================================================================================================

k-Anonymity :
The method generates k-1 dummy locations and merges those locations with the
user's location to form a set of k similar locations. Then these locations can be used to query
the LBS.

Try 1:
===============
User's Location: B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India

k=10 locations:
1. Sri Maasti Venkateshiyangar Rd, Gavipuram Extn, Gavipuram Extention, Kempegowda Nagar, Bengaluru, Karnataka 560019, India
2. Megha Residency, Basavanagudi, Bengaluru, Karnataka 560004, India
3. Panchavati Niwas, Jain Temple Cross Rd, Parvathipuram, Vishweshwarapura, Shankarapura, Bengaluru, Karnataka 560004, India
4. 3rd Cross Rd, Gavipuram Extn, Gavipuram Extention, Kempegowda Nagar, Bengaluru, Karnataka 560019, India
5. Temple, Govindappa Road, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
6. B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India     <-------- actual location
7. BP Wadia Rd, Basavanagudi, Bengaluru, Karnataka 560004, India
8. Rathna Niwas, 4th Cross Rd, Shankarapura, Bengaluru, Karnataka 560004, India
9. 137, Kanakapura Rd, 2nd Block, 7th Block, Jayanagar, Bengaluru, Karnataka 560011, India
10. 50, Vanivilas Rd, Basavanagudi, Bengaluru, Karnataka 560004, India

Try 2:
================
User's Location: B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India

k = 10 locations:
1. NN Plaza, Subbarama Chetty Rd, Shankarapura, Bengaluru, Karnataka 560004, India
2. Shyampuri Residency, Conservancy Ln, Basavanagudi, Bengaluru, Karnataka 560004, India
3. B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India   <----- actual location
4. Steps to Bull Temple, Basavanagudi, Bengaluru, Karnataka 560004, India
5. 85, Gavipuram Extn, Gavipuram Extention, Kempegowda Nagar, Bengaluru, Karnataka 560019, India
6. Pampa Mahakavi Rd, Shankarapura, Bengaluru, Karnataka 560004, India
7. Rathna Niwas, 4th Cross Rd, Shankarapura, Bengaluru, Karnataka 560004, India
8. E Anjaneya Temple St, Basavanagudi, Bengaluru, Karnataka 560004, India
9. 2, DVG Road, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
10. 6/152, DVG Road, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India

Try 3:
================
User's Location: B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India

k = 10 locations:
1. 14/3, Bugle Rock Rd, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
2. 115, Surveyor St, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
3. 35, 1st Cross Rd, Gavipuram Extn, Gavipuram Extention, Kempegowda Nagar, Bengaluru, Karnataka 560019, India
4. 4, Krishna Rd, Basavanagudi, Bengaluru, Karnataka 560004, India
5. Prathiba Complex, Karnic Rd, Shankarapura, Bengaluru, Karnataka 560004, India
6. 99/6, Mahantara Lay Out, Kempegowda Nagar, Bengaluru, Karnataka 560019, India
7. 4, Krishna Rd, Basavanagudi, Bengaluru, Karnataka 560004, India
8. 24, Bugle Rock Rd, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
9. 66, Vanivilas Rd, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
10. B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India.  <------ actual location

Try 4:
================
User's Location: B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India

k = 10 locations:
1. 29, HB Samaja Rd, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
2. 104, Surveyor St, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
3. 93, Kanakapura Rd, Basavanagudi, Bengaluru, Karnataka 560004, India
4. 14, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
5. B M S College of Engineering, Bull Temple Road, Basavanagudi, Bengaluru, Karnataka 560019, India    <------- actual location
6. Siddaiya Complex, Mount Joy Rd, Gavipuram Extn, Basavanagudi, Bengaluru, Karnataka 560019, India
7. Soundarya Nilayam, Market Rd, Basavanagudi, Bengaluru, Karnataka 560004, India
8. 113, Diagonal Rd, Parvathipuram, Vishweshwarapura, Shankarapura, Bengaluru, Karnataka 560004, India
9. 38/2, Gandhi Bazar Main Rd, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India
10. North Public Square Road, Basavanagudi, Bengaluru, Karnataka 560004, India

The different tries conducted show that at k=10, a user location is well hidden among 10 locations and the position of the user location never is the same. Also, the other 9 locations keep on changing confirming the effectiveness of the algorithm.

"""features.py - data for the Timeline, Map and Quiz pages.

All facts match the files in the data/ folder. Verify them before presenting.
"""

# (year, title, detail, category)
TIMELINE = [
    (1163, "Thousand Pillar Temple", "Kakatiya king Rudra Deva builds it at Hanamkonda.", "Heritage"),
    (1213, "Ramappa Temple", "Built at Palampet by Recherla Rudra, a general of Ganapati Deva.", "Heritage"),
    (1518, "Qutb Shahi rule begins", "The dynasty rules from Golconda until 1687.", "Heritage"),
    (1591, "Hyderabad and Charminar", "Muhammad Quli Qutb Shah founds Hyderabad and builds the Charminar.", "Heritage"),
    (1687, "Fall of Golconda", "Aurangzeb conquers Golconda.", "Heritage"),
    (1724, "Asaf Jahi dynasty founded", "Mir Qamar-ud-din Khan, Asaf Jah I, begins Nizam rule.", "Nizam era"),
    (1853, "Salar Jung I", "Becomes prime minister of Hyderabad State and reforms administration.", "Nizam era"),
    (1908, "Great Musi flood", "Leads to the building of Osman Sagar and Himayat Sagar.", "Nizam era"),
    (1911, "Last Nizam", "Mir Osman Ali Khan, Asaf Jah VII, begins his rule.", "Nizam era"),
    (1918, "Osmania University", "Founded in Hyderabad.", "Nizam era"),
    (1930, "Andhra Mahasabha", "Founded at Jogipet to promote Telugu language and culture.", "Movement"),
    (1940, "Komaram Bheem", "The Gond leader is killed at Jodeghat.", "Movement"),
    (1946, "Telangana Armed Struggle begins", "Peasant uprising against jagirdars and vetti.", "Movement"),
    (1947, "Standstill Agreement", "The Nizam signs it with India in November.", "Nizam era"),
    (1948, "Operation Polo", "13 to 17 September: Hyderabad State joins the Indian Union.", "Nizam era"),
    (1951, "Armed struggle withdrawn", "The communist party withdraws the struggle in October.", "Movement"),
    (1952, "First elected government", "Burgula Ramakrishna Rao becomes chief minister; Non-Mulki agitation.", "Movement"),
    (1956, "Andhra Pradesh formed", "1 November: Telangana merges with Andhra State.", "Movement"),
    (1969, "Jai Telangana agitation", "Student-led protests demand a separate state.", "Movement"),
    (2001, "TRS formed", "K. Chandrashekar Rao forms the party on 27 April.", "Movement"),
    (2009, "Announcement and reversal", "Process announced on 9 December, put on hold on 23 December.", "Movement"),
    (2011, "Million March", "Sakala Janula Samme general strike led by the Telangana JAC.", "Movement"),
    (2013, "Congress Working Committee", "Supports a separate Telangana on 30 July.", "Movement"),
    (2014, "Telangana formed", "2 June: India's 29th state is born; KCR is the first chief minister.", "Modern"),
    (2019, "Kaleshwaram project", "Lift irrigation project on the Godavari is inaugurated in June.", "Modern"),
    (2021, "Ramappa Temple", "UNESCO declares it a World Heritage Site.", "Modern"),
    (2023, "Assembly election", "Congress wins; A. Revanth Reddy becomes chief minister in December.", "Modern"),
]

CATEGORIES = ["Heritage", "Nizam era", "Movement", "Modern"]

# Approximate locations (latitude, longitude)
PLACES = [
    ("Hyderabad", 17.385, 78.487, "Capital; Charminar, Golconda, Nizam's palaces"),
    ("Warangal", 17.969, 79.594, "Kakatiya capital Orugallu; Warangal Fort"),
    ("Palampet", 18.260, 79.941, "Ramappa Temple, UNESCO World Heritage Site"),
    ("Karimnagar", 18.439, 79.129, "Major city of north Telangana"),
    ("Nizamabad", 18.673, 78.094, "Near Sriram Sagar project on the Godavari"),
    ("Adilabad", 19.664, 78.532, "Komaram Bheem's region; forests and Kawal Tiger Reserve area"),
    ("Khammam", 17.247, 80.151, "East Telangana; part of the armed struggle region"),
    ("Nalgonda", 17.057, 79.268, "Heart of the Telangana armed struggle"),
    ("Mahabubnagar", 16.737, 77.985, "South Telangana on the Deccan Plateau"),
]

QUIZ = [
    {"q": "Who was the last Nizam of Hyderabad?",
     "options": ["Mir Osman Ali Khan", "Mahbub Ali Khan", "Salar Jung I", "Asaf Jah I"],
     "answer": "Mir Osman Ali Khan"},
    {"q": "When did Operation Polo take place?",
     "options": ["August 1947", "13 to 17 September 1948", "January 1950", "November 1956"],
     "answer": "13 to 17 September 1948"},
    {"q": "Who formed the Telangana Rashtra Samithi in 2001?",
     "options": ["M. Chenna Reddy", "Burgula Ramakrishna Rao", "K. Chandrashekar Rao", "M. Kodandaram"],
     "answer": "K. Chandrashekar Rao"},
    {"q": "On which date was Telangana state formed?",
     "options": ["1 November 1956", "9 December 2009", "30 July 2013", "2 June 2014"],
     "answer": "2 June 2014"},
    {"q": "Which two major rivers flow through Telangana?",
     "options": ["Kaveri and Tungabhadra", "Godavari and Krishna", "Narmada and Tapi", "Mahanadi and Brahmani"],
     "answer": "Godavari and Krishna"},
    {"q": "Which Gond leader used the slogan Jal, Jangal, Zameen?",
     "options": ["Komaram Bheem", "Ravi Narayana Reddy", "Qasim Razvi", "Sundarayya"],
     "answer": "Komaram Bheem"},
    {"q": "In which year did UNESCO name Ramappa Temple a World Heritage Site?",
     "options": ["2014", "2019", "2021", "2023"],
     "answer": "2021"},
    {"q": "Who founded the city of Hyderabad in 1591?",
     "options": ["Muhammad Quli Qutb Shah", "Ganapati Deva", "Aurangzeb", "Nizam-ul-Mulk"],
     "answer": "Muhammad Quli Qutb Shah"},
    {"q": "How many districts does Telangana have?",
     "options": ["10", "21", "33", "38"],
     "answer": "33"},
    {"q": "How often is the Medaram Sammakka Saralamma Jatara held?",
     "options": ["Every year", "Every two years", "Every five years", "Every twelve years"],
     "answer": "Every two years"},
]
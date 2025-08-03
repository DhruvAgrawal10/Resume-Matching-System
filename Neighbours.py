indian_state_neighbors = {
    "Andhra Pradesh": ["Telangana", "Tamil Nadu", "Karnataka", "Odisha", "Chhattisgarh"],
    "Arunachal Pradesh": ["Assam", "Nagaland"],
    "Assam": ["Arunachal Pradesh", "Nagaland", "Manipur", "Meghalaya", "Tripura", "Mizoram", "West Bengal"],
    "Bihar": ["Uttar Pradesh", "Jharkhand", "West Bengal"],
    "Chhattisgarh": ["Madhya Pradesh", "Maharashtra", "Telangana", "Odisha", "Jharkhand", "Uttar Pradesh"],
    "Goa": ["Maharashtra", "Karnataka"],
    "Gujarat": ["Maharashtra", "Madhya Pradesh", "Rajasthan"],
    "Haryana": ["Punjab", "Himachal Pradesh", "Uttarakhand", "Uttar Pradesh", "Rajasthan", "Delhi"],
    "Himachal Pradesh": ["Punjab", "Haryana", "Uttarakhand", "Jammu and Kashmir"],
    "Jharkhand": ["Bihar", "Odisha", "Chhattisgarh", "West Bengal"],
    "Karnataka": ["Goa", "Maharashtra", "Telangana", "Andhra Pradesh", "Tamil Nadu", "Kerala"],
    "Kerala": ["Tamil Nadu", "Karnataka"],
    "Madhya Pradesh": ["Uttar Pradesh", "Chhattisgarh", "Maharashtra", "Rajasthan", "Gujarat"],
    "Maharashtra": ["Gujarat", "Madhya Pradesh", "Chhattisgarh", "Telangana", "Karnataka", "Goa"],
    "Manipur": ["Nagaland", "Mizoram", "Assam"],
    "Meghalaya": ["Assam"],
    "Mizoram": ["Tripura", "Manipur", "Assam"],
    "Nagaland": ["Arunachal Pradesh", "Assam", "Manipur"],
    "Odisha": ["West Bengal", "Jharkhand", "Chhattisgarh", "Andhra Pradesh"],
    "Punjab": ["Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Rajasthan"],
    "Rajasthan": ["Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Gujarat"],
    "Sikkim": ["West Bengal"],
    "Tamil Nadu": ["Andhra Pradesh", "Karnataka", "Kerala"],
    "Telangana": ["Maharashtra", "Chhattisgarh", "Andhra Pradesh", "Karnataka"],
    "Tripura": ["Assam", "Mizoram"],
    "Uttar Pradesh": ["Uttarakhand", "Himachal Pradesh", "Delhi", "Haryana", "Rajasthan", "Madhya Pradesh", "Chhattisgarh", "Bihar", "Jharkhand"],
    "Uttarakhand": ["Himachal Pradesh", "Uttar Pradesh"],
    "West Bengal": ["Bihar", "Jharkhand", "Odisha", "Sikkim", "Assam"],
    "Delhi": ["Haryana", "Uttar Pradesh"],
    "Jammu and Kashmir": ["Himachal Pradesh", "Punjab", "Ladakh"],  # Include Ladakh as separate if needed
    "Ladakh": ["Jammu and Kashmir", "Himachal Pradesh"]
}

usa_state_neighbors = {
    "Alabama": ["Florida", "Georgia", "Mississippi", "Tennessee"],
    "Alaska": [],
    "Arizona": ["California", "Nevada", "Utah", "Colorado", "New Mexico"],
    "Arkansas": ["Missouri", "Tennessee", "Mississippi", "Louisiana", "Texas", "Oklahoma"],
    "California": ["Oregon", "Nevada", "Arizona"],
    "Colorado": ["Wyoming", "Nebraska", "Kansas", "Oklahoma", "New Mexico", "Arizona", "Utah"],
    "Connecticut": ["Massachusetts", "Rhode Island", "New York"],
    "Delaware": ["Maryland", "New Jersey", "Pennsylvania"],
    "Florida": ["Alabama", "Georgia"],
    "Georgia": ["Florida", "Alabama", "Tennessee", "North Carolina", "South Carolina"],
    "Hawaii": [],
    "Idaho": ["Montana", "Wyoming", "Utah", "Nevada", "Oregon", "Washington"],
    "Illinois": ["Indiana", "Kentucky", "Missouri", "Iowa", "Wisconsin"],
    "Indiana": ["Michigan", "Ohio", "Kentucky", "Illinois"],
    "Iowa": ["Minnesota", "Wisconsin", "Illinois", "Missouri", "Nebraska", "South Dakota"],
    "Kansas": ["Nebraska", "Missouri", "Oklahoma", "Colorado"],
    "Kentucky": ["Illinois", "Indiana", "Ohio", "West Virginia", "Virginia", "Tennessee", "Missouri"],
    "Louisiana": ["Arkansas", "Mississippi", "Texas"],
    "Maine": ["New Hampshire"],
    "Maryland": ["Virginia", "West Virginia", "Delaware", "Pennsylvania"],
    "Massachusetts": ["New Hampshire", "Vermont", "New York", "Connecticut", "Rhode Island"],
    "Michigan": ["Ohio", "Indiana", "Wisconsin", "Minnesota (via water)"],
    "Minnesota": ["North Dakota", "South Dakota", "Iowa", "Wisconsin"],
    "Mississippi": ["Louisiana", "Arkansas", "Tennessee", "Alabama"],
    "Missouri": ["Iowa", "Illinois", "Kentucky", "Tennessee", "Arkansas", "Oklahoma", "Kansas", "Nebraska"],
    "Montana": ["North Dakota", "South Dakota", "Wyoming", "Idaho"],
    "Nebraska": ["South Dakota", "Iowa", "Missouri", "Kansas", "Colorado", "Wyoming"],
    "Nevada": ["Oregon", "Idaho", "Utah", "Arizona", "California"],
    "New Hampshire": ["Maine", "Massachusetts", "Vermont"],
    "New Jersey": ["New York", "Delaware", "Pennsylvania"],
    "New Mexico": ["Colorado", "Oklahoma", "Texas", "Arizona"],
    "New York": ["Pennsylvania", "New Jersey", "Connecticut", "Massachusetts", "Vermont"],
    "North Carolina": ["Virginia", "South Carolina", "Georgia", "Tennessee"],
    "North Dakota": ["Minnesota", "South Dakota", "Montana"],
    "Ohio": ["Pennsylvania", "West Virginia", "Kentucky", "Indiana", "Michigan"],
    "Oklahoma": ["Texas", "Arkansas", "Missouri", "Kansas", "Colorado", "New Mexico"],
    "Oregon": ["Washington", "Idaho", "Nevada", "California"],
    "Pennsylvania": ["New York", "New Jersey", "Delaware", "Maryland", "West Virginia", "Ohio"],
    "Rhode Island": ["Massachusetts", "Connecticut"],
    "South Carolina": ["North Carolina", "Georgia"],
    "South Dakota": ["North Dakota", "Minnesota", "Iowa", "Nebraska", "Wyoming", "Montana"],
    "Tennessee": ["Kentucky", "Virginia", "North Carolina", "Georgia", "Alabama", "Mississippi", "Arkansas", "Missouri"],
    "Texas": ["New Mexico", "Oklahoma", "Arkansas", "Louisiana"],
    "Utah": ["Idaho", "Wyoming", "Colorado", "New Mexico", "Arizona", "Nevada"],
    "Vermont": ["New York", "New Hampshire", "Massachusetts"],
    "Virginia": ["North Carolina", "Tennessee", "Kentucky", "West Virginia", "Maryland"],
    "Washington": ["Idaho", "Oregon"],
    "West Virginia": ["Pennsylvania", "Maryland", "Virginia", "Kentucky", "Ohio"],
    "Wisconsin": ["Minnesota", "Iowa", "Illinois", "Michigan"],
    "Wyoming": ["Montana", "South Dakota", "Nebraska", "Colorado", "Utah", "Idaho"]
}

canada_province_neighbors = {
    "Alberta": ["British Columbia", "Saskatchewan", "Northwest Territories"],
    "British Columbia": ["Alberta", "Yukon"],
    "Manitoba": ["Saskatchewan", "Ontario", "Nunavut"],
    "New Brunswick": ["Nova Scotia", "Quebec", "Prince Edward Island (via bridge)"],
    "Newfoundland and Labrador": [],
    "Nova Scotia": ["New Brunswick", "Prince Edward Island (via bridge)"],
    "Ontario": ["Manitoba", "Quebec"],
    "Prince Edward Island": ["New Brunswick", "Nova Scotia"],
    "Quebec": ["Ontario", "New Brunswick", "Newfoundland and Labrador"],
    "Saskatchewan": ["Alberta", "Manitoba", "Northwest Territories"],
    "Northwest Territories": ["Yukon", "British Columbia", "Alberta", "Saskatchewan", "Nunavut"],
    "Nunavut": ["Manitoba", "Northwest Territories"],
    "Yukon": ["British Columbia", "Northwest Territories"]
}

uk_region_neighbors = {
    # Countries
    "England": ["Scotland", "Wales"],
    "Scotland": ["England"],
    "Wales": ["England"],
    "Northern Ireland": [],  # separated by sea from rest of UK, borders Republic of Ireland (not in UK)

    # England regions (NUTS1 level)
    "North East England": ["North West England", "Yorkshire and the Humber"],
    "North West England": ["North East England", "Yorkshire and the Humber", "West Midlands"],
    "Yorkshire and the Humber": ["North East England", "North West England", "East Midlands"],
    "East Midlands": ["Yorkshire and the Humber", "West Midlands", "East of England"],
    "West Midlands": ["North West England", "East Midlands", "South West England", "Wales"],
    "East of England": ["East Midlands", "South East England", "London"],
    "South East England": ["East of England", "London", "South West England"],
    "South West England": ["West Midlands", "South East England", "Wales"],
    "London": ["South East England", "East of England"],

    # Scotland and Wales subdivisions (for future use)
    # Currently, Scotland and Wales are not subdivided into NUTS1 regions like England in resume databases
}




australia_state_neighbors = {
    "New South Wales": ["Queensland", "South Australia", "Victoria", "Australian Capital Territory"],
    "Victoria": ["New South Wales", "South Australia"],
    "Queensland": ["Northern Territory", "South Australia", "New South Wales"],
    "South Australia": ["Western Australia", "Northern Territory", "Queensland", "New South Wales", "Victoria"],
    "Western Australia": ["Northern Territory", "South Australia"],
    "Tasmania": [],  # Island
    "Northern Territory": ["Western Australia", "South Australia", "Queensland"],
    "Australian Capital Territory": ["New South Wales"]
}

germany_state_neighbors = {
    "Baden-Württemberg": ["Bavaria", "Hesse", "Rhineland-Palatinate"],
    "Bavaria": ["Baden-Württemberg", "Hesse", "Thuringia", "Saxony"],
    "Berlin": ["Brandenburg"],
    "Brandenburg": ["Mecklenburg-Vorpommern", "Saxony", "Saxony-Anhalt", "Berlin"],
    "Bremen": ["Lower Saxony"],
    "Hamburg": ["Schleswig-Holstein", "Lower Saxony"],
    "Hesse": ["North Rhine-Westphalia", "Rhineland-Palatinate", "Bavaria", "Thuringia", "Lower Saxony"],
    "Lower Saxony": ["Schleswig-Holstein", "Hamburg", "Bremen", "Hesse", "Saxony-Anhalt", "North Rhine-Westphalia"],
    "Mecklenburg-Vorpommern": ["Brandenburg", "Schleswig-Holstein"],
    "North Rhine-Westphalia": ["Lower Saxony", "Hesse", "Rhineland-Palatinate"],
    "Rhineland-Palatinate": ["North Rhine-Westphalia", "Hesse", "Baden-Württemberg", "Saarland"],
    "Saarland": ["Rhineland-Palatinate"],
    "Saxony": ["Bavaria", "Thuringia", "Saxony-Anhalt", "Brandenburg"],
    "Saxony-Anhalt": ["Lower Saxony", "Brandenburg", "Saxony", "Thuringia"],
    "Schleswig-Holstein": ["Hamburg", "Lower Saxony", "Mecklenburg-Vorpommern"],
    "Thuringia": ["Hesse", "Bavaria", "Saxony", "Saxony-Anhalt"]
}

neighbors_data = {
        **indian_state_neighbors,
        **usa_state_neighbors,
        **canada_province_neighbors,
        **australia_state_neighbors,
        **germany_state_neighbors,
        **uk_region_neighbors
    }
from django.db import models


class State(models.TextChoices):
    ANDHRA_PRADESH = 'AP', 'Andhra Pradesh'
    ARUNACHAL_PRADESH = 'AR', 'Arunachal Pradesh'
    ASSAM = 'AS', 'Assam'
    BIHAR = 'BR', 'Bihar'
    CHHATTISGARH = 'CG', 'Chhattisgarh'
    GOA = 'GA', 'Goa'
    GUJARAT = 'GJ', 'Gujarat'
    HARYANA = 'HR', 'Haryana'
    HIMACHAL_PRADESH = 'HP', 'Himachal Pradesh'
    JHARKHAND = 'JH', 'Jharkhand'
    KARNATAKA = 'KA', 'Karnataka'
    KERALA = 'KL', 'Kerala'
    MADHYA_PRADESH = 'MP', 'Madhya Pradesh'
    MAHARASHTRA = 'MH', 'Maharashtra'
    MANIPUR = 'MN', 'Manipur'
    MEGHALAYA = 'ML', 'Meghalaya'
    MIZORAM = 'MZ', 'Mizoram'
    NAGALAND = 'NL', 'Nagaland'
    ODISHA = 'OR', 'Odisha'
    PUNJAB = 'PB', 'Punjab'
    RAJASTHAN = 'RJ', 'Rajasthan'
    SIKKIM = 'SK', 'Sikkim'
    TAMIL_NADU = 'TN', 'Tamil Nadu'
    TELANGANA = 'TG', 'Telangana'
    TRIPURA = 'TR', 'Tripura'
    UTTAR_PRADESH = 'UP', 'Uttar Pradesh'
    UTTARAKHAND = 'UK', 'Uttarakhand'
    WEST_BENGAL = 'WB', 'West Bengal'

    # Union Territories
    ANDAMAN_AND_NICOBAR = 'AN', 'Andaman & Nicobar Islands (UT)'
    CHANDIGARH = 'CH', 'Chandigarh (UT)'
    DADRA_AND_NAGAR_HAVELI_DAMAN_DIU = 'DN', 'Dadra & Nagar Haveli and Daman & Diu (UT)'
    DELHI = 'DL', 'Delhi (UT)'
    JAMMU_AND_KASHMIR = 'JK', 'Jammu & Kashmir (UT)'
    LADAKH = 'LA', 'Ladakh (UT)'
    LAKSHADWEEP = 'LD', 'Lakshadweep (UT)'
    PUDUCHERRY = 'PY', 'Puducherry (UT)'
    OTHER = 'OTHER', 'Other / International'


STATE_CITIES_MAP = {
    'AP': [
        'Adoni', 'Amalapuram', 'Anantapur', 'Bapatla', 'Bhimavaram', 'Bobbili',
        'Chirala', 'Chittoor', 'Dharmavaram', 'Eluru', 'Gudivada', 'Guntakal',
        'Guntur', 'Hindupur', 'Kadapa (YSR Kadapa)', 'Kakinada', 'Kavali',
        'Kurnool', 'Machilipatnam', 'Madanapalle', 'Mangalagiri', 'Markapur',
        'Nandyal', 'Narasapuram', 'Narasaraopet', 'Nellore', 'Nidadavole',
        'Ongole', 'Palakollu', 'Palasa-Kasibugga', 'Parvathipuram', 'Peddapuram',
        'Piduguralla', 'Pithapuram', 'Ponnur', 'Proddatur',
        'Rajamahendravaram (Rajahmundry)', 'Rajampet', 'Ramachandrapuram',
        'Rayachoti', 'Rayadurg', 'Renigunta', 'Salur', 'Samalkot',
        'Sattenapalle', 'Srikakulam', 'Tadepalligudem', 'Tadipatri', 'Tanuku',
        'Tenali', 'Tirupati', 'Tuni', 'Vijayawada', 'Visakhapatnam',
        'Vizianagaram', 'Yemmiganur'
    ],
    'AR': [
        'Aalo', 'Bomdila', 'Itanagar', 'Khonsa', 'Naharlagun', 'Namsai',
        'Pasighat', 'Roing', 'Seppa', 'Tawang', 'Tezu', 'Ziro'
    ],
    'AS': [
        'Barpeta', 'Bongaigaon', 'Dhubri', 'Dibrugarh', 'Diphu', 'Goalpara',
        'Golaghat', 'Guwahati', 'Hailakandi', 'Jorhat', 'Karimganj', 'Lanka',
        'Lumding', 'Mangaldoi', 'Margherita', 'Nagaon', 'Nalbari',
        'North Lakhimpur', 'Sibsagar', 'Silapathar', 'Silchar', 'Tezpur', 'Tinsukia'
    ],
    'BR': [
        'Arrah', 'Aurangabad', 'Bagaha', 'Begusarai', 'Bettiah', 'Bhabua',
        'Bhagalpur', 'Bihar Sharif', 'Buxar', 'Chapra', 'Darbhanga', 'Dehri',
        'Gaya', 'Hajipur', 'Jamalpur', 'Jamui', 'Katihar', 'Kishanganj',
        'Lakhisarai', 'Madhepura', 'Madhubani', 'Motihari', 'Munger',
        'Muzaffarpur', 'Nawada', 'Patna', 'Purnia', 'Saharsa', 'Samastipur',
        'Sasaram', 'Sheikhpura', 'Sitamarhi', 'Siwan', 'Supaul'
    ],
    'CG': [
        'Ambikapur', 'Bhilai', 'Bilaspur', 'Chirmiri', 'Dalli-Rajhara',
        'Dhamtari', 'Durg', 'Jagdalpur', 'Janjgir', 'Korba',
        'Mahasamund', 'Raigarh', 'Raipur', 'Rajnandgaon'
    ],
    'GA': [
        'Bicholim', 'Canacona', 'Curchorem', 'Mapusa', 'Margao', 'Mormugao',
        'Panaji', 'Ponda', 'Quepem', 'Sanguem', 'Valpoi', 'Vasco da Gama'
    ],
    'GJ': [
        'Ahmedabad', 'Amreli', 'Anand', 'Anjar', 'Bharuch', 'Bhavnagar',
        'Bhuj', 'Botad', 'Dahod', 'Deesa', 'Gandhidham', 'Gandhinagar',
        'Godhra', 'Himatnagar', 'Jamnagar', 'Jetpur', 'Junagadh', 'Kalol',
        'Mehsana', 'Modasa', 'Morbi', 'Nadiad', 'Navsari', 'Palanpur',
        'Patan', 'Porbandar', 'Rajkot', 'Surat', 'Surendranagar',
        'Vadodara', 'Valsad', 'Veraval', 'Vapi', 'Vyara'
    ],
    'HR': [
        'Ambala', 'Bahadurgarh', 'Bhiwani', 'Faridabad', 'Fatehabad',
        'Gurugram', 'Hisar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra',
        'Narnaul', 'Palwal', 'Panipat', 'Panchkula', 'Rewari', 'Rohtak',
        'Sirsa', 'Sonipat', 'Thanesar', 'Yamunanagar'
    ],
    'HP': [
        'Baddi', 'Bilaspur', 'Chamba', 'Dharamshala', 'Hamirpur', 'Kullu',
        'Mandi', 'Nahan', 'Palampur', 'Shimla', 'Solan', 'Una'
    ],
    'JH': [
        'Adityapur', 'Bokaro Steel City', 'Chaibasa', 'Chirkunda', 'Deoghar',
        'Dhanbad', 'Dumka', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh',
        'Jamshedpur', 'Lohardaga', 'Medininagar', 'Phusro', 'Ramgarh',
        'Ranchi', 'Sahibganj'
    ],
    'KA': [
        'Bagalkot', 'Ballari', 'Belagavi', 'Bengaluru', 'Bhadravati', 'Bidar',
        'Chamarajanagar', 'Chikkamagaluru', 'Chitradurga', 'Davanagere',
        'Gadag-Betageri', 'Gangavati', 'Hassan', 'Haveri', 'Hosapete',
        'Hubballi-Dharwad', 'Kalaburagi', 'Karwar', 'Kolar', 'Koppal',
        'Madikeri', 'Mandya', 'Mangaluru', 'Mysuru', 'Raichur',
        'Robertsonpet', 'Shivamogga', 'Tumakuru', 'Udupi', 'Vijayapura', 'Yadgir'
    ],
    'KL': [
        'Alappuzha', 'Attingal', 'Chalakudy', 'Kannur', 'Kasaragod', 'Kochi',
        'Kollam', 'Kottayam', 'Kozhikode', 'Manjeri', 'Nedumangad',
        'Neyyattinkara', 'Palakkad', 'Pathanamthitta', 'Payyannur', 'Ponnani',
        'Taliparamba', 'Thalassery', 'Thiruvananthapuram', 'Thrissur',
        'Tirur', 'Vadakara'
    ],
    'MP': [
        'Ashoknagar', 'Balaghat', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur',
        'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Guna',
        'Gwalior', 'Hoshangabad', 'Indore', 'Itarsi', 'Jabalpur', 'Katni',
        'Khandwa', 'Khargone', 'Mandsaur', 'Morena', 'Murwara', 'Neemuch',
        'Pithampur', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni',
        'Shahdol', 'Shajapur', 'Shivpuri', 'Singrauli', 'Ujjain', 'Vidisha'
    ],
    'MH': [
        'Ahilyanagar', 'Akola', 'Amravati', 'Aurangabad (Chhatrapati Sambhajinagar)',
        'Baramati', 'Beed', 'Bhandara', 'Bhiwandi', 'Bhusawal', 'Chandrapur',
        'Dhule', 'Gondia', 'Hinganghat', 'Hingoli', 'Ichalkaranji', 'Jalgaon',
        'Jalna', 'Kalyan', 'Karad', 'Kolhapur', 'Latur', 'Malegaon',
        'Mira-Bhayandar', 'Mumbai', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik',
        'Navi Mumbai', 'Osmanabad (Dharashiv)', 'Panvel', 'Parbhani',
        'Pimpri-Chinchwad', 'Pune', 'Ratnagiri', 'Sangli', 'Satara', 'Solapur',
        'Thane', 'Ulhasnagar', 'Vasai-Virar', 'Wardha', 'Washim', 'Yavatmal'
    ],
    'MN': ['Bishnupur', 'Churachandpur', 'Imphal', 'Kakching', 'Mayang Imphal', 'Moirang', 'Moreh', 'Thoubal'],
    'ML': ['Baghmara', 'Jowai', 'Nongpoh', 'Nongstoin', 'Resubelpara', 'Shillong', 'Tura', 'Williamnagar'],
    'MZ': ['Aizawl', 'Champhai', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saiha', 'Serchhip'],
    'NL': ['Dimapur', 'Kohima', 'Mokokchung', 'Mon', 'Phek', 'Tuensang', 'Wokha', 'Zunheboto'],
    'OR': [
        'Angul', 'Balangir', 'Balasore', 'Barbil', 'Bargarh', 'Baripada',
        'Berhampur', 'Bhadrak', 'Bhubaneswar', 'Brajarajnagar', 'Byasanagar',
        'Cuttack', 'Dhenkanal', 'Jeypore', 'Jharsuguda', 'Kendrapara',
        'Keonjhar', 'Paradip', 'Phulbani', 'Puri', 'Rayagada', 'Rourkela',
        'Sambalpur', 'Sunabeda'
    ],
    'PB': [
        'Abohar', 'Amritsar', 'Barnala', 'Batala', 'Bathinda', 'Faridkot',
        'Fatehgarh Sahib', 'Fazilka', 'Firozpur', 'Gurdaspur', 'Hoshiarpur',
        'Jalandhar', 'Kapurthala', 'Khanna', 'Kotkapura', 'Ludhiana',
        'Malerkotla', 'Malout', 'Mansa', 'Moga', 'Mohali', 'Muktsar',
        'Nabha', 'Pathankot', 'Patiala', 'Phagwara', 'Rajpura', 'Rupnagar',
        'Sangrur', 'Sunam'
    ],
    'RJ': [
        'Ajmer', 'Alwar', 'Balotra', 'Baran', 'Barmer', 'Beawar', 'Bharatpur',
        'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa',
        'Dholpur', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jhalawar', 'Jhunjhunu',
        'Jodhpur', 'Kishangarh', 'Kota', 'Nagaur', 'Pali', 'Sikar',
        'Sri Ganganagar', 'Tonk', 'Udaipur'
    ],
    'SK': ['Gangtok', 'Geyzing', 'Jorethang', 'Mangan', 'Namchi', 'Rangpo', 'Singtam'],
    'TN': [
        'Ambur', 'Arakkonam', 'Avadi', 'Chennai', 'Coimbatore', 'Cuddalore',
        'Dharmapuri', 'Dindigul', 'Erode', 'Hosur', 'Kanchipuram', 'Karur',
        'Kumbakonam', 'Madurai', 'Nagercoil', 'Namakkal', 'Pollachi',
        'Pudukkottai', 'Ranipet', 'Salem', 'Sivakasi', 'Tambaram',
        'Thanjavur', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
        'Tiruppur', 'Tiruvannamalai', 'Udhagamandalam', 'Vellore',
        'Viluppuram', 'Virudhunagar'
    ],
    'TG': [
        'Adilabad', 'Bodhan', 'Hyderabad', 'Jagtial', 'Karimnagar',
        'Khammam', 'Kothagudem', 'Mahabubnagar', 'Mancherial', 'Miryalaguda',
        'Nalgonda', 'Nizamabad', 'Ramagundam', 'Sangareddy', 'Siddipet',
        'Suryapet', 'Warangal'
    ],
    'TR': ['Agartala', 'Belonia', 'Dharmanagar', 'Kailashahar', 'Khowai', 'Pratapgarh', 'Udaipur'],
    'UP': [
        'Agra', 'Aligarh', 'Ambedkar Nagar (Akbarpur)', 'Amroha', 'Ayodhya',
        'Azamgarh', 'Bahraich', 'Ballia', 'Banda', 'Barabanki', 'Bareilly',
        'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli',
        'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad',
        'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hapur', 'Hardoi',
        'Hathras', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur', 'Kasganj',
        'Khurja', 'Lakhimpur', 'Lalitpur', 'Lucknow', 'Mainpuri', 'Mathura',
        'Mau', 'Meerut', 'Mirzapur', 'Modinagar', 'Moradabad', 'Muzaffarnagar',
        'Noida', 'Orai', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 'Raebareli',
        'Rampur', 'Saharanpur', 'Sambhal', 'Shahjahanpur', 'Shamli',
        'Shikohabad', 'Sitapur', 'Sultanpur', 'Unnao', 'Varanasi'
    ],
    'UK': [
        'Almora', 'Dehradun', 'Haldwani', 'Haridwar', 'Kashipur', 'Kotdwar',
        'Manglaur', 'Mussoorie', 'Nainital', 'Pithoragarh', 'Ramnagar',
        'Rishikesh', 'Roorkee', 'Rudrapur', 'Sitarganj', 'Srinagar', 'Vikasnagar'
    ],
    'WB': [
        'Alipurduar', 'Asansol', 'Baharampur', 'Balurghat', 'Bansberia', 'Bankura',
        'Baranagar', 'Bardhaman', 'Barrackpore', 'Basirhat', 'Bhatpara', 'Bidhannagar',
        'Chandannagar', 'Contai', 'Cooch Behar', 'Dankuni', 'Darjeeling', 'Dhulian',
        'Dinhata', 'Durgapur', 'English Bazar', 'Habra', 'Haldia', 'Howrah',
        'Jalpaiguri', 'Jangipur', 'Kalyani', 'Kanchrapara', 'Kharagpur', 'Kolkata',
        'Krishnanagar', 'Madhyamgram', 'Malda', 'Nabadwip', 'North Dumdum', 'Purulia',
        'Raiganj', 'Rajarhat', 'Ranaghat', 'Serampore', 'Shantipur', 'Siliguri',
        'South Dumdum', 'Tamluk', 'Titagarh', 'Uttarpara'
    ],
    'AN': ['Port Blair'],
    'CH': ['Chandigarh'],
    'DN': ['Daman', 'Diu', 'Silvassa'],
    'DL': ['Delhi', 'New Delhi'],
    'JK': ['Anantnag', 'Baramulla', 'Jammu', 'Kathua', 'Pulwama', 'Sopore', 'Srinagar', 'Udhampur'],
    'LA': ['Kargil', 'Leh'],
    'LD': ['Agatti', 'Kavaratti'],
    'PY': ['Karaikal', 'Mahe', 'Puducherry', 'Yanam'],
    'OTHER': []
}


def get_cities_for_state(state_code):
    return STATE_CITIES_MAP.get(state_code, [])


import pandas as pd


def safe_float(x):
    if isinstance(x, (int, float)):
        return x
    try:
        # Handle strings like "<0.1" by stripping the '<' and converting
        if isinstance(x, str) and x.startswith("<"):
            return float(x[1:])  # convert "0.1" to float
        return float(x)
    except (ValueError, TypeError):
        return None  # or np.nan


asia = [
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain",
    "Bangladesh", "Bhutan", "Brunei",
    "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia",
    "Iran", "Iraq", "Israel",
    "Japan", "Jordan", "Kazakhstan", "Kuwait",
    "Kyrgyzstan", "Laos", "Lebanon", "Malaysia",
    "Maldives", "Mongolia", "Myanmar (Burma)", "Nepal",
    "North Korea", "Oman", "Pakistan",
    "Palestine", "Philippines", "Qatar",
    "Saudi Arabia", "Singapore", "South Korea",
    "Sri Lanka", "Syria", "Taiwan", "Tajikistan",
    "Thailand", "Timor-Leste", "Turkey",
    "Turkmenistan", "United Arab Emirates",
    "Uzbekistan", "Vietnam", "Yemen"
]
africa = [
    "Algeria", "Angola", "Benin", "Botswana",
    "Burkina Faso", "Burundi", "Cabo Verde",
    "Cameroon", "Central African Republic",
    "Chad", "Comoros", "Republic of the Congo",
    "Democratic Republic of the Congo",
    "Côte d'Ivoire", "Djibouti", "Egypt",
    "Equatorial Guinea",
    "Eritrea", "Eswatini", "Ethiopia", "Gabon",
    "Gambia", "Ghana", "Guinea", "Guinea-Bissau",
    "Kenya", "Lesotho", "Liberia", "Libya",
    "Madagascar", "Malawi", "Mali", "Mauritania",
    "Mauritius", "Morocco", "Mozambique",
    "Namibia", "Niger", "Nigeria", "Rwanda",
    "São Tomé and Príncipe", "Senegal",
    "Seychelles", "Sierra Leone", "Somalia", "South Africa",
    "South Sudan", "Sudan", "Tanzania",
    "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]
europe = [
    "Albania", "Andorra", "Austria", "Belarus",
    "Belgium", "Bosnia and Herzegovina",
    "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland",
    "France", "Germany", "Greece", "Hungary",
    "Iceland", "Ireland", "Italy", "Kosovo",
    "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco",
    "Montenegro", "Netherlands",
    "North Macedonia", "Norway", "Poland", "Portugal",
    "Romania", "Russia", "San Marino",
    "Serbia", "Slovakia", "Slovenia", "Spain",
    "Sweden", "Switzerland", "Ukraine", "United Kingdom"
]
north_america = [
    "Antigua and Barbuda", "Bahamas", "Barbados",
    "Belize", "Canada", "Costa Rica",
    "Cuba", "Dominica", "Dominican Republic",
    "El Salvador", "Grenada", "Guatemala",
    "Haiti", "Honduras", "Jamaica", "Mexico",
    "Nicaragua", "Panama", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines",
    "Trinidad and Tobago", "United States"
]
south_america = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana",
    "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"
]


def find_continents(stri):
    if stri in europe:
        return 'Europe'
    if stri in asia:
        return 'Asia'
    if stri in africa:
        return 'Africa'
    if stri in north_america:
        return 'North_America'
    if stri in south_america:
        return 'South_America'


def replace_none(x):
    return "index" if pd.isna(x) else x


def is_float(x):
    try:
        float(x)
        return True
    except (ValueError, TypeError):
        return False

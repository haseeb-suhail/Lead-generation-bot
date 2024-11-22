from selenium.webdriver.support.wait import WebDriverWait
import csv
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import certifi
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome
from selenium.webdriver.support import expected_conditions as EC

state_names_abbreviations = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'American Samoa': 'AS',
                             'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
                             'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU',
                             'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
                             'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
                             'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
                             'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
                             'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
                             'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK',
                             'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI',
                             'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
                             'Trust Territories': 'TT', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI',
                             'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI',
                             'Wyoming': 'WY'}


def match_location(locations, city, state):
    for loc in locations:
        print(loc)
        return True
    return False


def search_page(first_name, middle_name, last_name, city, state, row, driver, output, is_time_out):
    result_blocks = None
    try:
        result_blocks = driver.find_elements(By.CLASS_NAME, 'success-wrapper-block')
    except:
        print("No results appear")
        pass

    profiles_data = []

    if result_blocks:
        for result_block in result_blocks:
            try:
                profile_url = result_block.find_element(By.XPATH, 'div/div/a').get_attribute('href')
                sk_full_name_element = result_block.find_element(By.XPATH, 'div/div/h3')
                sk_full_name_text = sk_full_name_element.text.strip()

                sk_first_name = sk_middle_name = sk_last_name = sk_age = None
                if 'age' in sk_full_name_text.lower():
                    req_sk_full_name = sk_full_name_text.split('Age')[0].strip().replace(',', '')
                    sk_age = sk_full_name_text.split('Age')[-1].strip()
                else:
                    req_sk_full_name = sk_full_name_text

                temp_sk_full_name = req_sk_full_name.split(' ')
                sk_first_name = temp_sk_full_name[0]
                sk_last_name = temp_sk_full_name[-1]
                if len(temp_sk_full_name) > 2:
                    sk_middle_name = ' '.join(temp_sk_full_name[1:-1])

                live_locations = result_block.find_element(By.XPATH, './/div[contains(text(), "Lives in:")]')
                used_locations_element = result_block.find_element(By.XPATH,
                                                                   './/div[contains(text(), "Prior addresses:")]/following-sibling::div')

                locations = []
                if live_locations:
                    locations.append(live_locations.text.replace('Lives in:', '').strip().replace(', ', ' '))
                if used_locations_element:
                    used_locations_text = used_locations_element.text.strip().split(', ')
                    locations += used_locations_text

                profiles_data.append(
                    [req_sk_full_name, sk_first_name, sk_middle_name, sk_last_name, sk_age, locations, profile_url])
            except:
                pass

        print(profiles_data)

        try:
            state = state
            print("Target Location", state)

            for data in profiles_data:
                first_name = data[1]
                middle_name = data[2]
                last_name = data[3]
                locations = data[-2]
                profile_url = data[-1]

                print("First name:", first_name)
                print("Middle name:", middle_name)
                print("Last name:", last_name)
                print("Locations:", locations)
                print("Profile URL:", profile_url)

                if match_location(locations, city, state):
                    print("Data match")
                    try:
                        driver.get(profile_url)
                        sleep(1.5)
                    except:
                        is_time_out = True
                        data_export('', row, driver, output, is_time_out)
                        return
                    data_export('', row, driver, output, is_time_out)
                    return
                elif state in locations:
                    print("State match, but city doesn't match")
                    continue

                print("Data does not match")

            # If no match is found, export old information without any new information
            data_export('', row, driver, output, is_time_out)

        except Exception as e:
            print("Error:", e)

    else:
        print("No results found on page")


# ***********************************************Code 1 for Ohio Residents Site to get All Persons Detail******************************************************

def data_export(age, row, driver, output, is_time_out):
    required_previous_address = req_current_contact_wireless = req_current_contact_landline = required_previous_contact_wireless = required_previous_contact_landline = positions = Educations = \
        Company_Names = required_email = None
    with (open(output, 'a', newline='') as final_csv):

        final_csv_writer = csv.writer(final_csv)
        # Check if the file is empty (no headers)
        file_empty = final_csv.tell() == 0

        # Write the header row if the file is empty
        if file_empty:
            headers = ['first_name', 'middle_name', 'last_name', 'BirthYear', 'Address', 'city', 'state', 'AddressZip',
                       'VoterIdent', 'Date_of_birth', 'Net_Worth', 'Salary', 'Registered_vote', 'Registration_Date',
                       'Voter_status', 'Precinct', 'Precinct_code', 'Career_Center', 'Congressional_District',
                       'State_Representative_District',
                       'State_Senate_District', 'Township',
                       'current_location', 'SK Previous Addresses', 'req_current_contact_wireless',
                       'req_current_contact_landline', 'required_previous_contact_wireless',
                       'required_previous_contact_landline', 'Postion', 'Educations', 'Company_Names(Perdicted)',
                       'required_email']

            final_csv_writer.writerow(headers)
        if not is_time_out:
            try:
                driver.execute_script('window.scrollBy(0,500)')

            except Exception as x:
                print('no show more found...', x)

            # current addresses
            try:

                Current_Address = driver.find_element(By.XPATH, "//p[@class='ls_contacts__text']")
            except NoSuchElementException:
                try:
                    # If the first XPath fails, attempt to find the element by the second XPath
                    Current_Address = driver.find_element(By.XPATH,
                                                          "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/a[2]/p")
                except NoSuchElementException:
                    # If both XPaths fail, handle the NoSuchElementException
                    print('Error in getting addresses')
                    Current_Address = None

                # Check if Current_Address is found before attempting to access its text
            if Current_Address is not None:
                Current_Address = Current_Address.text
                print('Current Address: ', Current_Address)
            else:

                print('Current Address not found or could not be retrieved.')
            try:

                click_on = driver.find_element(By.CSS_SELECTOR, '.show-more:nth-child(12) .show-text')
                click_on.click()
                previous_address_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'shown')))
                # If found, get the list items within it
                previous_address = previous_address_element.find_elements(By.TAG_NAME, 'li')
                # Initialize a list to store the previous addresses
                required_previous_address = []
                for pd in previous_address:
                    # Append each previous address text to the list
                    required_previous_address.append(pd.text.strip())

                # Join the list items with a separator
                required_previous_address = ' | '.join(required_previous_address)
                print('Previous Addresses: ', required_previous_address)

            except TimeoutException:

                # Handle the case where the element with class 'shown' is not found
                print('Timeout: Element with class "shown" not found')

            except NoSuchElementException:

                # Handle the case where any other element is not found
                try:

                    # Attempt to retrieve the previous addresses using an alternate method
                    address = driver.find_element(By.CSS_SELECTOR, 'ul:nth-child(11) a').text.strip()
                    address2 = driver.find_element(By.CSS_SELECTOR, 'ul:nth-child(11) li+ li a').text.strip()
                    required_previous_address = address + '| ' + address2
                    print("print_previous", required_previous_address)

                except NoSuchElementException:

                    # Handle the case where the alternate method also fails
                    print('Error in getting previous addresses')


                except Exception as e:
                    # Handle any other unexpected exceptions

                    print('Unexpected error:', e)
            print(
                "****************PreviousAddressed*******************************************************************************************")

            try:
                # Find and click on the second "Show More" button
                req_current_contact_landline = None
                req_current_contact_wireless = None  # Assuming you want to initialize both variables

                current_contact_element = driver.find_element(By.CSS_SELECTOR, ".ls_success-link span")
                if current_contact_element:
                    parent_current_contact = current_contact_element.find_element(By.XPATH, '..')
                    parent_current_contact = parent_current_contact.find_element(By.XPATH, '..')
                    parent_current_contact_text = parent_current_contact.text
                    if 'landline' in parent_current_contact_text.lower():
                        req_current_contact_landline = parent_current_contact_text.replace('- LandLine', '').strip()
                    else:

                        req_current_contact_wireless = parent_current_contact_text.replace('- Wireless', '').strip()

                print("Wireless : ", req_current_contact_wireless, "\nLandline : ", req_current_contact_landline)
            except NoSuchElementException:
                try:

                    req_current_contact_landline = None
                    req_current_contact_wireless = None  # Assuming you want to initialize both variables

                    current_contact_element = driver.find_element(By.XPATH,
                                                                  "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/p/a/span")
                    if current_contact_element:

                        parent_current_contact = current_contact_element.find_element(By.XPATH, '..')
                        parent_current_contact = parent_current_contact.find_element(By.XPATH, '..')
                        parent_current_contact_text = parent_current_contact.text
                        if 'landline' in parent_current_contact_text.lower():
                            req_current_contact_landline = parent_current_contact_text.replace('- LandLine', '').strip()
                        else:
                            req_current_contact_wireless = parent_current_contact_text.replace('- Wireless', '').strip()

                    print("Wireless : ", req_current_contact_wireless, "\nLandline : ", req_current_contact_landline)
                except NoSuchElementException:
                    print('Error in getting current Number')

                except Exception as e:
                    # Handle any other unexpected exceptions

                    print('Unexpected error:', e)
            print("**********************Current Contact Number********************")

            try:

                try:

                    onclick1 = driver.find_element(By.CSS_SELECTOR, '.show-more:nth-child(15) .show-text')
                    onclick1.click()
                    required_previous_contact_wireless = []
                    required_previous_contact_landline = []

                    # Attempt to find phone elements with itemprop="telephone"
                    phone_elements = driver.find_elements(By.CSS_SELECTOR, 'li[itemtype="https://schema.org/Person"]')

                    for element in phone_elements:
                        try:
                            phone_number = element.find_element(By.CSS_SELECTOR, 'a[itemprop="telephone"]').text.strip()
                            phone_type = element.text.strip().split('\n')[-1]

                            if 'landline' in phone_type.lower():
                                required_previous_contact_landline.append(phone_number)
                            else:
                                required_previous_contact_wireless.append(phone_number)


                        except:

                            print('Error in getting numbers')

                    required_previous_contact_wireless = ', '.join(required_previous_contact_wireless)
                    required_previous_contact_landline = ', '.join(required_previous_contact_landline)
                    print('\nWireless : ', required_previous_contact_wireless)
                    print('Landlines : ', required_previous_contact_landline)

                except Exception as e:
                    print('Error:', e)

            except NoSuchElementException:
                try:

                    required_previous_contact_wireless = []
                    required_previous_contact_landline = []

                    # Attempt to find the first phone number element
                    phone1 = \
                        driver.find_element(By.CSS_SELECTOR, '.show-more~ ul li:nth-child(1) a').text.strip().split(
                            "\n")[
                            -1]

                    # Check if the phone number is a landline or wireless
                    if 'Landline' in phone1:
                        required_previous_contact_landline.append(phone1)
                    else:
                        required_previous_contact_wireless.append(phone1)

                    # Attempt to find the second phone number element
                    phone2 = driver.find_element(By.CSS_SELECTOR, '.show-more~ ul a').text.strip().split("\n")[-1]

                    # Check if the phone number is a landline or wireless
                    if 'Landline' in phone2:
                        required_previous_contact_landline.append(phone2)
                    else:
                        required_previous_contact_wireless.append(phone2)

                    # Print the collected phone numbers
                    print('\nWireless :', required_previous_contact_wireless)
                    print('Landlines :', required_previous_contact_landline)

                except NoSuchElementException:
                    print("No telephone element found for this entry.")
                except Exception as e:
                    print('Error in getting numbers:', e)

            except Exception as e:
                print('Not append data:', e)

            print("***********************************previous Number*****************************************")
            try:

                # If the first XPath fails, attempt to find the element by the second XPath
                position = driver.find_element(By.XPATH,
                                               '//div[@class="relative-card workplace"]/p[2]')
            except NoSuchElementException:
                # If both XPaths fail, handle the NoSuchElementException
                print('Error in getting addresses')
                position = None

            # Check if Current_Address is found before attempting to access its text
            if position is not None:
                positions = position.text
                print('designation: ', positions)
            else:
                print('Current Address not found or could not be retrieved.')
            print(

                "***********************************Podition Of Employee**************************************************************")
            try:

                # If the first XPath fails, attempt to find the element by the second XPath
                Education = driver.find_element(By.CSS_SELECTOR,
                                                '.workplace-education > p')
            except NoSuchElementException:
                # If both XPaths fail, handle the NoSuchElementException
                print('Error in getting addresses')
                Education = None

            # Check if Current_Address is found before attempting to access its text
            if Education is not None:
                Educations = Education.text.replace('Education:', '')
                print('designation: ', Educations)
            else:

                print('Current Address not found or could not be retrieved.')
            print(

                "***********************************Podition Of Employee**************************************************************")
            try:

                # If the first XPath fails, attempt to find the element by the second XPath
                Company_Name = driver.find_element(By.CSS_SELECTOR,
                                                   'p.companyName')
            except NoSuchElementException:
                # If both XPaths fail, handle the NoSuchElementException
                print('Error in getting Company_Name')
                Company_Name = None

            # Check if Current_Address is found before attempting to access its text
            if Company_Name is not None:
                Company_Names = Company_Name.text
                print('Company_Names: ', Company_Names)
            else:
                print('Company_Name not found or could not be retrieved.')
            print(
                "***********************************Company Of Employee**************************************************************")
            required_email = []
            try:
                emails = driver.find_elements(By.PARTIAL_LINK_TEXT, '@')
                if emails:
                    for email in emails:
                        required_email += [email.text]

            except:
                pass

            required_email = '| '.join(required_email)
            print('\nEmail : ', required_email)
            print(
                '--------------------------------------------------------')

            # Construct the final row data
            final_row = [
                row[0],  # First Name
                row[1],  # Middle Name
                row[2],  # Last Name
                row[3],  # Birth Year

                row[4],  # Address
                row[5],  # City
                row[6],  # State
                row[7],  # Address Zip
                row[8],
                row[9],  # Voter Ident

                row[10],
                row[11],
                row[12],
                row[13],
                row[14],
                row[15],
                row[16],
                row[17],

                row[18],
                row[19],
                row[20],
                row[21],

                Current_Address,
                required_previous_address,

                req_current_contact_wireless,
                req_current_contact_landline,
                required_previous_contact_wireless,

                required_previous_contact_landline,
                positions,
                Educations,
                Company_Names,
                required_email]

            # save data in csv file
            final_csv_writer.writerow(final_row)
            print("Data save to csv")


# ***********************************************Code 1 for Ohio Residents Site Main_Page******************************************************

def main(input, output, driver):
    print('main working')

    try:
        with open(input, mode="r") as file:
            reader = csv.reader(file)
            n = next(reader)
            count = 0
            print("reader")
            for row in reader:
                is_time_out = False
                First_Name = row[0]
                middle_name = row[1]
                Last_Name = row[2]
                BirthYear = row[3]
                Address = row[4]
                city = row[5]
                state = row[6]
                AddressZip = row[7]
                VoterIdent = row[8]
                date_of_birth = row[9]
                Net_Worth = row[10]
                Salary = row[11]
                Registered_vote = row[12]
                Registration_Date = row[13]
                Voter_status = row[14]
                Precinct = row[15]
                Precinct_code = row[16]
                Career_Center = row[17]
                Congressional_District = row[18]
                State_Representative_District = row[19]
                State_Senate_District = row[20]
                Township = row[21]

                print("First Name", First_Name)
                print("middle_name", middle_name)
                print("Last Name", Last_Name)
                print("BirthYear", BirthYear)
                print("Address", Address)
                print("City", city)
                # print("State", state)
                print("AddressZip", AddressZip)
                print("VoterIdent", VoterIdent)
                print("date_of_birth", date_of_birth)
                print("Net_Worth", Net_Worth)
                print("Salary", Salary)
                print("Net_Worth", Registered_vote)
                print("Registration_Date", Registration_Date)
                print("Voter_status", Voter_status)
                print("Precinct", Precinct)
                print("Precinct_code", Precinct_code)
                print("Career_Center", Career_Center)
                print("Congressional_District", Congressional_District)
                print("State_Representative_District", State_Representative_District)
                print("State_Senate_District", State_Senate_District)
                print("Township", Township)

                try:
                    #U CARE ABT TIS SHIT
                    print("State", state)
                    full_state_name = None
                    if First_Name and Last_Name:
                        if state in state_names_abbreviations.values():
                            full_state_name = [k for k, v in state_names_abbreviations.items() if v == state][0]
                        if full_state_name:
                            # url = f'https://www.usphonebook.com/{First_Name.strip().lower()}-{middle_name.strip().lower()}-{Last_Name.strip().lower()}/{state.strip().lower()}'
                            url = f'https://www.usphonebook.com/{First_Name.strip().lower()}-{middle_name.strip().lower()}-{Last_Name.strip().lower()}/{state.strip().lower()}/{city.strip().lower()}'
                        else:
                            url = f'https://www.usphonebook.com/{First_Name.strip().lower()}-{middle_name.strip().lower()}-{Last_Name.strip().lower()}/{state.strip().lower()}'
                        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        try:
                            sleep(1)
                            driver.refresh()
                            sleep(2)
                            try:
                                driver.get(url)
                            except:
                                is_time_out = True
                                data_export('', row, driver, output, is_time_out)
                                continue
                            print(url)
                            sleep(3)
                            search_page(First_Name, middle_name, Last_Name, city, state, row, driver, output,
                                        is_time_out)
                        # search_page(First_Name, middle_name, Last_Name, city, state, row, driver, output, is_time_out)
                        except Exception as e:
                            print(e)
                            continue
                    else:
                        try:
                            is_time_out = True
                            driver.get('https://www.usphonebook.com/')

                            driver.maximize_window()
                            url = 'https://www.usphonebook.com/John-Doe/alabama/cumberland'
                            driver.get(url)
                            sleep(10)
                        except:
                            pass
                        sleep(2)
                        data_export('', row, driver, output, is_time_out)
                except:
                    pass


    except Exception as e:
        print(e)

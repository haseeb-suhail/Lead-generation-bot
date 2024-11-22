import scrapy
import csv
from ..items import OhioResidentItem


class OhioResidentSpider(scrapy.Spider):
    name = 'ohio_resident_spider'
    allowed_domains = ["ohioresidentdatabase.com"]

    state_names_abbreviations = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'American Samoa': 'AS', 'California': 'CA', 'Colorado': 'CO',
        'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
        'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI',
        'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
        'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
        'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
        'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
        'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
        'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI',
        'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
        'Trust Territories': 'TT', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }  # Your state abbreviations dictionary

    def start_requests(self):
        # here give your input csv in my case it is Voter_information file
        with open('Week_11_4_Usman.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                First_Name, middle_name, Last_Name, BirthYear, Address, city, state, AddressZip, VoterIdent = row

                url = self.construct_url(First_Name, Last_Name, city, state)

                yield scrapy.Request(url, callback=self.search_page, meta={'row': row})

    def construct_url(self, First_Name, Last_Name, city, state):
        state = state.strip()
        full_state_name = self.state_names_abbreviations.get(state)
        if full_state_name:
            return f'https://www.ohioresidentdatabase.com/name/{First_Name.strip().lower()}-{Last_Name.strip().lower()}/{city.strip().lower()}'
        else:
            return f'https://www.ohioresidentdatabase.com/name/{First_Name.strip().lower()}-{Last_Name.strip().lower()}/{city.strip().lower()}'

    def search_page(self, response):
        row = response.meta['row']
        First_Name, middle_name, Last_Name, BirthYear, Address, city, state, AddressZip, VoterIdent = row

        # row_found = False

        total_results_element = response.xpath('//*[@id="search-results"]/h1/text()').get()
        if total_results_element:
            total_results = int(total_results_element.split()[0])
            print(total_results)

            row_found = False
            for i in range(1, total_results + 1):
                name_element = response.xpath(f'//a[{i}]/h3[@itemprop="name"]/text()')
                name = name_element.get().strip().lower()
                print('name.............', name)
                dob_element = response.xpath(f'//div[{i}]/div[1]//p[strong[contains(text(),"Age:")]]/text()')
                dob = dob_element.get().strip().replace(")", '').split()[-1]
                print('dob.....................', dob)
                if (name == f"{First_Name.lower().strip()} {middle_name.lower().strip()} {Last_Name.lower().strip()}" or
                        name == f"{First_Name.strip().lower()} {Last_Name.strip().lower()}"):
                    if dob == str(BirthYear):
                        view_page_link = response.xpath(
                            f'//*[@id="search-results"]/div[{i}]/div[2]/div[1]/div/a/@href').get()
                        if view_page_link:
                            yield response.follow(view_page_link, callback=self.parse_details, meta={'row': row})
                            row_found = True
                            break

        if not row_found:
            yield self.data_export(row)

    def parse_details(self, response):
        row = response.meta['row']
        First_Name, middle_name, Last_Name, BirthYear, Address, city, state, AddressZip, VoterIdent = row
        # First_Name = middle_name = Last_Name = BirthYear = Address = city = state = AddressZip = VoterIdent = dob_text = Net_Worth = Salary = None
        # Extract details from the detail page using corrected XPath selectors
        dob_text = response.xpath('//*[@id="person-data-wrapper"]/div[2]/div/div[2]/p/text()').get()
        Net_Worth = response.xpath('//p/strong[contains(text(), "Net Worth")]/following-sibling::text()').get()
        Salary = response.xpath('//*[@id="person-data-wrapper"]/p[1]/text()').get()
        Registered_vote = response.xpath(
            '//p/strong[contains(text(), "Registered to vote in")]/following-sibling::text()').get()
        Registration_Date = response.xpath(
            '//p/strong[contains(text(), "Registration Date")]/following-sibling::text()').get()
        Voter_status = response.xpath('//p/strong[contains(text(), "Voter Status")]/following-sibling::text()').get()
        Precinct = response.xpath('//p/strong[contains(text(), "Precinct")]/following-sibling::text()').get()
        Precinct_code = response.xpath('//p/strong[contains(text(), "Precinct Code")]/following-sibling::text()').get()
        Career_Center = response.xpath('//p/strong[contains(text(), "Career Center")]/following-sibling::text()').get()
        Congressional_District = response.xpath(
            '//p/strong[contains(text(), "Congressional District")]/following-sibling::text()').get()
        State_Representative_District = response.xpath(
            '//p/strong[contains(text(), "State Representative District")]/following-sibling::text()').get()
        State_Senate_District = response.xpath(
            '//p/strong[contains(text(), "State Senate District")]/following-sibling::text()').get()
        Township = response.xpath('//p/strong[contains(text(), "Township")]/following-sibling::text()').get()

        # Create an instance of OhioResidentItem and populate it with scraped data
        item = OhioResidentItem(
            First_Name=First_Name,
            middle_name=middle_name,
            Last_Name=Last_Name,
            BirthYear=BirthYear,
            Address=Address,
            city=city,
            state=state,
            AddressZip=AddressZip,
            VoterIdent=VoterIdent,
            dob_text=dob_text.strip() if dob_text is not None else '',
            Net_Worth=Net_Worth.strip() if Net_Worth is not None else '',
            Salary=Salary.strip() if Salary is not None else '',
            Registered_vote=Registered_vote.strip().split(":")[-1] if Registered_vote is not None else '',
            Registration_Date=Registration_Date.strip().split(":")[-1] if Registration_Date is not None else '',
            Voter_status=Voter_status.strip().split(":")[-1] if Voter_status is not None else '',
            Precinct=Precinct.strip().split(":")[-1] if Precinct is not None else '',
            Precinct_code=Precinct_code.strip().split(":")[-1] if Precinct_code is not None else '',
            Career_Center=Career_Center.strip().split(":")[-1] if Career_Center is not None else '',
            Congressional_District=Congressional_District.strip().split(":")[
                -1] if Congressional_District is not None else '',
            State_Representative_District=State_Representative_District.strip().split(":")[
                -1] if State_Representative_District is not None else '',
            State_Senate_District=State_Senate_District.strip().split(":")[
                -1] if State_Senate_District is not None else '',
            Township=Township.strip().split(":")[-1] if Township is not None else ''
        )

        yield item

    def data_export(self, row):
        # Create an instance of OhioResidentItem with empty strings for missing data
        item = OhioResidentItem(
            First_Name=row[0],
            middle_name=row[1],
            Last_Name=row[2],
            BirthYear=row[3],
            Address=row[4],
            city=row[5],
            state=row[6],
            AddressZip=row[7],
            VoterIdent=row[8],
            dob_text='',
            Net_Worth='',
            Salary='',
            Registered_vote='',
            Registration_Date='',
            Voter_status='',
            Precinct='',
            Precinct_code='',
            Career_Center='',
            Congressional_District='',
            State_Representative_District='',
            State_Senate_District='',
            Township=''
            # Populate other fields similarly
        )

        return item

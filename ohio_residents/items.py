# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OhioResidentItem(scrapy.Item):
    # Define the fields for your item here like:
    First_Name = scrapy.Field()
    middle_name = scrapy.Field()
    Last_Name = scrapy.Field()
    BirthYear = scrapy.Field()
    Address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    AddressZip = scrapy.Field()
    VoterIdent = scrapy.Field()
    dob_text = scrapy.Field()
    Net_Worth = scrapy.Field()
    Salary = scrapy.Field()
    Registered_vote = scrapy.Field()
    Registration_Date = scrapy.Field()
    Voter_status = scrapy.Field()
    Precinct = scrapy.Field()
    Precinct_code = scrapy.Field()
    Career_Center = scrapy.Field()
    Congressional_District = scrapy.Field()
    State_Representative_District = scrapy.Field()
    State_Senate_District = scrapy.Field()
    Township = scrapy.Field()

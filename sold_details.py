import requests
import csv
from bs4 import BeautifulSoup
import re

ACRES_TO_SQFT = 43560

def parse_baths(baths):
    bath_list = baths.split(" ")
    return bath_list[0], bath_list[2]

def parse_datetime(date):
    #print(date)
    dates = date.split("/")
    return dates[0] + "/20" + dates[2]

def create_street_name(street):
    output_name = ""
    street_names = street.split(" ")
    for name in street_names[1:]:
        output_name = output_name + " " + name
    return output_name[1:]
    
def parse_two(address):
    cities = address.split(",")
    # print(cities)
    return cities[0], cities[1][1:] # Splice [1:] to remove the extra space

def parse_styles(style):
    if len(style) > 1:
        return style[0], style[1][1:] # Splice [1:] to remove the extra space
    elif len(style) == 1:
        return style[0], style[0]    

def parse_one(feature):
    return feature[0]
'''
PARSE CHECKLIST
1. Correct page in || for home in range([num]) ||?
2. urls Correct?
3. ids Correct?
'''

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
ids = 7025 ## 0

for home in range(13):
    print(f" *** At page {home+1} ***")
    # Page 1, doesn't have the .../1_p/?SearchQueryState...
    if home == 0:
        url = "https://www.zillow.com/odenton-md/sold/house,condo,apartment_duplex,townhouse_type/1-_beds/1.0-_baths/?searchQueryState={%22pagination%22:{},%22usersSearchTerm%22:%22Odenton%22,%22mapBounds%22:{%22west%22:-76.72034447847449,%22east%22:-76.6866130179032,%22south%22:39.06405674548125,%22north%22:39.08362694743152},%22regionSelection%22:[{%22regionId%22:29211,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:15,%22filterState%22:{%22beds%22:{%22min%22:1},%22baths%22:{%22min%22:1},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isRecentlySold%22:{%22value%22:true},%22isManufactured%22:{%22value%22:false},%22isLotLand%22:{%22value%22:false}},%22isListVisible%22:true}"
    elif home > 0:
        # " + str(home+1) + "
        # url = "https://www.zillow.com/bowie-md/sold/house,condo,apartment_duplex,townhouse_type/1-_beds/1.0-_baths/" + str(home+1) + "_p/?searchQueryState={%22pagination%22:{%22currentPage%22:" + str(home+1) + "},%22mapBounds%22:{%22west%22:-76.82545620569698,%22east%22:-76.7579932845544,%22south%22:38.98411163016077,%22north%22:39.02329090660128},%22regionSelection%22:[{%22regionId%22:30552,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:14,%22filterState%22:{%22price%22:{%22min%22:10000},%22monthlyPayment%22:{%22min%22:37},%22beds%22:{%22min%22:1},%22baths%22:{%22min%22:1},%22sqft%22:{%22min%22:500},%22lotSize%22:{%22min%22:1000},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isRecentlySold%22:{%22value%22:true},%22isManufactured%22:{%22value%22:false},%22isLotLand%22:{%22value%22:false}},%22isListVisible%22:true}"
        url = "https://www.zillow.com/odenton-md/sold/house,condo,apartment_duplex,townhouse_type/1-_beds/1.0-_baths/" + str(home+1) + "_p/?searchQueryState={%22pagination%22:{%22currentPage%22:" + str(home+1) + "},%22usersSearchTerm%22:%22Odenton%22,%22mapBounds%22:{%22west%22:-76.72034447847449,%22east%22:-76.6866130179032,%22south%22:39.06405674548125,%22north%22:39.08362694743152},%22regionSelection%22:[{%22regionId%22:29211,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:15,%22filterState%22:{%22beds%22:{%22min%22:1},%22baths%22:{%22min%22:1},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isRecentlySold%22:{%22value%22:true},%22isManufactured%22:{%22value%22:false},%22isLotLand%22:{%22value%22:false}},%22isListVisible%22:true}"
    
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    
    print(f"Starting at {ids}")
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    content_details = []
    houses_specs = []

    zillow_detatil = soup.find_all("a", attrs={"href": re.compile("^https://www.zillow.com/homedetails/")})

    # The homedetail obtains two copies of every link, so skip every other index.
    for links in zillow_detatil[::2]:
        content_details.append(links.get("href"))

    for j in range(len(content_details)):
        zillows = requests.get(content_details[j], headers=headers)
        z_soup = BeautifulSoup(zillows.content, "html.parser")
        print(f"Scraping: {content_details[j]}\n")

        address_header   = z_soup.find(class_="zsg-h1 hdp-home-header-st-addr")
        addresses        = z_soup.find(class_="zsg-h2")
        price_sold       = z_soup.find(class_="status")
        bed_bath_beyond  = z_soup.find(class_="edit-facts-light")
        date_sold        = z_soup.find(class_="zsg-fineprint date-sold")
        property_details = z_soup.find(class_="hdp-facts zsg-content-component")

        home_type_flag, year_flag, heating_flag, cooling_flag     = False, False, False, False
        bedroom_flag, bathroom_flag, fullBath_flag, halfBath_flag = False, False, False, False
        basement_flag, floor_size_flag, stories_flag              = False, False, False
        architecture_flag, roof_flag, exterior_flag               = False, False, False
        construct_mat_flag, flooring_flag                         = False, False

        if address_header is None:
            print(" -- Sold house has nothing in it. Skip over -- ")
            print("Address soup,", addresses)
            print("Address header soup,", address_header)
            print()
            continue

        street_name = create_street_name(str(list(address_header.strings)[0]))

        address = str(list(address_header.strings)[0]) + ", " + str(list(addresses.strings)[0]) ## 1
        region, zipcode = parse_two(str(list(addresses.strings)[0]))  ## 2 ## 3
        bath_totals = list(bed_bath_beyond.strings)[3]
        bath_rooms = parse_one(bath_totals)
        floor_size = list(bed_bath_beyond.strings)[-1][:-5].replace(",", "")
        list_price = list(price_sold.strings)[-1] ## 4

        monthYear_sold = parse_datetime(list(date_sold.strings)[-1]) ## 5

        for i in range(len(list(property_details.strings))):
            if list(property_details.strings)[i] == "Type":
                home_type = list(property_details.strings)[i+2] ## 6
                home_type_flag = True
                print("Correct home type?:", home_type)
            if list(property_details.strings)[i] == "Year Built":
                year_built = list(property_details.strings)[i+2] ## 7
                year_flag = True
                print("Correct year?:", year_built)

            if list(property_details.strings)[i] == "Heating":
                heating = list(property_details.strings)[i+2] ## 8
                heating_flag = True
                print("Correct heating:", heating)
            if list(property_details.strings)[i] == "Cooling":
                cooling = list(property_details.strings)[i+2] ## 9
                cooling_flag = True
                print("Correct cooling?:", cooling)

            if list(property_details.strings)[i] == "Lot:":
                lot_size = list(property_details.strings)[i+2] ## 11
                print("Correct lot size?:", lot_size)       
                if lot_size[-5:] == "acres":
                    lot_size = float(lot_size[:-5].replace(",", ""))
                    lot_size = lot_size * ACRES_TO_SQFT 
                    print("Acres to sqft:", lot_size)
                else:
                    lot_size = int(lot_size[:-5].replace(",", ""))
                lot_size_flag = True
            if list(property_details.strings)[i] == "Beds:":
                bedrooms = list(property_details.strings)[i+2] ## 12
                bedroom_flag = True
                print("Correct num of bedrooms?:", bedrooms) 

            if list(property_details.strings)[i] == "Baths:":
                bathrooms = list(property_details.strings)[i+2] ## 13
                bathrooms_flag = True
                if bathrooms_flag == True:
                    print("Correct num of bedrooms?:", bathrooms)      
                    full_baths, half_baths = parse_baths(bathrooms) 
                    print("Correct fulls and half?:", full_baths, half_baths) 
                    fullBath_flag, halfBath_flag = True, True
                else:
                    fullBath_flag, halfBath_flag = True, True
            if list(property_details.strings)[i] == "Basement":
                basement = list(property_details.strings)[i+1] ## 14
                basement_flag = True
                print("Correct basement?:", basement)         

            if (list(property_details.strings)[i] == "StoriesTotal:") or (list(property_details.strings)[i] == "Stories:"):
                stories = list(property_details.strings)[i+2] ## 16
                stories_flag = True
                print("Correct stories?:", stories)     
            if (list(property_details.strings)[i] == "Structure type:") or (list(property_details.strings)[i] == "ArchitecturalStyle:"):
                architecture = list(property_details.strings)[i+2] ## 17
                architecture_flag = True
                print("Correct architecture?:", architecture)   
                # Some preprocessing of the data.
                if architecture == "CAPE COD" or architecture == "Cape cod":
                    architecture = "Cape Cod"
                if architecture == "TRANSITIONAL":
                    architecture = "Transitional"
            if list(property_details.strings)[i] == "Roof type:":
                roof = list(property_details.strings)[i+2] ## 18
                roof_flag = True
                print("Correct roof materials?:", roof)    
            if list(property_details.strings)[i] == "Exterior material:":
                exterior_mat = list(property_details.strings)[i+2] ## 19
                exterior_flag = True
                print("Correct exterior materials?:", exterior_mat)  

            if list(property_details.strings)[i] == "Exterior Features":
                if list(property_details.strings)[i] == "View Type":
                    exterior_feat = list(property_details.strings)[i+1]
                else:
                    exterior_feat = list(property_details.strings)[i+1] ## 19
                    exterior_feat_flag = True
                print("Correct exterior features?:", exterior_feat)          
            if list(property_details.strings)[i] == "Construction Materials:" or list(property_details.strings)[i] == "ConstructionMaterials:":
                construct_mat = list(property_details.strings)[i+2] ## 21
                construct_mat_flag = True
                print("Correct construction materials?:", construct_mat)

            if list(property_details.strings)[i] == "Flooring:":
                flooring = list(property_details.strings)[i+2] ## 21
                flooring_flag = True
                print("Correct flooring?:", flooring)  

        if home_type_flag == False:
            home_type = "Other"
        if heating_flag == False:
            heating = "No Data"
        if cooling_flag == False:
            cooling = "No Data"
        if bedroom_flag == False:
            bedrooms = "No Data"
        if lot_size_flag == False:
            lot_size = 0
        if fullBath_flag == False:
            full_baths = bath_rooms
        if halfBath_flag == False:
            half_baths = 0
        if basement_flag == False:
            basement = "None"
        if stories_flag == False:
            stories = 0
        if architecture_flag == False:
            architecture = "No Data"
        if roof_flag == False:
            roof = "No Data"
        if exterior_flag == False:
            exterior_mat = "No Data"
        if construct_mat_flag == False:
            construct_mat = "No Data"
        if flooring_flag == False:
            flooring = "No Data"

        heating1        = parse_one(heating.split(","))
        arch_style1     = parse_one(architecture.split(","))
        cooling1        = parse_one(cooling.split(","))
        exterior_feat1  = parse_one(exterior_feat.split(","))

        exteriors1, exteriors2          = parse_styles(exterior_mat.split(","))
        construct_mat1, construct_mat2  = parse_styles(construct_mat.split(","))
        flooring1, flooring2            = parse_styles(flooring.split(","))

        if floor_size != "--" and int(floor_size) > 0:
            price_sqft = round(int(list_price[1:].replace(',', '')) / int(floor_size))
        else:
            price_sqft = "No Data"
        # print("Price/Sqft:", price_sqft)

        if exterior_feat1 == "Lot":
            exterior_feat1 = "None"

        house_spec = [ids, heating1, cooling1, basement, flooring1, flooring2, arch_style1,
                        construct_mat1, construct_mat2, roof, lot_size, home_type, floor_size, 
                        bath_rooms, bedrooms, full_baths, half_baths, stories, exterior_feat1,
                        exteriors1, exteriors2, address, street_name, region, zipcode, year_built, 
                        monthYear_sold, price_sqft, list_price, content_details[j]]
        
        print(f"Appending #: {ids}")
        houses_specs.append(house_spec)
        ids += 1       

    print(f"\n *-*-*- Writing page {home} at {ids} *-*-*-\n")
    with open("bowie_housingV2.csv", "a") as f:
        wr = csv.writer(f, dialect="excel")
        wr.writerows(houses_specs)    

    







        
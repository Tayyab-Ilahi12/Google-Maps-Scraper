from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
##Data list
data = []
# result_count = 0

def get_url():
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)


    #        driver = webdriver.Chrome(options=options, ChromeDriverManager().install()
    driver = webdriver.Chrome(options=options,executable_path=r'chromedriver.exe')
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
    })
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/84.0.4147.89'})
    # print(driver.execute_script("return navigator.userAgent;"))
    url = "https://www.google.com/maps"
    driver.get(url)
    
    return driver
#####################################
def get_data_to_csv():
    df = pd.DataFrame(data, columns=['Name','Img link','Iframe Code','Main tag','Address','Website','Phone',
                                     'Opening Hours Sunday','Opening Hours Monday','Opening Hours Tuesday',
                                     'Opening Hours Wednesday','Opening Hours Thursday','Opening Hours Friday',
                                     'Opening Hours Saturday','Description','Review Rank','Chart info 5',
                                     'Chart info 4','Chart info 3','Chart info 2','Chart info 1',
                                     'Review 1 Name','Review 1 location','Review 1 rank','Review 1 text',
                                     'Review 2 Name','Review 2 location','Review 2 rank','Review 2 text',
                                     'Review 3 Name','Review 3 location','Review 3 rank','Review 3 text',
                                     'Review 4 Name','Review 4 location','Review 4 rank','Review 4 text',
                                     'Review 5 Name','Review 5 location','Review 5 rank','Review 5 text',
                                     'Review 6 Name','Review 6 location','Review 6 rank','Review 6 text',
                                     'Review 7 Name','Review 7 location','Review 7 rank','Review 7 text',
                                     'Review 8 Name','Review 8 location','Review 8 rank','Review 8 text',
                                     'Review 9 Name','Review 9 location','Review 19 rank','Review 9 text',
                                     'Review 10 Name','Review 10 location','Review 10 rank','Review 10 text','Key Word'])
    df.to_csv('Some_results.csv', index = False,encoding='utf-8-sig')
#####################################
def get_phone(driver):
    try:
        for i in driver.find_elements_by_tag_name('button'):
            if re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', i.text):
                phone = i.text.strip()
                return phone
            else:
                pass
    except Exception as e:
        print(e)
#####################################
def get_address(driver):
    address = 'N/A'
    try:
        for i in driver.find_elements_by_tag_name('button'):
            if 'address' in str(i.get_attribute('data-item-id')):
                actions = ActionChains(driver)
                actions.move_to_element(i).perform()
                address = i.text.strip()
                return address
            else:
                pass
    except Exception as e:
        print("Error in gettig address: ",e)
    return address
#####################################
def get_website(driver):
    website = 'N/A'
    try:
        for i in driver.find_elements_by_tag_name('button'):
            if 'Open website' in str(i.get_attribute('data-tooltip')):
                actions = ActionChains(driver)
                actions.move_to_element(i).perform()
                website = i.text.strip()
                return website
            else:
                pass
    except Exception as e:
        print("Error in gettig website: ",e)
    return website
#####################################
def get_thumbnail(driver):
    try:
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME,'section-hero-header-image')))
        img_link = driver.find_element_by_class_name('section-hero-header-image').find_element_by_tag_name('img').get_attribute("src")
        return img_link
    except Exception as e:
        pass
        # print("Error in getting thumbnail image: ",e)
#####################################
def rev_summary(driver):
    r5 = r4 = r3 = r2 = r1 = "N/A"
    for i in driver.find_elements_by_tag_name('tr'):
        try:
            if '5 stars' in i.get_attribute('aria-label'):
                r5 =  i.get_attribute('aria-label').split(',')[-1].split("reviews")[0].strip()
    #             print(r5)
            elif '4 stars' in i.get_attribute('aria-label'):
                r4 =  i.get_attribute('aria-label').split(',')[-1].split("reviews")[0].strip()
    #             print(r4)
            elif '3 stars' in i.get_attribute('aria-label'):
                r3 =  i.get_attribute('aria-label').split(',')[-1].split("reviews")[0].strip()
    #             print(r3)
            elif '2 stars' in i.get_attribute('aria-label'):
                r2 =  i.get_attribute('aria-label').split(',')[-1].split("reviews")[0].strip()
    #             print(r2)
            elif '1 stars' in i.get_attribute('aria-label'):
                r1 =  i.get_attribute('aria-label').split(',')[-1].split("reviews")[0].strip()
    #             print(r1)
            else:
                pass
        except:
            pass
    return r5,r4,r3,r2,r1
#####################################
def get_main_tag(driver):
    try:
        main_tag_element = driver.find_element_by_class_name('section-rating').find_elements_by_class_name('gm2-body-2')
        if main_tag_element[1].text == '':
            main_tag = main_tag_element[0].text.split('·')[-1].strip()
        else:
            main_tag = main_tag_element[1].text.strip()
        return main_tag
    except Exception as e:
        print("Error in getting Main Tag: ",e)
#####################################
def get_opening_hours(driver):
    opening_hours_dict = {'Monday':'N/A',
                         'Tuesday':'N/A',
                         'Wednesday':'N/A',
                         'Thursday':'N/A',
                         'Friday':'N/A',
                         'Saturday':'N/A',
                         'Sunday':'N/A'}
    try:
        # time.sleep(0.5)
        hours_button = driver.find_elements_by_class_name('cX2WmPgCkHi__section-info-hour-text')
        if hours_button != []:
            actions = ActionChains(driver)
            actions.move_to_element(hours_button[0]).perform()
            hours_button[0].click()
            elements = driver.find_elements_by_class_name('lo7U087hsMA__row-row') 
            if elements != []:
                for day in elements:
                    if 'Monday' in day.text:
                        opening_hours_dict['Monday'] = day.text.split("\n")[-1]
                    if 'Tuesday' in day.text:
                        opening_hours_dict['Tuesday'] = day.text.split("\n")[-1]
                    if 'Wednesday' in day.text:
                        opening_hours_dict['Wednesday'] = day.text.split("\n")[-1]
                    if 'Thursday' in day.text:
                        opening_hours_dict['Thursday'] = day.text.split("\n")[-1]
                    if 'Friday' in day.text:
                        opening_hours_dict['Friday'] = day.text.split("\n")[-1]
                    if 'Saturday' in day.text:
                        opening_hours_dict['Saturday'] = day.text.split("\n")[-1]
                    if 'Sunday' in day.text:
                        opening_hours_dict['Sunday'] = day.text.split("\n")[-1]          
                hours_button[0].click()
                return opening_hours_dict
            else:
                return opening_hours_dict
        else:
            return opening_hours_dict
    except Exception as e:
        print(e)
#####################################
def get_iframe(driver):
    try:
        # time.sleep(0.5)
        #share button
        driver.find_element_by_css_selector("button[aria-label=Share]").send_keys("\n")
        time.sleep(0.5)
        # wait for window to appear
        #########
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-dialog-widget"]/div[2]/div/div[3]/div/div/div[1]/div[2]/button[2]')))
        window = driver.find_element_by_xpath('//*[@id="modal-dialog-widget"]/div[2]/div/div[3]/div/div/div[1]/div[2]/button[2]')
        ##########
        window.click()
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME,'section-embed-map-input')))
        #Copy 
        iframe_code = driver.find_element_by_class_name('section-embed-map-input').get_attribute('value')
        #Close the window
        close_button = driver.find_element_by_class_name('modal-close-row')
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME,'modal-close-row')))
        actions = ActionChains(driver)
        actions.move_to_element(close_button).perform()
        close_button.click()
        return iframe_code
    except Exception as iframe_func:
        print("Error in getting iframe code: ",iframe_func)
#####################################
def scroll_again(driver):
    try:
        scrollable_div = driver.find_element_by_css_selector(
            'div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
                )
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight', 
                scrollable_div
                )
        time.sleep(1.5)
        ###############
        reviews = driver.find_elements_by_class_name('section-review-content')
        return reviews
    except Exception as e:
        print("Error in scrolling reviews againg:",e)
#####################################
def get_review(driver):
    check_iframe_window(driver)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ozj7Vb3wnYq__section-topappbar")))
    time.sleep(0.7)
    for i in range(2):
        reviews10 = []
        try:
            reviews = review_name = review_location = review_text = review_rank = "N/A"
            try:
                scrollable_div = driver.find_element_by_css_selector(
                 'div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
                                     )
                driver.execute_script(
                               'arguments[0].scrollTop = arguments[0].scrollHeight', 
                                scrollable_div
                               )
                time.sleep(1.5)
                ###############
                reviews = driver.find_elements_by_class_name('section-review-content')
            except:
                try:
                    reviews = scroll_again(driver)
                except Exception as e:
                    print("Error in scrolling reviews:",e)
            #############################################
            try:
                for rev in reviews:
                    review_name = review_location = review_text = review_rank = "N/A"
                    try:
                        review_name = rev.find_element_by_class_name('section-review-title').text
                    except:
                        pass
                    try:
                        review_location = rev.find_element_by_class_name('section-review-subtitle').find_elements_by_tag_name('span')[0].text
                    except:
                        pass
                    try:
                        review_rank = rev.find_element_by_class_name('section-review-stars').get_attribute('aria-label').strip()
                    except:
                        pass
                    try:
                        more_button = rev.find_element_by_tag_name('jsl')
#                         print("Clicked review")
                        actions = ActionChains(driver)
                        actions.move_to_element(more_button).perform()
                        time.sleep(0.2)
                        # if " Read more on " in more_button.text or ".com" in more_button.text:
                            # pass
                        if more_button.text == "More":
                            more_button.click()
                        else:
                            pass
                    except:
                        pass
                    try:
                        review_text = rev.find_element_by_class_name('section-review-text').text.strip()
                    except:
                        pass
                    reviews10.append((review_name,review_location,review_rank,review_text))

            except Exception as f:
                print("Error in getting review data:",f)
                pass
        except:
            pass
    if len(reviews10) > 10:
        return reviews10[:10]
    else:
        return reviews10
#####################################
def click_back_to_profile(driver):
    print("Clicking back to main profile")
    try:
        back_bt = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[1]/button[1]')
            # driver.find_element_by_class_name('ozj7Vb3wnYq__action-button-container').send_keys('\n')
        actions = ActionChains(driver)
        actions.move_to_element(back_bt).perform()
        time.sleep(0.2)
        back_bt.send_keys("\n")
        time.sleep(0.2)
    except Exception as back_bt_exp:
        print("Error in clicking back button of review section: ",back_bt_exp)
#####################################
def check_iframe_window(driver):
    try:
        share_window = driver.find_elements_by_class_name('section-copy-link')
        if len(share_window) > 0 and share_window[0].is_displayed():
            close_button = driver.find_element_by_class_name('modal-close-row')
            actions = ActionChains(driver)
            actions.move_to_element(close_button).perform()
            close_button.click()
        else:
            try:    #Close the window
                close_button = driver.find_element_by_class_name('modal-close-row')
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,'modal-close-row')))
                actions = ActionChains(driver)
                actions.move_to_element(close_button).perform()
                close_button.click()
            except:
                pass
    except:
        pass
#####################################
def get_data(driver,keyword):
    try:
        try:
            opening_hours = opening_hours_monday  = description =  "N/A" 
            opening_hours_wednesday = opening_hours_thursday = opening_hours_tuesday = "N/A" 
            opening_hours_friday = opening_hours_saturday = opening_hours_sunday = "N/A"
            r5 = r4 = r3 = r2 = r1 =  iframe_code = "N/A"
            r1_name = r1_location = r1_rank = r1_text = r2_name = r2_location = r2_rank = r2_text = "N/A" 
            r3_name = r3_location = r3_rank = r3_text = r4_name = r4_location = r4_rank = r4_text = "N/A"
            r5_name = r5_location = r5_rank = r5_text = r6_name = r6_location = r6_rank = r6_text = "N/A"
            r7_name = r7_location = r7_rank = r7_text = r8_name = r8_location = r8_rank = r8_text = "N/A"
            r9_name = r9_location = r9_rank = r9_text = r10_name = r10_location = r10_rank = r10_text = "N/A"
            main_tag =  img_link = iframe_code = "N/A"
            name = address = phone = star_rating = total_reviews = opening_hours = website = 'N/A'
        except:
            pass
        try:
            name = driver.find_element_by_class_name('section-hero-header-title-description').text.strip().split('\n')[0]
            print(name)
        except:
            try:
                name = driver.find_element_by_class_name('section-hero-header-title-description').text.strip().split('\n')[0]
            except Exception as gd1:
                print("GD1:",gd1)
        ##################################
        try:
            description = driver.find_element_by_class_name('section-editorial-quote').text
        except Exception as gd3:
            # print("No description found")
            pass
        try:
            main_tag = get_main_tag(driver)
        except Exception as gd4:
            print("GD4:",gd4)
            pass
        ##################################
        try:
            star_rating = driver.find_element_by_class_name('section-star-display').text.strip()
        except Exception as gd5:
            print("GD5",gd5)
            pass
        ################################################
        try:
            opening_hours = get_opening_hours(driver)
            opening_hours_monday = opening_hours['Monday']
            opening_hours_tuesday = opening_hours['Tuesday']
            opening_hours_wednesday = opening_hours['Wednesday']
            opening_hours_thursday = opening_hours['Thursday']
            opening_hours_friday = opening_hours['Friday']
            opening_hours_saturday = opening_hours['Saturday']
            opening_hours_sunday = opening_hours['Sunday']
        except Exception as gd6:
            print("GD6:",gd6)
            pass
        ###################################
        try:
            time.sleep(1)
            img_link = get_thumbnail(driver)
        except Exception as gd2:
            print("GD2:",gd2)
            pass
        
        ####################################
        try:
            r5 , r4 , r3 , r2 , r1 = rev_summary(driver)
        except Exception as gd7:
            print("GD7:",gd7)
            pass
        ####################################
        try:
            phone = get_phone(driver)
        except Exception as gd8:
            print("GD8:",gd8)
            pass
        ####################################
        try:
            address = get_address(driver)
        except Exception as gd9:
            print("GD9:",gd9)
            pass
        ###################################
        try:
            website = get_website(driver)
        except Exception as gd10:
            print("GD10:",gd10)
            pass
        ##########################################
        try:
            iframe_code = get_iframe(driver)
            try:
                check_iframe_window(driver)
            except:
                pass
        except Exception as gd11: 
            print("GD11:",gd11)
            pass
        ##########################################
        try:
            print("Getting into reviews")
            all_rev_button = driver.find_element_by_class_name('section-rating').find_element_by_tag_name('button')
            actions = ActionChains(driver)
            actions.move_to_element(all_rev_button).perform()
            all_rev_button.send_keys("\n")

            reviews = get_review(driver)
            
            try:
                r1_name = reviews[0][0]
                r1_location = reviews[0][1]
                r1_rank = reviews[0][2]
                r1_text = reviews[0][3]
            except:
                pass
            ###########
            try:
                r2_name = reviews[1][0]
                r2_location = reviews[1][1]
                r2_rank = reviews[1][2]
                r2_text = reviews[1][3]
            except:
                pass
            ###########
            try:
                r3_name = reviews[2][0]
                r3_location = reviews[2][1]
                r3_rank = reviews[2][2]
                r3_text = reviews[2][3]
            except:
                pass
            ###########
            try:
                r10_name = reviews[9][0]
                r10_location = reviews[9][1]
                r10_rank = reviews[9][2]
                r10_text = reviews[9][3]
            except:
                pass
            ###########
            try:
                r4_name = reviews[3][0]
                r4_location = reviews[3][1]
                r4_rank = reviews[3][2]
                r4_text = reviews[3][3]
            except:
                pass
            ###########
            try:
                r5_name = reviews[4][0]
                r5_location = reviews[4][1]
                r5_rank = reviews[4][2]
                r5_text = reviews[4][3]
            except:
                pass
            ###########
            try:
                r6_name = reviews[5][0]
                r6_location = reviews[5][1]
                r6_rank = reviews[5][2]
                r6_text = reviews[5][3]
            except:
                pass
            ###########
            try:
                r7_name = reviews[6][0]
                r7_location = reviews[6][1]
                r7_rank = reviews[6][2]
                r7_text = reviews[6][3]
            except:
                pass
            ###########
            try:
                r8_name = reviews[7][0]
                r8_location = reviews[7][1]
                r8_rank = reviews[7][2]
                r8_text = reviews[7][3]
            except:
                pass
            ###########
            try:
                r9_name = reviews[8][0]
                r9_location = reviews[8][1]
                r9_rank = reviews[8][2]
                r9_text = reviews[8][3]
            except:
                pass
            ###########

            click_back_to_profile(driver)
            time.sleep(1)
        except Exception as rev_exp:
            print("No reviews found\n Error: ",rev_exp)
            
        if(img_link == "N/A"):
            try:
                time.sleep(1)
                img_link = get_thumbnail(driver)
            except Exception as gd12:
                print("GD12:",gd12)
                pass
        ###########################################
        data.append((name,img_link,iframe_code,main_tag,address,website,phone,opening_hours_sunday,
                    opening_hours_monday,opening_hours_tuesday,opening_hours_wednesday,
                    opening_hours_thursday,opening_hours_friday,opening_hours_saturday,description,
                    star_rating,r5,r4,r3,r2,r1,r1_name,r1_location ,r1_rank , r1_text , 
                    r2_name , r2_location , r2_rank , r2_text ,r3_name , r3_location , r3_rank , r3_text ,
                    r4_name , r4_location , r4_rank ,r4_text, r5_name , r5_location , r5_rank , r5_text , 
                    r6_name , r6_location , r6_rank , r6_text, r7_name , r7_location , r7_rank , r7_text , 
                    r8_name , r8_location , r8_rank ,r8_text, r9_name , r9_location , r9_rank , r9_text , 
                    r10_name , r10_location , r10_rank,r10_text,keyword))
                    
        print("Img_link:",img_link)
        print("Iframe code: ",iframe_code)
        print('Name: ',name)
        print("Main tag:",main_tag)
        print('Website: ',website)
        print('Phone: ',phone)
        print('Address: ',address)
        # print('Review Rank: ',star_rating)
        # print("Review Summary:\n")
        # print("5-stars:",r5)
        # print("4-stars:",r4)
        # print("3-stars:",r3)
        # print("2-stars:",r2)
        # print("1-stars:",r1)
        # print(reviews[0])
        # print('Opening Hours: \n')
        # print('Opening Hours Monday:',opening_hours_monday)
        # print('Opening Hours Tuesday:',opening_hours_tuesday)
        # print('Opening Hours Wednesday:',opening_hours_wednesday)
        # print('Opening Hours Thursday:',opening_hours_thursday)
        # print('Opening Hours Friday:',opening_hours_friday)
        # print('Opening Hours Saturday:',opening_hours_saturday)
        # print('Opening Hours Sunday:',opening_hours_sunday)
        
        
    except Exception as e:
        print("Error in get data function:",e)
#####################################
def next_page(driver):    
    try:
        next_button = driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').is_enabled()
        if next_button:
            print("next button is enabled")
            try:
                element=driver.find_element_by_class_name('section-no-result-title')
                return False
            except NoSuchElementException:
                try:
                    print("here")
                    WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, "n7lv7yjyC35__section-pagination-button-next")))
                    button = driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next')
                    actions = ActionChains(driver)
                    actions.move_to_element(button).perform()
                    button.click()
                    time.sleep(5)
                    return True
                except Exception as e:
                    print(e)
        else:
            return False
    except Exception as e:
        print(e)    
#####################################
def click_back(driver):
    try:
        for i in driver.find_elements_by_tag_name('span'):
            if "Back to results" in i.text:
                actions = ActionChains(driver)
                actions.move_to_element(i).perform()
                i.click()
                break
    except Exception as e:
        print("click back function: ",e)
#####################################
def check_window_location(driver):
    try:
        time.sleep(1)

        review_window = driver.find_elements_by_class_name("ozj7Vb3wnYq__section-topappbar")
        business_main_window = driver.find_elements_by_class_name('section-hero-header-title-description')
        share_window = driver.find_elements_by_class_name('section-copy-link')

        if len(share_window) > 0 and share_window[0].is_displayed():
            close_button = driver.find_element_by_class_name('modal-close-row')
            actions = ActionChains(driver)
            actions.move_to_element(close_button).perform()
            close_button.click()
            time.sleep(1)
        else:
            try:    #Close the window
                close_button = driver.find_element_by_class_name('modal-close-row')
                WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME,'modal-close-row')))
                actions = ActionChains(driver)
                actions.move_to_element(close_button).perform()
                close_button.click()
            except:
                pass

        if len(review_window) > 0 and review_window[0].is_displayed():
        #     print("True, In review window")
        #     print("Clicking back to main product and main page....")
            try:
                click_back_to_profile(driver)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "section-hero-header-title-description")))
                click_back(driver)
            except:
                pass

        elif len(business_main_window) > 0 and business_main_window[0].is_displayed:
        #     print("In business main window")
        #     print("Clicking back to main result page....")
            try:
                click_back(driver)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "section-hero-header-title-description")))
            except:
                pass
        else:
            pass

    except Exception as e:
        # print("Window Check Function Error:",e)
        pass
#####################################
def click_each_result(driver,keyword):
    try:
        search_list = driver.find_elements_by_class_name("section-result")
        for i in range(len(search_list)):
            print('#########################')
            try:
                check_window_location(driver)
                check_iframe_window(driver)
                search_list[i].click()
#                 WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__taparea")))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-hero-header-title-description")))
                time.sleep(1.5)
                # print('after sleep')
                # print("In get data fucntion")
                get_data(driver,keyword)
                print("Item done\n")
                # print('Now clicking back')
                click_back(driver)
                check_window_location(driver)
                print("Clicked back")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "section-result-content")))
                time.sleep(1)
                search_list = driver.find_elements_by_class_name("section-result")
                check_window_location(driver)
            except Exception as fd:
                print("Error Loop of click each res func in :",fd)
                pass
        # print("Leaving click each result func")
    except Exception as e:
        print("click each result function: ",e)
#####################################
def next_button_click2(driver):
    try:
        i = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[7]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/div/button[2]')
        if i:
            actions = ActionChains(driver)
            actions.move_to_element(i).perform()
            i.send_keys('\n')  
            check_window_location(driver)
            return True
        else:
            return False
    except:
        pass
#####################################
def overWrite_File(items):
    try:
        with open('keywords.txt', 'w') as f:
            for item in items:
                f.write("%s\n" % item)
    except Exception as fd:
        print("Error in updating keywords: ",fd)
#####################################
def load_data():
    try:
        
        with open("keywords.txt") as file_in:
            key_words = []
            for line in file_in:
                if line != "\n":
                    key_words.append(line.strip())
                elif line == "\n" or line == None:
                    pass
        return key_words
    except Exception as fileOpen:
        print("Error in file opening: ",fileOpen)
#####################################
def main():
    key_words = load_data()
    result_count = 0
    count = 0
    if len(key_words) > 0:
        print("key words loaded")
        driver = get_url()
        #######################
        for keyWord in key_words:
            check_window_location(driver)
            time.sleep(1)
            check_iframe_window(driver)
            print("Searching for key word: ",keyWord)
            driver.find_element_by_id("searchboxinput").send_keys(keyWord)
            driver.find_element_by_id("searchbox-searchbutton").click()
            time.sleep(2)
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "section-result")))
            except:
                pass
            next_button = True
            ##########################
            while next_button:
                click_each_result(driver,keyWord)
                time.sleep(1)
                try:
                    check_window_location(driver)
                    next_button = next_button_click2(driver)
                    if keyWord == driver.find_element_by_id("searchboxinput").get_attribute('value'):
                        pass
                    else:
                        print("No more records")
                        break
                except Exception as next_bt:
                    check_window_location(driver)
                    print("Error clicking Next button:",next_bt)
                time.sleep(1.5)
            #########################
            try:
                driver.find_element_by_id('searchboxinput').clear()
            except:
                pass
            #########################
            print("Scraping "+keyWord," Complete")
            try:
                count = count + 1
                overWrite_File(key_words[count:])
                print("Key word file updated")
            except Exception as ov:
                print("Error in over writing left keywords!",ov)
                pass
            #########################
        driver.close()
    else:
        print("No key words!")
    
########################################
if __name__ == "__main__":
    print("Starting program")
    main()
    get_data_to_csv()
    print("Data saved")
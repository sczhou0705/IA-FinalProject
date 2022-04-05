import pandas as pd
import s3fs

def main(event = None, context = None):
    print("Start running LinkedInScraper")
    values = [['Atreish Ramlakhan',
              'New York, New York, United States',
              'Katz School at Yeshiva University',
              'Graduate Teaching Assistant',
              'https://www.linkedin.com/company/16181365/'],
             ['Yuxiao (Henry) Shen',
              'New York, New York, United States',
              'The AAT Project (America’s Amazing Teens, LLC)',
              'Full Stack PHP Web Developer',
              'https://www.linkedin.com/search/results/all/?keywords=The+AAT+Project+%28America%E2%80%99s+Amazing+Teens%2C+LLC%29'],
             ['Shichao Zhou',
              'New York, New York, United States',
              'S&P Global Market Intelligence · Internship',
              'Data Analyst',
              'https://www.linkedin.com/company/162892/'],
             ['Mahlet Melese', 'New York, New York, United States', None, None, None]]
    df = pd.DataFrame(values,columns = [["Full Name", "Location", "Most Recent Company", 'Job Title', 'Company Url']])
    ###LOAD THE FILE INTO S3####
    # prepare csv file name   
    pathname = 'ia-final2022-csv/'#specify location of s3:/{my-bucket}/
    filenames = f"{pathname}linkedIn_info.csv" #name of the filepath and csv file

    #encoding must be adjusted to accommodate abnormal characters. Use s3fs to write to S3 bucket
    print("Start adding LinkedIn data to csv")
    byte_encoded_df = df.to_csv(None, index=False).encode() #encodes file as binary
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(filenames, 'wb') as file:
        file.write(byte_encoded_df) #writes byte-encoded file to s3 location

    #print success message
    print("Successfull uploaded file to location:"+str(filenames))
    print("Complete running LinkedInScraper")
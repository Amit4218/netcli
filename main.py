from src.utils.soap_scraper import start_soap_scraper


def run() -> None: 

    user_query = input("Enter a movie name: ")
    
    start_soap_scraper(user_query=user_query)
    
    
if __name__ == "__main__":
    run()
def main():
    import scraper
    
    last_run_nick = ""
    last_run_bakke = ""

    scraper.update_nick_if_new_data()
        

if __name__ == "__main__":
    main()
else:
    raise ImportError()
import pandas as pd
import requests
from bs4 import BeautifulSoup


def powerfm_last_played_songs_info():
    headers = ({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    try:
        response = requests.get("https://www.powerapp.com.tr/powerfm/song-history/", headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # We are collecting datas via soup and creating variables
        singer = soup.find('span', {'class': 'item-title'}).text.strip()
        song = soup.find('span', {'class': 'item-subtitle'}).text.strip()
        datetime = soup.find('span', {'class': 'item-date'}).text.strip()
        return song, singer, datetime
    except AttributeError:
        print("Couldn't find the information.")
        return None


if __name__ == "__main__":

    song_info = powerfm_last_played_songs_info()
    if song_info: # If song information is success
        singer, song, datetime = song_info
        print("Last Played Song :", song, ",", singer, ",", datetime)  # Printing in screen
        Sarki = singer + " - " + song

        # We are opening existing Excel file
        df_mevcut = pd.read_excel("powerfm_last_played_songs.xlsx")

        # We are getting data, last row's last cell
        son_satir = df_mevcut.iloc[-1]
        time_control_veri = son_satir['Time']

        # We are checking if last played song already in last row in Excel, if there is not; we are updating Excel file.
        if time_control_veri != datetime:
            yeni_veri = {"Last Played Song": singer+" - "+song, "Time": datetime}
            df_yeni = pd.DataFrame([yeni_veri])
            df_birlesik = pd.concat([df_mevcut, df_yeni], ignore_index=True)
            df_birlesik.to_excel("powerfm_last_played_songs.xlsx", index=False)
            print("Excel file has been updated.")
        else:
            print("Last song already wrote in Excel file. Excel file has not been updated.")

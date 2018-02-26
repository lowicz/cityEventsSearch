komendy po kolei do odpalenia:

git clone https://github.com/lowicz/cityEventsSearch.git
docker build -t city_events_search .
docker run -i -t --entrypoint /bin/bash city_events_search

teraz jesteś już w środowisku dockera,
uruchamiasz apkę normalnie:
python main.py

każde kolejne uruchomienie:
docker run -i -t --entrypoint /bin/bash city_events_search
python main.py

komendy po kolei do odpalenia:

git clone https://github.com/lowicz/cityEventsSearch.git
docker build -t city_events_search .
docker run -ti city_events_search

każde kolejne uruchomienie:
docker run -ti city_events_search